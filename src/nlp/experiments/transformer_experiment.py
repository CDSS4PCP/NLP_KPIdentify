"""Transformer token-classification experiment (reviewer concern #1).

Runs a controlled "sanity-check" biomedical transformer baseline (PubMedBERT /
BioBERT / SciBERT) for keyphrase identification on the SAME synthetic train split
and GS42/GS91 test splits used by the BiLSTM/HAN-CRF pipeline.

Pipeline:
  1. Reuse ``mark_keyword_all_sentences`` to derive word-level BIO labels from each
     document's keyword list (identical labeling to the classical pipeline).
  2. Tokenize with the HF fast tokenizer; align labels to subwords (label on first
     subword, -100 on continuations and special tokens).
  3. Fine-tune for a few epochs (manual torch loop, no Trainer dependency).
  4. Evaluate with seqeval strict IOB2 on GS42/GS91; optionally dump per-document
     word-level gold/pred tags compatible with error_analysis.py / bootstrap_ci.py.

This module intentionally mirrors the I/O contract of GNAExperiment.evaluate()'s
prediction dump so downstream analysis tools are shared across model families.
"""
import os
import time
import json
import random

import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader

from src.core import configV2 as config
from src.nlp.utils.io import read_json_array, save_json
from src.nlp.models.preProcessData import (
    mark_keyword_all_sentences,
    normalize_sentence_tokens_for_alignment,
)
from src.nlp.models.transformer_token_classifier import (
    build_token_classifier,
    resolve_model_name,
    LABEL_LIST,
    LABEL2ID,
    ID2LABEL,
)


