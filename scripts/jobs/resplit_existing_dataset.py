#!/usr/bin/env python
"""Re-split the existing *labeled* synthetic corpus at a target train fraction.

Used by the Phase 6 split-sensitivity experiment. The canonical `createData`
mode regenerates synthetic labels with the sciSpacy NER model, but that model's
static vectors are broken in the current environment (spaCy E896). Since the
synthetic labels already exist in train.json + test.json, split sensitivity only
needs to re-partition that combined labeled corpus — no re-labeling required.

This mirrors the shuffle/split logic in
`src/nlp/data/dataset.py::generate_synthetic_dataset` (random.Random(seed).shuffle
then a single contiguous cut) so results are consistent with the main pipeline.
"""
import argparse
import json
import os
import random

# Canonical labeled-corpus directory (matches src/core/configV2.py::JSON_DATA).
DEFAULT_JSON_DIR = "data/pubmed_data/json_data_synthetic_labels_v2"


def _load(path):
    with open(path, "r") as fh:
        return json.load(fh)


def _save(obj, path):
    with open(path, "w") as fh:
        json.dump(obj, fh)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trainFraction", type=float, required=True, help="Target train fraction in (0,1)")
    parser.add_argument("--seed", type=int, default=42, help="Shuffle seed (matches pipeline split_seed)")
    parser.add_argument("--jsonDir", type=str, default=DEFAULT_JSON_DIR, help="Directory holding train.json/test.json")
    args = parser.parse_args()

    train_path = os.path.join(args.jsonDir, "train.json")
    test_path = os.path.join(args.jsonDir, "test.json")

    combined = _load(train_path) + _load(test_path)
    total = len(combined)
    if total <= 1:
        raise SystemExit(f"Combined corpus too small to split ({total} docs).")

    fraction = min(max(float(args.trainFraction), 1e-6), 1.0 - 1e-6)
    split_idx = int(round(total * fraction))
    split_idx = max(1, min(total - 1, split_idx))

    shuffled = list(combined)
    random.Random(args.seed).shuffle(shuffled)

    _save(shuffled[:split_idx], train_path)
    _save(shuffled[split_idx:], test_path)
    print(
        f"Re-split labeled corpus: total={total}, train_fraction={fraction:.4f}, "
        f"train_docs={split_idx}, test_docs={total - split_idx}, seed={args.seed}."
    )


if __name__ == "__main__":
    main()
