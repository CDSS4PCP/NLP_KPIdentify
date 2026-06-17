"""HuggingFace transformer token-classification wrapper (reviewer concern #1).

Provides a thin builder around ``AutoModelForTokenClassification`` for biomedical
transformer baselines (PubMedBERT, BioBERT, SciBERT) on the keyphrase BIO task.
Kept separate from the BiLSTM/HAN models so the classical pipeline is untouched.

Default model presets map short names to HF hub identifiers.
"""
from typing import Dict

MODEL_PRESETS: Dict[str, str] = {
    "pubmedbert": "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext",
    "biobert": "dmis-lab/biobert-base-cased-v1.1",
    "scibert": "allenai/scibert_scivocab_uncased",
}

# Fixed BIO label scheme for keyphrase token classification.
LABEL_LIST = ["O", "B-KP", "I-KP"]
LABEL2ID = {l: i for i, l in enumerate(LABEL_LIST)}
ID2LABEL = {i: l for l, i in LABEL2ID.items()}


def resolve_model_name(name_or_path: str) -> str:
    """Map a preset short-name to its HF identifier, or pass through a path/hub id."""
    return MODEL_PRESETS.get(name_or_path.lower(), name_or_path)


def build_token_classifier(name_or_path: str):
    """Load tokenizer + token-classification model for the keyphrase BIO scheme.

    Returns (tokenizer, model). Import of ``transformers`` is deferred so the rest
    of the codebase does not hard-depend on the library being installed.
    """
    from transformers import AutoTokenizer, AutoModelForTokenClassification

    hf_id = resolve_model_name(name_or_path)
    tokenizer = AutoTokenizer.from_pretrained(hf_id, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(
        hf_id,
        num_labels=len(LABEL_LIST),
        id2label=ID2LABEL,
        label2id=LABEL2ID,
    )
    return tokenizer, model