def set_global_seed(seed):
    seed = int(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    return seed


def _document_to_words_labels(article, nlp_cache):
    """Return (words, bio_labels) for a single article using shared labeling logic."""
    if "sentences" not in article or not article["sentences"]:
        nlp = nlp_cache.get("nlp")
        if nlp is None:
            import spacy
            nlp = spacy.blank("en")
            nlp.add_pipe("sentencizer")
            nlp_cache["nlp"] = nlp
        text = article.get("title", "") + " " + article.get("abstract", "")
        doc = nlp(text)
        article["sentences"] = [
            normalize_sentence_tokens_for_alignment([token.text for token in sent])
            for sent in doc.sents
        ]
    keywords = article.get("keywords", [])
    _, labels, sentences = mark_keyword_all_sentences(keywords, article["sentences"], schema="BIO")
    words, bio = [], []
    for sent_tokens, sent_labels in zip(sentences, labels):
        words.extend(sent_tokens)
        bio.extend(sent_labels)
    return words, bio


class _TokenClsDataset(Dataset):
    """Tokenizes word/label sequences and aligns labels to subword pieces."""

    def __init__(self, docs, tokenizer, max_length):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.docs = [d for d in docs if d[0]]  # drop empty-word docs

    def __len__(self):
        return len(self.docs)

    def __getitem__(self, idx):
        words, bio = self.docs[idx]
        enc = self.tokenizer(
            words,
            is_split_into_words=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors=None,
        )
        word_ids = enc.word_ids()
        label_ids = []
        prev_word = None
        for wid in word_ids:
            if wid is None:
                label_ids.append(-100)
            elif wid != prev_word:
                label_ids.append(LABEL2ID.get(bio[wid], 0))
            else:
                label_ids.append(-100)  # only first subword carries the label
            prev_word = wid
        enc["labels"] = label_ids
        enc["word_ids_list"] = [wid if wid is not None else -1 for wid in word_ids]
        return enc, words, bio


def _collate(batch, tokenizer):
    encs = [b[0] for b in batch]
    words = [b[1] for b in batch]
    bios = [b[2] for b in batch]
    maxlen = max(len(e["input_ids"]) for e in encs)
    pad_id = tokenizer.pad_token_id or 0

    input_ids, attention, labels, word_ids = [], [], [], []
    for e in encs:
        n = len(e["input_ids"])
        pad = maxlen - n
        input_ids.append(e["input_ids"] + [pad_id] * pad)
        attention.append(e["attention_mask"] + [0] * pad)
        labels.append(e["labels"] + [-100] * pad)
        word_ids.append(e["word_ids_list"] + [-1] * pad)
    out = {
        "input_ids": torch.tensor(input_ids, dtype=torch.long),
        "attention_mask": torch.tensor(attention, dtype=torch.long),
        "labels": torch.tensor(labels, dtype=torch.long),
    }
    return out, word_ids, words, bios


class TransformerExperiment:
    def __init__(self, config_dict):
        self.config = config_dict
        seed = self.config.get("seed", 42)
        self.seed = set_global_seed(seed)

        # Resolve the active JSON_DATA directory: explicit --jsonDataDir wins; otherwise a
        # non-synthetic --dataSource selects its default public-dataset folder. Setting the
        # module global propagates to every config.JSON_DATA reference below.
        data_source = self.config.get("dataSource", "synthetic") or "synthetic"
        json_dir_override = self.config.get("jsonDataDir", None)
        if not json_dir_override and data_source != "synthetic":
            if data_source == "kpbiomed":
                json_dir_override = getattr(config, "PUBLIC_DATA_KPBIOMED", None)
            elif data_source == "pubmedake":
                json_dir_override = getattr(config, "PUBLIC_DATA_PUBMEDAKE", None)
        if json_dir_override:
            config.JSON_DATA = json_dir_override
            print(f"Using JSON_DATA directory: {config.JSON_DATA} (dataSource={data_source})")

        device_str = self.config.get("device")
        if device_str:
            self.device = torch.device(device_str)
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"TransformerExperiment device: {self.device} | seed: {self.seed}")

        self.hf_model = self.config.get("hfModel", "pubmedbert")
        self.max_length = int(self.config.get("maxLength", 256))
        self.batch_size = int(self.config.get("batchSize", 16))
        self.epochs = int(self.config.get("epochs", 3))
        self.lr = float(self.config.get("lr", 3e-5))
        self.dump_predictions = self.config.get("dumpPredictions", None)
        self.transfer_model = self.config.get(
            "transferModel", "d4data/biomedical-ner-all"
        )
        self.tokenizer = None
        self.model = None
        self.transfer_mode = False
        self.transfer_id2label = None

    # ------------------------------------------------------------------ data
    def _load_docs(self, filename):
        path = os.path.join(os.getcwd(), config.JSON_DATA, filename)
        if not os.path.exists(path):
            return None
        raw = read_json_array(path)
        nlp_cache = {}
        return [_document_to_words_labels(a, nlp_cache) for a in raw]

    # ----------------------------------------------------------------- train
    def train(self):
        print(f"Fine-tuning transformer baseline: {resolve_model_name(self.hf_model)}")
        self.tokenizer, self.model = build_token_classifier(self.hf_model)
        self.model.to(self.device)

        train_docs = self._load_docs("train.json")
        if not train_docs:
            print("No train.json found; cannot fine-tune.")
            return
        train_sample_size = self.config.get("trainSampleSize", None)
        if train_sample_size and train_sample_size > 0 and len(train_docs) > train_sample_size:
            idx = np.random.default_rng(self.seed).permutation(len(train_docs))[:train_sample_size]
            original_train_docs = len(train_docs)
            train_docs = [train_docs[i] for i in idx]
            print(
                f"Training subsampled to trainSampleSize={train_sample_size} "
                f"(from {original_train_docs} docs, seed={self.seed})."
            )
        ds = _TokenClsDataset(train_docs, self.tokenizer, self.max_length)
        loader = DataLoader(
            ds,
            batch_size=self.batch_size,
            shuffle=True,
            collate_fn=lambda b: _collate(b, self.tokenizer),
        )
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.lr, weight_decay=0.01)
        use_amp = self.device.type == "cuda"
        scaler = torch.cuda.amp.GradScaler(enabled=use_amp)

        self.model.train()
        for epoch in range(self.epochs):
            ep_start = time.time()
            total_loss = 0.0
            for batch, _wids, _words, _bios in loader:
                inputs = {k: v.to(self.device) for k, v in batch.items()}
                optimizer.zero_grad()
                with torch.cuda.amp.autocast(enabled=use_amp):
                    out = self.model(**inputs)
                    loss = out.loss
                scaler.scale(loss).backward()
                scaler.step(optimizer)
                scaler.update()
                total_loss += float(loss.item())
            print(
                f"Epoch {epoch + 1}/{self.epochs} | loss={total_loss / max(1, len(loader)):.4f} "
                f"| {time.time() - ep_start:.1f}s"
            )

        out_dir = os.path.join(os.getcwd(), config.INTERIM_DATA, f"transformer_{self.hf_model}")
        os.makedirs(out_dir, exist_ok=True)
        self.model.save_pretrained(out_dir)
        self.tokenizer.save_pretrained(out_dir)
        print(f"Saved fine-tuned transformer to {out_dir}")

    # ------------------------------------------------------- zero-shot load
    def load_base_zero_shot(self):
        """Load the base pretrained encoder with an untrained token-classification head.

        This is the "direct inference without fine-tuning" baseline (Phase 8). No
        public keyphrase-fine-tuned head exists for these biomedical encoders, so
        ``AutoModelForTokenClassification`` attaches a freshly (randomly)
        initialized classifier layer on top of the pretrained weights. The global
        seed is set first so the random head is reproducible across runs. The
        resulting predictions therefore reflect the pretrained encoder WITHOUT any
        task supervision — a lower-bound reference, not a trained model.
        """
        set_global_seed(self.seed)
        print(
            f"Zero-shot (no fine-tuning) baseline: {resolve_model_name(self.hf_model)} "
            f"| classifier head randomly initialized (seed {self.seed})"
        )
        self.tokenizer, self.model = build_token_classifier(self.hf_model)
        self.model.to(self.device)
        return True

    # ------------------------------------------------- zero-shot NER transfer
    def load_pretrained_ner_head(self):
        """Load a REAL pretrained biomedical-NER token classifier (Option B).

        Unlike ``load_base_zero_shot`` (random head), this uses an off-the-shelf
        checkpoint that already ships a TRAINED token-classification head, then
        applies it zero-shot by mapping any recognized biomedical entity span onto
        our keyphrase scheme (entity -> B-KP/I-KP, outside -> O). The head was
        trained on a different taxonomy, so this is a *zero-shot transfer* baseline
        with a documented label-mapping heuristic, not an in-domain model.
        """
        from transformers import AutoTokenizer, AutoModelForTokenClassification

        set_global_seed(self.seed)
        ckpt = self.transfer_model
        print(
            f"Zero-shot transfer baseline: {ckpt} (pretrained NER head, "
            f"entity->keyphrase mapping, seed {self.seed})"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(ckpt, use_fast=True)
        self.model = AutoModelForTokenClassification.from_pretrained(ckpt)
        self.model.to(self.device)
        self.transfer_id2label = dict(self.model.config.id2label)
        self.transfer_mode = True
        return True

    @staticmethod
    def _entity_label_to_kp(raw_label, prev_was_entity):
        """Map an arbitrary NER label string onto our keyphrase BIO scheme.

        Any recognized biomedical entity is treated as a keyphrase candidate;
        BIO/BILOU prefixes are honored when present, otherwise span boundaries are
        inferred from whether the previous token was already inside an entity.
        Returns ``(kp_label, is_entity)``.
        """
        if raw_label is None:
            return "O", False
        upper = str(raw_label).strip().upper()
        if upper in ("O", "", "OUTSIDE") or upper.endswith("-O"):
            return "O", False
        if upper.startswith(("B-", "S-", "U-")):
            return "B-KP", True
        if upper.startswith(("I-", "E-", "L-")):
            return ("I-KP" if prev_was_entity else "B-KP"), True
        # Bare entity type (no BIO prefix): infer boundary from continuity.
        return ("I-KP" if prev_was_entity else "B-KP"), True

    def _resolve_transfer_label(self, idx):
        m = self.transfer_id2label or {}
        if idx in m:
            return m[idx]
        return m.get(str(idx))

    def evaluate_transfer(self):
        """Evaluate the zero-shot NER-transfer model on GS42/GS91 (Option B)."""
        from seqeval.metrics import (
            classification_report,
            f1_score,
            precision_score,
            recall_score,
        )
        from seqeval.scheme import IOB2

        if self.model is None or not self.transfer_mode:
            print("Transfer model not loaded; call load_pretrained_ner_head() first.")
            return
        if self.dump_predictions:
            os.makedirs(self.dump_predictions, exist_ok=True)

        gs_files = [
            ("testgs42.json", "Gold Standard 42"),
            ("testgs91.json", "Gold Standard 91"),
        ]
        self.model.eval()
        for filename, label in gs_files:
            docs = self._load_docs(filename)
            if not docs:
                print(f"Warning: {filename} not found; skipping.")
                continue
            ds = _TokenClsDataset(docs, self.tokenizer, self.max_length)
            loader = DataLoader(
                ds,
                batch_size=self.batch_size,
                shuffle=False,
                collate_fn=lambda b: _collate(b, self.tokenizer),
            )

            y_true, y_pred, dump_records = [], [], []
            with torch.no_grad():
                for batch, word_ids, words_batch, bios_batch in loader:
                    inputs = {
                        k: v.to(self.device) for k, v in batch.items() if k != "labels"
                    }
                    logits = self.model(**inputs).logits
                    preds = logits.argmax(-1).cpu().tolist()
                    for b in range(len(words_batch)):
                        words = words_batch[b]
                        gold_bio = bios_batch[b]
                        wids = word_ids[b]
                        word_pred = ["O"] * len(words)
                        seen = set()
                        prev_entity = False
                        for pos, wid in enumerate(wids):
                            if wid is None or wid < 0 or wid in seen or wid >= len(words):
                                continue
                            seen.add(wid)
                            raw = self._resolve_transfer_label(preds[b][pos])
                            kp, is_ent = self._entity_label_to_kp(raw, prev_entity)
                            word_pred[wid] = kp
                            prev_entity = is_ent
                        eval_len = len(words)
                        gold_seq = gold_bio[:eval_len]
                        pred_seq = word_pred[:eval_len]
                        y_true.append(gold_seq)
                        y_pred.append(pred_seq)
                        if self.dump_predictions:
                            dump_records.append({
                                "tokens": words[:eval_len],
                                "gold": gold_seq,
                                "pred": pred_seq,
                            })

            if not y_true:
                print(f"No samples processed for {label}.")
                continue

            print(f"\nEvaluating on {label} dataset: {filename}")
            print(classification_report(y_true, y_pred, mode="strict", scheme=IOB2, zero_division=0))
            prec = precision_score(y_true, y_pred, mode="strict", scheme=IOB2, zero_division=0) * 100
            rec = recall_score(y_true, y_pred, mode="strict", scheme=IOB2, zero_division=0) * 100
            f1 = f1_score(y_true, y_pred, mode="strict", scheme=IOB2, zero_division=0) * 100
            flat_t = [t for s in y_true for t in s]
            flat_p = [t for s in y_pred for t in s]
            acc = (sum(1 for a, c in zip(flat_t, flat_p) if a == c) / max(1, len(flat_t))) * 100
            print("-" * 65)
            print(f"{'SeqEval Overall':<17} | {'Precision':>9} | {'Recall':>9} | {'F1-Score':>9} | {'Accuracy':>9}")
            print("-" * 65)
            print(f"{'Score (%)':<17} | {prec:>8.2f}% | {rec:>8.2f}% | {f1:>8.2f}% | {acc:>8.2f}%")
            print("-" * 65)

            if self.dump_predictions:
                base_name = filename.split(".")[0]
                dump_path = os.path.join(self.dump_predictions, f"predictions_{base_name}.json")
                save_json({
                    "dataset_label": label,
                    "source_file": filename,
                    "schema": "BIO",
                    "model_type": f"zeroshot_transfer:{self.transfer_model}",
                    "seed": self.seed,
                    "records": dump_records,
                }, dump_path)
                print(f"Dumped {len(dump_records)} prediction sequences to {dump_path}")

    # -------------------------------------------------------------- evaluate
    def _ensure_model_loaded(self):
        if self.model is not None:
            return True
        out_dir = os.path.join(os.getcwd(), config.INTERIM_DATA, f"transformer_{self.hf_model}")
        if os.path.exists(out_dir):
            from transformers import AutoTokenizer, AutoModelForTokenClassification
            self.tokenizer = AutoTokenizer.from_pretrained(out_dir, use_fast=True)
            self.model = AutoModelForTokenClassification.from_pretrained(out_dir)
            self.model.to(self.device)
            print(f"Loaded fine-tuned transformer from {out_dir}")
            return True
        print(f"No fine-tuned transformer found at {out_dir}. Run train mode first.")
        return False

    def evaluate(self, eval_files=None):
        if not self._ensure_model_loaded():
            return
        from seqeval.metrics import classification_report, f1_score, precision_score, recall_score
        from seqeval.scheme import IOB2

        if self.dump_predictions:
            os.makedirs(self.dump_predictions, exist_ok=True)

        if eval_files is None:
            eval_files = [("testgs42.json", "Gold Standard 42"), ("testgs91.json", "Gold Standard 91")]
        self.model.eval()
        for filename, label in eval_files:
            docs = self._load_docs(filename)
            if not docs:
                print(f"Warning: {filename} not found; skipping.")
                continue
            ds = _TokenClsDataset(docs, self.tokenizer, self.max_length)
            loader = DataLoader(
                ds,
                batch_size=self.batch_size,
                shuffle=False,
                collate_fn=lambda b: _collate(b, self.tokenizer),
            )

            y_true, y_pred, dump_records = [], [], []
            with torch.no_grad():
                for batch, word_ids, words_batch, bios_batch in loader:
                    inputs = {k: v.to(self.device) for k, v in batch.items() if k != "labels"}
                    logits = self.model(**inputs).logits
                    preds = logits.argmax(-1).cpu().tolist()
                    for b in range(len(words_batch)):
                        words = words_batch[b]
                        gold_bio = bios_batch[b]
                        wids = word_ids[b]
                        # Take prediction at the first subword of each word.
                        word_pred = ["O"] * len(words)
                        seen = set()
                        for pos, wid in enumerate(wids):
                            if wid is None or wid < 0 or wid in seen or wid >= len(words):
                                continue
                            seen.add(wid)
                            word_pred[wid] = ID2LABEL.get(preds[b][pos], "O")
                        # Some words may be truncated out; clip gold to evaluated length.
                        eval_len = len(words)
                        gold_seq = gold_bio[:eval_len]
                        pred_seq = word_pred[:eval_len]
                        y_true.append(gold_seq)
                        y_pred.append(pred_seq)
                        if self.dump_predictions:
                            dump_records.append({
                                "tokens": words[:eval_len],
                                "gold": gold_seq,
                                "pred": pred_seq,
                            })

            if not y_true:
                print(f"No samples processed for {label}.")
                continue

            print(f"\nEvaluating on {label} dataset: {filename}")
            print(classification_report(y_true, y_pred, mode="strict", scheme=IOB2, zero_division=0))
            prec = precision_score(y_true, y_pred, mode="strict", scheme=IOB2, zero_division=0) * 100
            rec = recall_score(y_true, y_pred, mode="strict", scheme=IOB2, zero_division=0) * 100
            f1 = f1_score(y_true, y_pred, mode="strict", scheme=IOB2, zero_division=0) * 100
            flat_t = [t for s in y_true for t in s]
            flat_p = [t for s in y_pred for t in s]
            acc = (sum(1 for a, c in zip(flat_t, flat_p) if a == c) / max(1, len(flat_t))) * 100
            print("-" * 65)
            print(f"{'SeqEval Overall':<17} | {'Precision':>9} | {'Recall':>9} | {'F1-Score':>9} | {'Accuracy':>9}")
            print("-" * 65)
            print(f"{'Score (%)':<17} | {prec:>8.2f}% | {rec:>8.2f}% | {f1:>8.2f}% | {acc:>8.2f}%")
            print("-" * 65)

            if self.dump_predictions:
                base_name = filename.split(".")[0]
                dump_path = os.path.join(self.dump_predictions, f"predictions_{base_name}.json")
                save_json({
                    "dataset_label": label,
                    "source_file": filename,
                    "schema": "BIO",
                    "model_type": f"transformer_{self.hf_model}",
                    "seed": self.seed,
                    "records": dump_records,
                }, dump_path)
                print(f"Dumped {len(dump_records)} prediction sequences to {dump_path}")

    # ------------------------------------------------------------------- run
    def run(self):
        mode = self.config.get("mode", "train")
        modes = [m.strip() for m in mode.split(",")]
        for m in modes:
            if m == "train":
                self.train()
            elif m == "inferGS":
                # Zero-shot direct inference: load base encoder (untrained head) then evaluate.
                self.load_base_zero_shot()
                self.evaluate()
            elif m == "transferGS":
                # Zero-shot transfer: pretrained NER head + entity->keyphrase mapping.
                self.load_pretrained_ner_head()
                self.evaluate_transfer()
            elif m == "testGS":
                self.evaluate()
            elif m == "test":
                # In-domain evaluation on the dataset's own held-out test.json.
                self.evaluate(eval_files=[("test.json", "In-Domain Test")])
            else:
                print(f"Unknown transformer mode: {m}")
