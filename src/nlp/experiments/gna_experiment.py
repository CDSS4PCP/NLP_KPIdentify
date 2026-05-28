import os
import torch
import torch.optim as optim
from tqdm import tqdm
import re
from src.nlp.experiments.base import BaseExperiment
from src.nlp.models.bilstm_crf import BiLSTM_CRF
from src.nlp.models.han_crf import HAN_CRF
from src.nlp.utils.io import read_json_array, save_json
from src.nlp.data.preprocessor import TextPreprocessor
from src.nlp.data.dataset import DatasetBuilder
from src.core import configV2 as config
import gensim
from gensim.models import KeyedVectors
import numpy as np
import time
from collections import Counter

class GNAExperiment(BaseExperiment):
    def __init__(self, config):
        super().__init__("GNAExperiment", config)
        self.preprocessor = TextPreprocessor()
        
        device_str = self.config.get("device")
        if device_str:
            self.device = torch.device(device_str)
            print(f"Forcefully using device: {self.device}")
            if device_str == "mps":
                print("WARNING: Apple Silicon MPS is selected. Note that PyTorch native stacked BiLSTMs may suffer from gradient instability and NaN loss on MPS.")
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            print(f"Auto-selected device: {self.device}")

        if self.device.type == "cuda":
            # Favor throughput for fixed-shape sequence workloads on NVIDIA GPUs.
            torch.backends.cudnn.benchmark = True
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            torch.set_float32_matmul_precision("high")
            
        # Dynamically propagate execution device to sub-modules
        from src.nlp.models import language_model
        from src.nlp.models import trainer
        language_model.set_device(self.device)
        trainer.set_device(self.device)
        
        self.model = None

    def prepare_data(self):
        print("Preparing data...")
        WORKING_PATH = os.getcwd()
        json_data_folder = os.path.join(WORKING_PATH, config.JSON_DATA)
        if not os.path.exists(json_data_folder): os.makedirs(json_data_folder)
        interim_data_folder = os.path.join(WORKING_PATH, config.INTERIM_DATA)
        if not os.path.exists(interim_data_folder): os.makedirs(interim_data_folder)

        builder = DatasetBuilder()
        pubmed_data_folder = os.path.join(WORKING_PATH, config.PUBMED_PROCESSED_DATA)
        try:
            fullData = builder.load_pubmed_data(pubmed_data_folder)
        except Exception as e:
            print(f"Warning: failed to load main PubMed source from {pubmed_data_folder}: {e}")
            fullData = []
        
        pubmed_data_folder_gs = os.path.join(WORKING_PATH, config.PUBMED_PROCESSED_DATA_GS)
        try:
            test42Abstracts = builder.load_pubmed_data(pubmed_data_folder_gs)
        except Exception as e:
            print(f"Warning: failed to load GS PubMed source from {pubmed_data_folder_gs}: {e}")
            test42Abstracts = []
        
        misc_path = os.path.join(WORKING_PATH, config.DATA_FOLDER, "ACM_MiscPubMed_Abstracts.json")
        try:
            miscData = read_json_array(misc_path)
        except Exception:
            miscData = []

        combined = fullData + test42Abstracts
        print(
            "Loaded source docs:",
            f"main={len(fullData)}",
            f"gs={len(test42Abstracts)}",
            f"misc={len(miscData)}",
            f"combined={len(combined) + len(miscData)}",
        )
        if len(combined) + len(miscData) < 100:
            print(
                "Warning: very small source corpus detected. If this is unexpected, rerun createData and verify PubMed XML loading warnings."
            )
        if not combined and not miscData:
            print("No data found to prepare!")
            return

        import time
        synth_start = time.time()

        preferred_model = self.config.get("synthModel")
        model_candidates = []
        if preferred_model:
            model_candidates.append(preferred_model)
        model_candidates.extend([
            os.path.join(WORKING_PATH, "outputs", "models", "cdssSciSpacy", "model-best"),
            os.path.join(WORKING_PATH, "cdssSciSpacy", "model-best"),
            "en_core_sci_lg",
            "en_core_web_sm",
        ])

        resolved_model = None
        import spacy
        for candidate in model_candidates:
            if not candidate:
                continue
            try:
                _ = spacy.load(candidate)
                resolved_model = candidate
                break
            except Exception as e:
                print(f"Synthetic model candidate failed: {candidate} ({type(e).__name__}: {e})")

        if not resolved_model:
            print("Warning: No loadable spaCy model found; using en_core_web_sm as last resort.")
            resolved_model = "en_core_web_sm"

        print(f"Synthetic keyword model: {resolved_model}")

        builder.generate_synthetic_dataset(
            combined,
            json_data_folder,
            min_sentences=self.config.get("minSentences", 3),
            filter_kp=self.config.get("filterKP", False),
            model_name=resolved_model,
            additional_data=miscData,
            train_test_split=self.config.get("traintestSplit", 3),
            split_seed=42,
        )
        synth_time = time.time() - synth_start
        print(f"Synthetic labels generation completed in {synth_time:.2f} seconds.")
        
        # Pre-compute TF-IDF and TextRank for any existing testgs JSONs
        print("Checking for existing Gold Standard testsets (testgs42, testgs91) to compute features...")
        from src.nlp.models.tf_idf import tf_idf
        from src.nlp.models.textrank import textrank
        for gs_file in ["testgs42.json", "testgs91.json"]:
            gs_path = os.path.join(json_data_folder, gs_file)
            if os.path.exists(gs_path):
                gs_data = read_json_array(gs_path)
                datas = [d['abstract'].split() + d['title'].split() for d in gs_data]
                tf_idf_res = tf_idf(datas)
                textrank_res = textrank(datas)
                tf_idf_save = {d['id']: tf_idf_res[i] for i, d in enumerate(gs_data)}
                textrank_save = {d['id']: textrank_res[i] for i, d in enumerate(gs_data)}
                base_name = gs_file.split('.')[0]
                save_json(tf_idf_save, os.path.join(json_data_folder, f"{base_name}_tf_idf.json"))
                save_json(textrank_save, os.path.join(json_data_folder, f"{base_name}_textrank.json"))
                print(f"Computed TF-IDF and TextRank for {gs_file}")

        print("Data preparation complete.")

    def build_model(self):
        pass

    def _print_label_diagnostics(self, data, split_name, schema):
        """Summarize keyword match coverage and label balance for a dataset split."""
        from src.nlp.models.preProcessData import mark_keyword_all_sentences
        import spacy

        if not data:
            print(f"Label diagnostics [{split_name}]: no documents")
            return

        nlp = None
        doc_count = 0
        token_count = 0
        kp_count = 0
        keyword_total = 0
        keyword_nonempty = 0
        keyword_matched = 0
        keyword_unmatched = 0
        unmatched_counter = Counter()
        unmatched_reason_counter = Counter()

        for article in data:
            if 'sentences' not in article or not article['sentences']:
                if nlp is None:
                    nlp = spacy.blank("en")
                    nlp.add_pipe('sentencizer')
                text = article.get('title', '') + ' ' + article.get('abstract', '')
                doc = nlp(text)
                article['sentences'] = [[token.text for token in sent] for sent in doc.sents]

            if 'keywords' not in article:
                article['keywords'] = []

            _, labels, _, stats = mark_keyword_all_sentences(
                article['keywords'], article['sentences'], schema=schema, return_stats=True
            )
            flat_labels = [tag for seq in labels for tag in seq]
            token_count += len(flat_labels)
            kp_count += sum(1 for tag in flat_labels if tag != 'O')

            keyword_total += int(stats.get('keyword_total', 0))
            keyword_nonempty += int(stats.get('keyword_nonempty', 0))
            keyword_matched += int(stats.get('keyword_matched', 0))
            keyword_unmatched += int(stats.get('keyword_unmatched', 0))
            unmatched_counter.update(stats.get('unmatched_examples', []))
            unmatched_reason_counter.update(stats.get('unmatched_reasons', {}))
            doc_count += 1

        kp_ratio = (kp_count / token_count) if token_count else 0.0
        match_ratio = (keyword_matched / keyword_nonempty) if keyword_nonempty else 0.0
        top_misses = ', '.join([x for x, _ in unmatched_counter.most_common(5)])

        print(
            f"Label diagnostics [{split_name}] | docs={doc_count} tokens={token_count} "
            f"kp_tokens={kp_count} kp_ratio={kp_ratio:.4f} "
            f"kw_nonempty={keyword_nonempty}/{keyword_total} "
            f"kw_matched={keyword_matched} kw_unmatched={keyword_unmatched} "
            f"match_ratio={match_ratio:.4f}"
        )
        if top_misses:
            print(f"Label diagnostics [{split_name}] top unmatched keywords: {top_misses}")
        if unmatched_reason_counter:
            reason_str = ', '.join(
                [f"{k}={v}" for k, v in unmatched_reason_counter.most_common()]
            )
            print(f"Label diagnostics [{split_name}] unmatched reasons: {reason_str}")

    def _load_gs_training_bundle(self, working_path):
        """Load GS42+GS91 data plus optional feature dictionaries for fine-tuning."""
        json_dir = os.path.join(working_path, config.JSON_DATA)
        gs_data = []
        tf_idf_dict = {}
        textrank_dict = {}

        for base_name in ["testgs42", "testgs91"]:
            ds_path = os.path.join(json_dir, f"{base_name}.json")
            if not os.path.exists(ds_path):
                continue

            try:
                gs_data.extend(read_json_array(ds_path))
            except Exception as e:
                print(f"Warning: could not load {ds_path}: {e}")
                continue

            tf_path = os.path.join(json_dir, f"{base_name}_tf_idf.json")
            tr_path = os.path.join(json_dir, f"{base_name}_textrank.json")
            if os.path.exists(tf_path):
                try:
                    tf_idf_dict.update(read_json_array(tf_path))
                except Exception as e:
                    print(f"Warning: could not load {tf_path}: {e}")
            if os.path.exists(tr_path):
                try:
                    textrank_dict.update(read_json_array(tr_path))
                except Exception as e:
                    print(f"Warning: could not load {tr_path}: {e}")

        return gs_data, tf_idf_dict, textrank_dict

    def train(self):
        print("Training BiLSTM_CRF...")
        total_start = time.time()
        
        WORKING_PATH = os.getcwd()
        
        # Step 1: Load training data
        step1_start = time.time()
        train_path = os.path.join(WORKING_PATH, config.JSON_DATA, "train.json")
        try:
            trainData = read_json_array(train_path)
        except Exception:
            print("No training data found.")
            return

        val_split = float(self.config.get("validationSplit", 0.1))
        valData = []
        if 0.0 < val_split < 0.5 and len(trainData) > 10:
            val_count = max(1, int(round(len(trainData) * val_split)))
            val_count = min(val_count, len(trainData) - 1)
            order = np.random.default_rng(42).permutation(len(trainData)).tolist()
            val_ids = set(order[:val_count])
            valData = [article for idx, article in enumerate(trainData) if idx in val_ids]
            trainData = [article for idx, article in enumerate(trainData) if idx not in val_ids]

        step1_time = time.time() - step1_start
        print(
            f"Step 1: Loaded training data JSON in {step1_time:.4f} seconds "
            f"(train_docs={len(trainData)}, val_docs={len(valData)})."
        )

        # Step 2: Load vocabulary
        step2_start = time.time()
        ix_to_word_path = os.path.join(WORKING_PATH, config.INTERIM_DATA, "int2token.json")
        word_to_ix_path = os.path.join(WORKING_PATH, config.INTERIM_DATA, "token2int.json")
        try:
            ix_to_word = read_json_array(ix_to_word_path)
            word_to_ix = read_json_array(word_to_ix_path)
        except Exception:
            print("Vocabulary mappings not found. Did you run preTrain?")
            return
        step2_time = time.time() - step2_start
        print(f"Step 2: Loaded vocabularies in {step2_time:.4f} seconds (Size: {len(ix_to_word)}).")
            
        # Step 3: Load pretrained embeddings
        step3_start = time.time()
        schema = self.config.get("taggingSchema", "IOBES")
        if schema == "BIO":
            tag_to_ix = {"O" : 0, "B-KP" : 1, "I-KP" : 2, "<START>": 3, "<STOP>": 4}
        elif schema == "BILOU":
            tag_to_ix = {"O" : 0, "U-KP" : 1, "B-KP" : 2, "I-KP" : 3, "L-KP" : 4, "<START>": 5, "<STOP>": 6}
        else:
            tag_to_ix = {"O" : 0, "S-KP" : 1, "B-KP" : 2, "I-KP" : 3, "E-KP" : 4, "<START>": 5, "<STOP>": 6}
        from src.nlp.models.language_model import EmbeddingsReader
        embed_file = os.path.join(WORKING_PATH, config.INTERIM_DATA, "LM_word2vec.bin")
        word_embeddings = None
        has_embd = False
        if os.path.exists(embed_file):
            print("Loading pre-trained Word2Vec embeddings...")
            word_embeddings = EmbeddingsReader.from_binary(
                filename=embed_file,
                vocab=word_to_ix
            )
            has_embd = True
        step3_time = time.time() - step3_start
        if has_embd:
            print(f"Step 3: Loaded pre-trained Word2Vec embeddings in {step3_time:.4f} seconds.")
        else:
            print(f"Step 3: No pre-trained Word2Vec embeddings found (took {step3_time:.4f} seconds).")
            
        # Step 4: Initialize model and load BiLM weights
        step4_start = time.time()
        model_type = self.config.get("model_type", "bilstm_crf")
        if model_type == "han_crf":
            self.model = HAN_CRF(
                vocab_size=len(word_to_ix),
                tag_to_ix=tag_to_ix,
                embedding_dim=300,
                use_pretrained_embd=word_embeddings
            )
        else:
            self.model = BiLSTM_CRF(
                vocab_size=len(word_to_ix),
                tag_to_ix=tag_to_ix,
                embedding_dim=300,
                use_pretrained_embd=word_embeddings
            )
        
        biLM_path = os.path.join(WORKING_PATH, config.INTERIM_DATA, "BiLM.pt")
        has_bilm = False
        if os.path.exists(biLM_path):
            print("Loading pre-trained Bi-Language Model weights...")
            model_stateDict = self.model.state_dict()
            pretrainedLM_stateDict = torch.load(biLM_path, map_location='cpu')
            # filter out unnecessary keys and shape mismatches
            pretrained_dict = {k: v for k, v in pretrainedLM_stateDict.items() if k in model_stateDict and v.size() == model_stateDict[k].size()}
            # overwrite entries in the existing state dict
            model_stateDict.update(pretrained_dict)
            # load the new state dict
            self.model.load_state_dict(model_stateDict)
            has_bilm = True
            
        self.model.to(self.device)
        step4_time = time.time() - step4_start
        print(f"Step 4: Initialized model & routed to device '{self.device}' in {step4_time:.4f} seconds (BiLM weights: {has_bilm}).")
        
        # Step 5: Epoch training loop
        step5_start = time.time()
        epochs = self.config.get("epochs", 20)
        optimizer_name = str(self.config.get("optimizer", "adamw")).lower()
        lr = float(self.config.get("lr", 1e-3))
        if optimizer_name == "sgd":
            optimizer = optim.SGD(self.model.parameters(), lr=lr, weight_decay=1e-4)
        else:
            optimizer = optim.AdamW(self.model.parameters(), lr=lr, weight_decay=1e-4)
        batch_size = self.config.get("batchSize", 64)
        early_stop_patience = int(self.config.get("earlyStopPatience", 4))

        # Surface label-coverage drift early; both models share this labeling path.
        self._print_label_diagnostics(trainData, "train", schema)
        if valData:
            self._print_label_diagnostics(valData, "val", schema)
        
        model_name = f"HAN-CRF_{schema}.pt" if model_type == "han_crf" else f"BiLSTM-CRF_{schema}.pt"
        model_path = os.path.join(WORKING_PATH, config.INTERIM_DATA, model_name)

        epoch_times = []

        # Build all CPU-side batches once so expensive NLP/POS preprocessing is not repeated each epoch.
        data_prep_start = time.time()
        tf_idf_path = os.path.join(WORKING_PATH, config.JSON_DATA, "tf_idf.json")
        textrank_path = os.path.join(WORKING_PATH, config.JSON_DATA, "textrank.json")
        tf_idf_dict = read_json_array(tf_idf_path) if os.path.exists(tf_idf_path) else {}
        textrank_dict = read_json_array(textrank_path) if os.path.exists(textrank_path) else {}
        cached_batches = list(
            self._get_batches(
                trainData,
                word_to_ix,
                tag_to_ix,
                tf_idf_dict,
                textrank_dict,
                batch_size,
                schema=schema,
            )
        )

        cached_val_batches = []
        if valData:
            cached_val_batches = list(
                self._get_batches(
                    valData,
                    word_to_ix,
                    tag_to_ix,
                    tf_idf_dict,
                    textrank_dict,
                    batch_size,
                    schema=schema,
                )
            )

        data_prep_time = time.time() - data_prep_start
        print(
            f"Step 5a: Prepared {len(cached_batches)} train and {len(cached_val_batches)} val CPU batches in {data_prep_time:.2f}s "
            "(cached for all epochs)."
        )

        if not cached_batches:
            print("No trainable batches were generated from train.json.")
            return

        use_amp = self.device.type == "cuda"
        scaler = torch.amp.GradScaler("cuda", enabled=use_amp)
        best_val_loss = float("inf")
        best_epoch = 0
        stale_epochs = 0
        trained_epochs = 0

        for epoch in range(epochs):
            epoch_start = time.time()
            self.model.train()
            total_loss = 0
            batch_count = 0

            # Keep stochasticity while reusing the same preprocessed CPU batch tensors.
            for batch_idx in np.random.permutation(len(cached_batches)):
                inputs, targets, masks, feats_pos, feats_cont = cached_batches[batch_idx]
                inputs = inputs.to(self.device, non_blocking=use_amp)
                targets = targets.to(self.device, non_blocking=use_amp)
                masks = masks.to(self.device, non_blocking=use_amp)
                feats_pos = feats_pos.to(self.device, non_blocking=use_amp)
                feats_cont = feats_cont.to(self.device, non_blocking=use_amp)

                optimizer.zero_grad(set_to_none=True)
                if use_amp:
                    with torch.autocast(device_type="cuda", dtype=torch.float16):
                        loss = self.model.neg_log_likelihood(inputs, targets, masks, feats_pos, feats_cont)
                    scaler.scale(loss).backward()
                    scaler.unscale_(optimizer)
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), 5.0)
                    scaler.step(optimizer)
                    scaler.update()
                else:
                    loss = self.model.neg_log_likelihood(inputs, targets, masks, feats_pos, feats_cont)
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), 5.0)
                    optimizer.step()

                total_loss += float(loss.detach().item())
                batch_count += 1

            if use_amp:
                torch.cuda.synchronize()

            avg_loss = total_loss / max(1, batch_count)

            val_loss_str = "n/a"
            val_loss = None
            if cached_val_batches:
                self.model.eval()
                total_val_loss = 0.0
                val_batches = 0
                with torch.no_grad():
                    for v_inputs, v_targets, v_masks, v_feats_pos, v_feats_cont in cached_val_batches:
                        v_inputs = v_inputs.to(self.device, non_blocking=use_amp)
                        v_targets = v_targets.to(self.device, non_blocking=use_amp)
                        v_masks = v_masks.to(self.device, non_blocking=use_amp)
                        v_feats_pos = v_feats_pos.to(self.device, non_blocking=use_amp)
                        v_feats_cont = v_feats_cont.to(self.device, non_blocking=use_amp)

                        if use_amp:
                            with torch.autocast(device_type="cuda", dtype=torch.float16):
                                v_loss = self.model.neg_log_likelihood(v_inputs, v_targets, v_masks, v_feats_pos, v_feats_cont)
                        else:
                            v_loss = self.model.neg_log_likelihood(v_inputs, v_targets, v_masks, v_feats_pos, v_feats_cont)
                        total_val_loss += float(v_loss.detach().item())
                        val_batches += 1

                val_loss = total_val_loss / max(1, val_batches)
                val_loss_str = f"{val_loss:.4f}"

            epoch_time = time.time() - epoch_start
            epoch_times.append(epoch_time)

            save_ckpt = False
            if val_loss is None:
                save_ckpt = True
            elif val_loss < best_val_loss:
                best_val_loss = val_loss
                best_epoch = epoch + 1
                stale_epochs = 0
                save_ckpt = True
            else:
                stale_epochs += 1

            if save_ckpt:
                torch.save(self.model.state_dict(), model_path)

            ckpt_msg = "Checkpoint Saved" if save_ckpt else "No Save"
            print(
                f"Epoch {epoch+1:2d}/{epochs} | Train Loss: {avg_loss:.4f} | "
                f"Val Loss: {val_loss_str} | Time: {epoch_time:.2f}s | {ckpt_msg}"
            )

            if cached_val_batches and early_stop_patience > 0 and stale_epochs >= early_stop_patience:
                print(
                    f"Early stopping at epoch {epoch+1} after {stale_epochs} non-improving validation epochs "
                    f"(best epoch={best_epoch}, best val loss={best_val_loss:.4f})."
                )
                trained_epochs = epoch + 1
                break
            trained_epochs = epoch + 1

        if cached_val_batches and best_epoch > 0:
            print(f"Best checkpoint selected from epoch {best_epoch} with val loss {best_val_loss:.4f}.")

        gs_finetune_epochs = int(self.config.get("gsFineTuneEpochs", 0))
        if gs_finetune_epochs > 0:
            gs_data, gs_tf_idf_dict, gs_textrank_dict = self._load_gs_training_bundle(WORKING_PATH)
            if len(gs_data) < 8:
                print("GS fine-tuning skipped: insufficient GS data found.")
            else:
                print("Starting optional GS fine-tuning stage...")
                gs_train_frac = float(self.config.get("gsFineTuneTrainFraction", 0.8))
                gs_train_frac = min(0.95, max(0.5, gs_train_frac))
                gs_seed = int(self.config.get("gsFineTuneSeed", 42))

                gs_perm = np.random.default_rng(gs_seed).permutation(len(gs_data)).tolist()
                gs_split = int(round(len(gs_data) * gs_train_frac))
                gs_split = max(1, min(len(gs_data) - 1, gs_split))
                gs_train_ids = set(gs_perm[:gs_split])
                gs_train = [article for idx, article in enumerate(gs_data) if idx in gs_train_ids]
                gs_val = [article for idx, article in enumerate(gs_data) if idx not in gs_train_ids]

                self._print_label_diagnostics(gs_train, "gs_finetune_train", schema)
                self._print_label_diagnostics(gs_val, "gs_finetune_val", schema)

                gs_train_batches = list(
                    self._get_batches(
                        gs_train,
                        word_to_ix,
                        tag_to_ix,
                        gs_tf_idf_dict,
                        gs_textrank_dict,
                        batch_size,
                        schema=schema,
                    )
                )
                gs_val_batches = list(
                    self._get_batches(
                        gs_val,
                        word_to_ix,
                        tag_to_ix,
                        gs_tf_idf_dict,
                        gs_textrank_dict,
                        batch_size,
                        schema=schema,
                    )
                )

                if not gs_train_batches:
                    print("GS fine-tuning skipped: no trainable GS batches were generated.")
                else:
                    gs_lr = float(self.config.get("gsFineTuneLr", 3e-4))
                    gs_optimizer = optim.AdamW(self.model.parameters(), lr=gs_lr, weight_decay=1e-4)
                    gs_best_val_loss = float("inf")
                    gs_best_epoch = 0
                    gs_stale = 0
                    gs_patience = max(1, early_stop_patience)

                    print(
                        f"GS fine-tuning config: epochs={gs_finetune_epochs}, lr={gs_lr}, "
                        f"train_docs={len(gs_train)}, val_docs={len(gs_val)}, patience={gs_patience}"
                    )

                    for gs_epoch in range(gs_finetune_epochs):
                        self.model.train()
                        gs_train_loss = 0.0
                        gs_batches = 0

                        for batch_idx in np.random.permutation(len(gs_train_batches)):
                            g_inputs, g_targets, g_masks, g_feats_pos, g_feats_cont = gs_train_batches[batch_idx]
                            g_inputs = g_inputs.to(self.device, non_blocking=use_amp)
                            g_targets = g_targets.to(self.device, non_blocking=use_amp)
                            g_masks = g_masks.to(self.device, non_blocking=use_amp)
                            g_feats_pos = g_feats_pos.to(self.device, non_blocking=use_amp)
                            g_feats_cont = g_feats_cont.to(self.device, non_blocking=use_amp)

                            gs_optimizer.zero_grad(set_to_none=True)
                            if use_amp:
                                with torch.autocast(device_type="cuda", dtype=torch.float16):
                                    g_loss = self.model.neg_log_likelihood(g_inputs, g_targets, g_masks, g_feats_pos, g_feats_cont)
                                scaler.scale(g_loss).backward()
                                scaler.unscale_(gs_optimizer)
                                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 5.0)
                                scaler.step(gs_optimizer)
                                scaler.update()
                            else:
                                g_loss = self.model.neg_log_likelihood(g_inputs, g_targets, g_masks, g_feats_pos, g_feats_cont)
                                g_loss.backward()
                                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 5.0)
                                gs_optimizer.step()

                            gs_train_loss += float(g_loss.detach().item())
                            gs_batches += 1

                        avg_gs_train_loss = gs_train_loss / max(1, gs_batches)
                        avg_gs_val_loss = None
                        if gs_val_batches:
                            self.model.eval()
                            val_loss_sum = 0.0
                            val_batches = 0
                            with torch.no_grad():
                                for gv_inputs, gv_targets, gv_masks, gv_feats_pos, gv_feats_cont in gs_val_batches:
                                    gv_inputs = gv_inputs.to(self.device, non_blocking=use_amp)
                                    gv_targets = gv_targets.to(self.device, non_blocking=use_amp)
                                    gv_masks = gv_masks.to(self.device, non_blocking=use_amp)
                                    gv_feats_pos = gv_feats_pos.to(self.device, non_blocking=use_amp)
                                    gv_feats_cont = gv_feats_cont.to(self.device, non_blocking=use_amp)
                                    if use_amp:
                                        with torch.autocast(device_type="cuda", dtype=torch.float16):
                                            gv_loss = self.model.neg_log_likelihood(gv_inputs, gv_targets, gv_masks, gv_feats_pos, gv_feats_cont)
                                    else:
                                        gv_loss = self.model.neg_log_likelihood(gv_inputs, gv_targets, gv_masks, gv_feats_pos, gv_feats_cont)
                                    val_loss_sum += float(gv_loss.detach().item())
                                    val_batches += 1
                            avg_gs_val_loss = val_loss_sum / max(1, val_batches)

                        gs_save = False
                        if avg_gs_val_loss is None:
                            gs_save = True
                        elif avg_gs_val_loss < gs_best_val_loss:
                            gs_best_val_loss = avg_gs_val_loss
                            gs_best_epoch = gs_epoch + 1
                            gs_stale = 0
                            gs_save = True
                        else:
                            gs_stale += 1

                        if gs_save:
                            torch.save(self.model.state_dict(), model_path)

                        gs_val_str = "n/a" if avg_gs_val_loss is None else f"{avg_gs_val_loss:.4f}"
                        gs_ckpt = "Checkpoint Saved" if gs_save else "No Save"
                        print(
                            f"GS Epoch {gs_epoch+1:2d}/{gs_finetune_epochs} | Train Loss: {avg_gs_train_loss:.4f} | "
                            f"Val Loss: {gs_val_str} | {gs_ckpt}"
                        )

                        if avg_gs_val_loss is not None and gs_stale >= gs_patience:
                            print(
                                f"GS fine-tuning early stop at epoch {gs_epoch+1} "
                                f"(best epoch={gs_best_epoch}, best val loss={gs_best_val_loss:.4f})."
                            )
                            break

                    if gs_best_epoch > 0:
                        print(
                            f"GS fine-tuning selected checkpoint from epoch {gs_best_epoch} "
                            f"(best val loss={gs_best_val_loss:.4f})."
                        )
            
        step5_time = time.time() - step5_start
        print(
            f"Step 5: Completed {trained_epochs} training epochs in {step5_time:.2f} seconds "
            f"(Avg per epoch: {np.mean(epoch_times):.2f}s; prep: {data_prep_time:.2f}s)."
        )
            
        train_total_time = time.time() - step1_start
        print("\n" + "="*50)
        print(f"TRAIN MODE SUMMARY ({model_type.upper()} on device: {self.device})")
        print(f"Total Train Mode Time: {train_total_time:.2f} seconds")
        print(f"  - Step 1: Loading Data:      {step1_time:.4f}s")
        print(f"  - Step 2: Loading Vocab:     {step2_time:.4f}s")
        print(f"  - Step 3: Embeddings Load:   {step3_time:.4f}s")
        print(f"  - Step 4: Model & Device:    {step4_time:.4f}s")
        print(f"  - Step 5: Epochs Train Loop: {step5_time:.2f}s (Avg: {np.mean(epoch_times):.2f}s/epoch)")
        print("="*50 + "\n")

    def _get_batches(self, data, word_to_ix, tag_to_ix, tf_idf_dict=None, textrank_dict=None, batch_size=64, max_len=128, schema="IOBES"):
        from src.nlp.models.preProcessData import mark_keyword_all_sentences
        from torch.nn.utils.rnn import pad_sequence
        import torch.nn as nn
        import spacy
        import nltk
        enabled_features = set(self.config.get("features", ["CEM", "WFOF", "POS", "LEN", "TI", "TR"]))
        PENN_POS_TAGS = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB']
        POS_TO_IX = {tag: i+1 for i, tag in enumerate(PENN_POS_TAGS)}
        
        nlp = None
        prcd_data = []
        doc_sents = []
        for article in data:
            if 'sentences' not in article or not article['sentences']:
                if nlp is None:
                    nlp = spacy.blank("en")
                    nlp.add_pipe('sentencizer')
                text = article.get('title', '') + ' ' + article.get('abstract', '')
                doc = nlp(text)
                article['sentences'] = [[token.text for token in sent] for sent in doc.sents]
            if 'keywords' not in article:
                article['keywords'] = []
                
            _, labels, sentences = mark_keyword_all_sentences(article['keywords'], article['sentences'], schema=schema)
            
            # WFOF preparation: Need plain text
            plain_text = ' '.join([' '.join(sent) for sent in sentences]).lower().strip()
            wfof_dict = {}
            for word in set(plain_text.split()):
                if len(word) < 2: continue
                item = re.search(re.escape(word), plain_text)
                if item is not None:
                    wfof_dict[word] = item.start() / max(1, len(plain_text))
                    
            article_ti = tf_idf_dict.get(article.get('id', ''), {}) if tf_idf_dict else {}
            article_tr = textrank_dict.get(article.get('id', ''), {}) if textrank_dict else {}

            sent_count = 0
            sent_label_pairs = [(x, y) for x, y in zip(sentences, labels) if len(x) > 3]
            if not sent_label_pairs:
                continue

            if "POS" in enabled_features:
                pos_tagged = nltk.pos_tag_sents([x for x, _ in sent_label_pairs])
            else:
                pos_tagged = [None] * len(sent_label_pairs)

            for (x, y), tagged in zip(sent_label_pairs, pos_tagged):
                if len(x) > 3:
                    if tagged is not None:
                        pos_tags = [POS_TO_IX.get(p, 0) for _, p in tagged]
                    else:
                        pos_tags = [0] * len(x)

                    lens = [len(w) if "LEN" in enabled_features else 0.0 for w in x]
                    wfofs = [wfof_dict.get(w.lower(), 0.0) if "WFOF" in enabled_features else 0.0 for w in x]
                    tis = [article_ti.get(w.lower(), 0.0) if "TI" in enabled_features else 0.0 for w in x]
                    trs = [article_tr.get(w.lower(), 0.0) if "TR" in enabled_features else 0.0 for w in x]
                    prcd_data.append((x, y, pos_tags, lens, wfofs, tis, trs))
                    sent_count += 1
            if sent_count > 0:
                doc_sents.append(sent_count)
                    
        model_type = self.config.get("model_type", "bilstm_crf")
        pos_upsample = int(self.config.get("positiveUpsample", 1))
        if self.config.get("mode") == "train" and pos_upsample > 1 and prcd_data:
            pos_samples = [item for item in prcd_data if any(tag != "O" for tag in item[1])]
            neg_samples = [item for item in prcd_data if all(tag == "O" for tag in item[1])]
            if pos_samples and neg_samples:
                prcd_data = neg_samples + (pos_samples * pos_upsample)
                np.random.shuffle(prcd_data)
        
        if model_type == "han_crf":
            # For HAN_CRF, each document is yielded as a single batch to preserve document context
            prv = 0
            for n in doc_sents:
                data_x, data_y, data_masks = [], [], []
                data_pos, data_cont = [], []
                for x, y, pos, lens, wfofs, tis, trs in prcd_data[prv:prv+n]:
                    idxs = [word_to_ix.get(w, word_to_ix.get('<UNK>', 0)) for w in x[:max_len]]
                    data_masks.append(torch.tensor([1 if idx else 0 for idx in idxs], dtype=torch.long))
                    data_x.append(torch.tensor(idxs, dtype=torch.long))
                    data_y.append(torch.tensor([tag_to_ix.get(t, 0) for t in y[:max_len]], dtype=torch.long))
                    data_pos.append(torch.tensor(pos[:max_len], dtype=torch.long))
                    cont_t = torch.tensor([lens[:max_len], wfofs[:max_len], tis[:max_len], trs[:max_len]], dtype=torch.float).transpose(0, 1)
                    data_cont.append(cont_t)
                    
                prv += n
                if len(data_x) == 0:
                    continue
                    
                data_x[0] = nn.ConstantPad1d((0, max_len - data_x[0].shape[0]), 0)(data_x[0])
                data_y[0] = nn.ConstantPad1d((0, max_len - data_y[0].shape[0]), 0)(data_y[0])
                data_masks[0] = nn.ConstantPad1d((0, max_len - data_masks[0].shape[0]), 0)(data_masks[0])
                data_pos[0] = nn.ConstantPad1d((0, max_len - data_pos[0].shape[0]), 0)(data_pos[0])
                data_cont[0] = nn.ConstantPad2d((0, 0, 0, max_len - data_cont[0].shape[0]), 0)(data_cont[0])
                
                yield (
                    torch.stack(tuple(pad_sequence(data_x, batch_first=True))),
                    torch.stack(tuple(pad_sequence(data_y, batch_first=True))),
                    torch.stack(tuple(pad_sequence(data_masks, batch_first=True))),
                    torch.stack(tuple(pad_sequence(data_pos, batch_first=True))),
                    torch.stack(tuple(pad_sequence(data_cont, batch_first=True)))
                )
        else:
            # For BiLSTM_CRF, we can pack sentences across documents up to batch_size for efficiency
            for n in range(0, len(prcd_data), batch_size):
                data_x, data_y, data_masks = [], [], []
                data_pos, data_cont = [], []
                for x, y, pos, lens, wfofs, tis, trs in prcd_data[n:n+batch_size]:
                    idxs = [word_to_ix.get(w, word_to_ix.get('<UNK>', 0)) for w in x[:max_len]]
                    data_masks.append(torch.tensor([1 if idx else 0 for idx in idxs], dtype=torch.long))
                    data_x.append(torch.tensor(idxs, dtype=torch.long))
                    data_y.append(torch.tensor([tag_to_ix.get(t, 0) for t in y[:max_len]], dtype=torch.long))
                    data_pos.append(torch.tensor(pos[:max_len], dtype=torch.long))
                    cont_t = torch.tensor([lens[:max_len], wfofs[:max_len], tis[:max_len], trs[:max_len]], dtype=torch.float).transpose(0, 1)
                    data_cont.append(cont_t)
                    
                if len(data_x) == 0:
                    continue
                    
                data_x[0] = nn.ConstantPad1d((0, max_len - data_x[0].shape[0]), 0)(data_x[0])
                data_y[0] = nn.ConstantPad1d((0, max_len - data_y[0].shape[0]), 0)(data_y[0])
                data_masks[0] = nn.ConstantPad1d((0, max_len - data_masks[0].shape[0]), 0)(data_masks[0])
                data_pos[0] = nn.ConstantPad1d((0, max_len - data_pos[0].shape[0]), 0)(data_pos[0])
                data_cont[0] = nn.ConstantPad2d((0, 0, 0, max_len - data_cont[0].shape[0]), 0)(data_cont[0])
                
                yield (
                    torch.stack(tuple(pad_sequence(data_x, batch_first=True))),
                    torch.stack(tuple(pad_sequence(data_y, batch_first=True))),
                    torch.stack(tuple(pad_sequence(data_masks, batch_first=True))),
                    torch.stack(tuple(pad_sequence(data_pos, batch_first=True))),
                    torch.stack(tuple(pad_sequence(data_cont, batch_first=True)))
                )

    def evaluate(self):
        print("Evaluating BiLSTM_CRF...")
        eval_total_start = time.time()
        WORKING_PATH = os.getcwd()
        mode = self.config.get("mode", "test")
        
        # Determine which datasets to evaluate
        datasets_to_eval = []
        if mode == "testGS":
            # For testGS, evaluate both gold standard 42 and 91
            for filename, label in [("testgs42.json", "Gold Standard 42"), ("testgs91.json", "Gold Standard 91")]:
                path = os.path.join(WORKING_PATH, config.JSON_DATA, filename)
                if os.path.exists(path):
                    datasets_to_eval.append((path, label))
                else:
                    print(f"Warning: {filename} not found at {path}")
            if not datasets_to_eval:
                # Fallback to testgs.json if neither exists
                test_path = os.path.join(WORKING_PATH, config.JSON_DATA, "testgs.json")
                if os.path.exists(test_path):
                    datasets_to_eval.append((test_path, "Gold Standard"))
        elif mode == "test":
            test_path = os.path.join(WORKING_PATH, config.JSON_DATA, "test.json")
            datasets_to_eval.append((test_path, "Test"))
        else:
            # Predict or default
            test_filename = "testgs.json"
            test_path = os.path.join(WORKING_PATH, config.JSON_DATA, test_filename)
            if not os.path.exists(test_path):
                test_filename = "testgs42.json"
                test_path = os.path.join(WORKING_PATH, config.JSON_DATA, test_filename)
            datasets_to_eval.append((test_path, mode))

        if not datasets_to_eval:
            print("No datasets found to evaluate.")
            return

        # Step 1: Load Vocabulary Mappings
        step1_start = time.time()
        ix_to_word_path = os.path.join(WORKING_PATH, config.INTERIM_DATA, "int2token.json")
        word_to_ix_path = os.path.join(WORKING_PATH, config.INTERIM_DATA, "token2int.json")
        try:
            ix_to_word = read_json_array(ix_to_word_path)
            word_to_ix = read_json_array(word_to_ix_path)
        except Exception:
            print("Vocabulary mappings not found. Did you run preTrain?")
            return
            
        schema = self.config.get("taggingSchema", "IOBES")
        if schema == "BIO":
            tag_to_ix = {"O" : 0, "B-KP" : 1, "I-KP" : 2, "<START>": 3, "<STOP>": 4}
        elif schema == "BILOU":
            tag_to_ix = {"O" : 0, "U-KP" : 1, "B-KP" : 2, "I-KP" : 3, "L-KP" : 4, "<START>": 5, "<STOP>": 6}
        else:
            tag_to_ix = {"O" : 0, "S-KP" : 1, "B-KP" : 2, "I-KP" : 3, "E-KP" : 4, "<START>": 5, "<STOP>": 6}
        ix_to_tag = {v: k for k, v in tag_to_ix.items()}
        step1_time = time.time() - step1_start
        print(f"Step 1: Loaded vocabulary mappings in {step1_time:.4f} seconds.")
        
        # Step 2: Initialize Model and Load weights
        step2_start = time.time()
        model_type = self.config.get("model_type", "bilstm_crf")
        if model_type == "han_crf":
            self.model = HAN_CRF(
                vocab_size=len(word_to_ix),
                tag_to_ix=tag_to_ix,
                embedding_dim=300
            )
        else:
            self.model = BiLSTM_CRF(
                vocab_size=len(word_to_ix),
                tag_to_ix=tag_to_ix,
                embedding_dim=300
            )
        self.model.to(self.device)
        
        model_name = f"HAN-CRF_{schema}.pt" if model_type == "han_crf" else f"BiLSTM-CRF_{schema}.pt"
        model_path = os.path.join(WORKING_PATH, config.INTERIM_DATA, model_name)
        if os.path.exists(model_path):
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device), strict=False)
                print(f"Loaded model weights from {model_path}")
            except RuntimeError as e:
                err = str(e)
                if "size mismatch for word_embeds.weight" in err:
                    print("Checkpoint/vocabulary mismatch detected while loading model weights.")
                    print(err)
                    print("Resolution: regenerate data and checkpoints consistently before testing.")
                    print(
                        "Suggested command: python src/nlp/jobs/gna_pipeline.py "
                        f"--mode createData,preTrain,train,test --model {model_type} --taggingSchema {schema}"
                    )
                    return
                raise
        else:
            print(f"No saved model found at {model_path}. Please run train mode first.")
            return
        self.model.eval()
        step2_time = time.time() - step2_start
        print(f"Step 2: Initialized model & loaded weights on '{self.device}' in {step2_time:.4f} seconds.")

        batch_size = self.config.get("batchSize", 64)
        
        from seqeval.metrics import classification_report, f1_score, recall_score, precision_score
        from seqeval.scheme import IOBES, BILOU, IOB2
        
        seqeval_scheme = IOBES
        if schema == "BIO":
            seqeval_scheme = IOB2
        elif schema == "BILOU":
            seqeval_scheme = BILOU
        
        for test_path, label in datasets_to_eval:
            print(f"\nEvaluating on {label} dataset: {os.path.basename(test_path)}")
            try:
                testData = read_json_array(test_path)
            except Exception as e:
                print(f"Error loading {test_path}: {e}")
                continue

            self._print_label_diagnostics(testData, label.lower().replace(' ', '_'), schema)
                
            # Step 3: Inference predictions loop
            step3_start = time.time()
            y_preds, y_targets = [], []
            
            base_name = os.path.basename(test_path).split('.')[0]
            tf_idf_path = os.path.join(WORKING_PATH, config.JSON_DATA, f"{base_name}_tf_idf.json")
            if not os.path.exists(tf_idf_path) and base_name == "test":
                tf_idf_path = os.path.join(WORKING_PATH, config.JSON_DATA, "tf_idf.json")
            textrank_path = os.path.join(WORKING_PATH, config.JSON_DATA, f"{base_name}_textrank.json")
            if not os.path.exists(textrank_path) and base_name == "test":
                textrank_path = os.path.join(WORKING_PATH, config.JSON_DATA, "textrank.json")
                
            tf_idf_dict = read_json_array(tf_idf_path) if os.path.exists(tf_idf_path) else {}
            textrank_dict = read_json_array(textrank_path) if os.path.exists(textrank_path) else {}
            
            with torch.no_grad():
                for inputs, targets, masks, feats_pos, feats_cont in self._get_batches(testData, word_to_ix, tag_to_ix, tf_idf_dict, textrank_dict, batch_size, schema=schema):
                    inputs, targets, masks = inputs.to(self.device), targets.to(self.device), masks.to(self.device)
                    feats_pos, feats_cont = feats_pos.to(self.device), feats_cont.to(self.device)
                    _, tags = self.model(inputs, masks, feats_pos, feats_cont)
                    
                    for pred, label_tensor, mask in zip(tags, targets, masks):
                        length = int(mask.sum().item())
                        temp_preds = [ix_to_tag.get(i, "O") for i in pred[:length]]
                        temp_targets = [ix_to_tag.get(i, "O") for i in label_tensor.cpu().tolist()[:length]]
                        
                        temp_preds = ["O" if t in ["<START>", "<STOP>"] else t for t in temp_preds]
                        temp_targets = ["O" if t in ["<START>", "<STOP>"] else t for t in temp_targets]
                        
                        y_preds.append(temp_preds)
                        y_targets.append(temp_targets)
            
            step3_time = time.time() - step3_start
            print(f"Step 3: Inference prediction loop completed in {step3_time:.2f} seconds.")

            if len(y_targets) == 0:
                print(f"No samples were successfully processed for {label}.")
                continue
                
            # Step 4: Metric calculations
            step4_start = time.time()
            print(f"Metrics on {label} DS:")
            
            # Token-level metrics and confusion matrix
            from sklearn.metrics import confusion_matrix
            flat_targets = [tag for seq in y_targets for tag in seq]
            flat_preds = [tag for seq in y_preds for tag in seq]

            non_o_pred_count = sum(1 for t in flat_preds if t != "O")
            if non_o_pred_count == 0:
                print("Warning: model predicted only 'O' tags. Strict SeqEval precision/recall/F1 will be 0.00.")
            
            labels_list = ["B-KP", "I-KP", "E-KP", "S-KP", "L-KP", "U-KP", "O"]
            # filter out any labels that are not in our target mapping
            labels_list = [l for l in labels_list if l in tag_to_ix]

            from collections import Counter
            target_counts = Counter(flat_targets)
            pred_counts = Counter(flat_preds)
            print("Label counts (target):", {l: int(target_counts.get(l, 0)) for l in labels_list})
            print("Label counts (pred):  ", {l: int(pred_counts.get(l, 0)) for l in labels_list})
            
            cm = confusion_matrix(flat_targets, flat_preds, labels=labels_list)
            print("Confusion Matrix:")
            print(cm)
            print("Row sums (target support by label order):", cm.sum(axis=1).tolist())
            print("Note: Rows represent Actual/True labels, Columns represent Predicted labels.")
            print(f"Label order: {labels_list}")
            
            precisions = []
            recalls = []
            f1s = []
            accuracies = []
            specificities = []
            
            print("-" * 115)
            print(f"{'Label':<10} | {'TP':>7} | {'FN':>7} | {'FP':>7} | {'TN':>8} | {'Accuracy':>8} | {'Misclass':>8} | {'Prec.':>8} | {'Recall':>8} | {'Spec.':>8} | {'F1':>8}")
            print("-" * 115)
            
            for idx, label_name in enumerate(labels_list):
                tp = cm[idx, idx]
                fn = cm[idx, :].sum() - tp
                fp = cm[:, idx].sum() - tp
                tn = cm.sum() - tp - fn - fp
                
                accuracy = (tp + tn) / (tp + fn + fp + tn) if (tp + fn + fp + tn) > 0 else 0.0
                misclassification = (fp + fn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0.0
                precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
                specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
                f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
                
                precisions.append(precision)
                recalls.append(recall)
                specificities.append(specificity)
                accuracies.append(accuracy)
                f1s.append(f1)
                
                print(f"{label_name:<10} | {tp:>7.1f} | {fn:>7.1f} | {fp:>7.1f} | {tn:>8.1f} | {accuracy:>8.4f} | {misclassification:>8.4f} | {precision:>8.4f} | {recall:>8.4f} | {specificity:>8.4f} | {f1:>8.4f}")
            print("-" * 115)
            print(f"{'Average':<10} | {'-':>7} | {'-':>7} | {'-':>7} | {'-':>8} | {np.mean(accuracies):>8.4f} | {1.0 - np.mean(accuracies):>8.4f} | {np.mean(precisions):>8.4f} | {np.mean(recalls):>8.4f} | {np.mean(specificities):>8.4f} | {np.mean(f1s):>8.4f}")
            print("-" * 115)
            
            print("SeqEval Metrics:")
            print(classification_report(y_targets, y_preds, mode='strict', scheme=seqeval_scheme, zero_division=0))
            seq_prec = precision_score(y_targets, y_preds, mode='strict', scheme=seqeval_scheme, zero_division=0) * 100
            seq_rec = recall_score(y_targets, y_preds, mode='strict', scheme=seqeval_scheme, zero_division=0) * 100
            seq_f1 = f1_score(y_targets, y_preds, mode='strict', scheme=seqeval_scheme, zero_division=0) * 100
            seq_acc = (sum(1 for yt, yp in zip(flat_targets, flat_preds) if yt == yp) / max(1, len(flat_targets))) * 100
            
            print("-" * 65)
            print(f"{'SeqEval Overall':<17} | {'Precision':>9} | {'Recall':>9} | {'F1-Score':>9} | {'Accuracy':>9}")
            print("-" * 65)
            print(f"{'Score (%)':<17} | {seq_prec:>8.2f}% | {seq_rec:>8.2f}% | {seq_f1:>8.2f}% | {seq_acc:>8.2f}%")
            print("-" * 65)
            
            step4_time = time.time() - step4_start
            print(f"Step 4: Metric calculations & reports completed in {step4_time:.4f} seconds.")
            
            ds_total_time = time.time() - step1_start
            print("\n" + "="*50)
            print(f"EVALUATION SUMMARY ON {label.upper()} ({model_type.upper()} on device: {self.device})")
            print(f"Total Dataset Eval Time: {ds_total_time:.2f} seconds")
            print(f"  - Step 1: Loading Vocabs:    {step1_time:.4f}s")
            print(f"  - Step 2: Model Loading:     {step2_time:.4f}s")
            print(f"  - Step 3: Batch Inference:   {step3_time:.2f}s")
            print(f"  - Step 4: Metric Report:     {step4_time:.4f}s")
            print("="*50 + "\n")

    def pre_train(self):
        print("Pre-training language model...")
        pretrain_total_start = time.time()
        WORKING_PATH = os.getcwd()
        
        # Step 1: Load train/test data
        step1_start = time.time()
        train_path = os.path.join(WORKING_PATH, config.JSON_DATA, "train.json")
        test_path = os.path.join(WORKING_PATH, config.JSON_DATA, "test.json")
        
        try:
            trainData = read_json_array(train_path)
            testData = read_json_array(test_path)
        except Exception as e:
            print(f"Could not load train/test json: {e}")
            return
        step1_time = time.time() - step1_start
        print(f"Step 1: Loaded train/test dataset JSON in {step1_time:.4f} seconds.")
            
        # Step 2: Sentence tokenization & corpus extraction
        step2_start = time.time()
        import spacy
        nlp = None
        for data_pool in [trainData, testData]:
            for article in data_pool:
                if 'sentences' not in article or not article['sentences']:
                    if nlp is None:
                        nlp = spacy.blank("en")
                        nlp.add_pipe('sentencizer')
                    text = article.get('title', '') + ' ' + article.get('abstract', '')
                    doc = nlp(text)
                    article['sentences'] = [[token.orth_.lower() for token in sent if not token.is_punct | token.is_space] for sent in doc.sents]
                    
        train_corpus_sentences = []
        for x in trainData:
            train_corpus_sentences.extend(x.get('sentences', []))
        
        test_corpus_sentences = []
        for x in testData:
            test_corpus_sentences.extend(x.get('sentences', []))
            
        total_corpus_sentences = train_corpus_sentences + test_corpus_sentences
        if not total_corpus_sentences:
            print("No sentences found.")
            return
        step2_time = time.time() - step2_start
        print(f"Step 2: Extracted sentences corpus in {step2_time:.4f} seconds (Total sents: {len(total_corpus_sentences)}).")
            
        # Step 3: Train Word2Vec model
        step3_start = time.time()
        print("Training Word2Vec model...")
        w2v_workers = max(1, (os.cpu_count() or 4) - 1)
        modelW2V = gensim.models.Word2Vec(
            sentences=total_corpus_sentences,
            vector_size=300, window=5,
            min_count=0, workers=w2v_workers,
            sg=1, seed=42
        )
        embed_file = os.path.join(WORKING_PATH, config.INTERIM_DATA, "LM_word2vec.bin")
        modelW2V.wv.save_word2vec_format(embed_file, binary=True)
        
        int2token = {0: '<UNK>'}
        cnt = 1
        for word in modelW2V.wv.key_to_index.keys():
            int2token[cnt] = word
            cnt += 1
        token2int = {t: i for i, t in int2token.items()}
        
        save_json(token2int, os.path.join(WORKING_PATH, config.INTERIM_DATA, "token2int.json"))
        save_json(int2token, os.path.join(WORKING_PATH, config.INTERIM_DATA, "int2token.json"))
        step3_time = time.time() - step3_start
        print(
            f"Step 3: Trained and saved Word2Vec embeddings in {step3_time:.4f} seconds "
            f"(Vocab size: {len(int2token)}, CPU workers: {w2v_workers})."
        )

        # Step 4: Split data and generate sequences
        step4_start = time.time()
        print("Training Bi-Directional Language Model...")
        import sys
        sys.path.append(WORKING_PATH)
        from src.nlp.models.language_model import LanguageModel, WordLSTM_v2
        from src.nlp.models.trainer import Trainer
        
        lang_model = LanguageModel(token2int=token2int)

        def splitData_Input_Targets(csLM, corpus_sents, token2int, seqLength=5):
            inputs, targets = [], []
            for sent in corpus_sents:
                seqs = csLM.create_seq(sent, seq_len=seqLength)
                if not isinstance(seqs, list):
                    seqs = [seqs]
                for seq in seqs:
                    if isinstance(seq, list):
                        seqTokens = seq
                    else:
                        seqTokens = seq.split()
                    seqInts = csLM.get_integer_seq(seqTokens, tokenized=True)
                    if len(seqInts) == seqLength + 1:
                        inputs.append(seqInts[:-1])
                        targets.append(seqInts[1:])
            return np.array(inputs, dtype="int32"), np.array(targets, dtype="int32")

        seqLength = self.config.get("seqLength", 5)
        x_train, y_train = splitData_Input_Targets(lang_model, train_corpus_sentences, token2int, seqLength)
        x_test, y_test = splitData_Input_Targets(lang_model, test_corpus_sentences, token2int, seqLength)
        step4_time = time.time() - step4_start
        print(f"Step 4: Generated input/target sequences in {step4_time:.4f} seconds (Train seqs: {len(x_train)}, Test seqs: {len(x_test)}).")

        # Step 5: Pre-train Language Model
        step5_start = time.time()
        biLMNet = WordLSTM_v2(
            n_layers=1,
            bidirection=True,
            pretrainedWE=embed_file,
            vocab=token2int
        )
        biLMNet.to(self.device)

        trainer = Trainer(
            token2int=token2int,
            X_train=x_train,
            y_train=y_train,
            X_test=x_test,
            y_test=y_test
        )

        trainer.train(
            biLMNet,
            batch_size=self.config.get("batchSize", 64),
            epochs=self.config.get("epochs", 20),
            num_workers=self.config.get("numWorkers", None),
        )
        step5_time = time.time() - step5_start
        print(f"Step 5: Completed BiLM neural network training in {step5_time:.2f} seconds.")

        # Step 6: Save BiLM model weights
        step6_start = time.time()
        bilm_weight_path = os.path.join(WORKING_PATH, config.INTERIM_DATA, "BiLM.pt")
        trainer.saveModel(
            biLMNet,
            bilm_weight_path
        )
        step6_time = time.time() - step6_start
        print(f"Step 6: Saved language model checkpoint to {bilm_weight_path} in {step6_time:.4f} seconds.")

        total_time = time.time() - pretrain_total_start
        print("\n" + "="*50)
        print(f"PRE-TRAIN MODE SUMMARY (BiLM on device: {self.device})")
        print(f"Total Pre-Train Mode Time: {total_time:.2f} seconds")
        print(f"  - Step 1: Loading Data:      {step1_time:.4f}s")
        print(f"  - Step 2: Sentences Corpus:  {step2_time:.4f}s")
        print(f"  - Step 3: Word2Vec Training: {step3_time:.4f}s")
        print(f"  - Step 4: Sequence Splitting:{step4_time:.4f}s")
        print(f"  - Step 5: BiLM Training:     {step5_time:.2f}s")
        print(f"  - Step 6: Save Checkpoint:   {step6_time:.4f}s")
        print("="*50 + "\n")


    def run(self):
        mode = self.config.get("mode", "train")
        if mode == "createData":
            print("Running in createData mode...")
            self.prepare_data()
        elif mode == "train":
            print("Running in train mode...")
            if self.config.get("preGenSyntheticData"):
                self.prepare_data()
            self.build_model()
            self.train()
        elif mode in ["test", "testGS", "predict"]:
            print(f"Running in {mode} mode...")
            if self.config.get("preGenSyntheticData"):
                self.prepare_data()
            self.build_model()
            self.evaluate()
        elif mode == "preTrain":
            print("Running in preTrain mode...")
            self.pre_train()
        else:
            print(f"Unknown mode: {mode}")

if __name__ == "__main__":
    pass
