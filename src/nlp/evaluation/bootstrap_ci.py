"""Bootstrap confidence intervals & paired significance testing (reviewer concern #6).

Two capabilities:

1. ``ci``    - 95% bootstrap confidence interval for a single model's entity-level
               F1, resampling GS documents with replacement.
2. ``paired`` - paired bootstrap significance test between two models evaluated on
                the SAME set of documents (shared resampling), reporting the
                proportion of resamples where model A beats model B (and a
                two-sided p-value).

Inputs are prediction dumps from ``GNAExperiment.evaluate(... dumpPredictions=<dir>)``.
Entity-level F1 is computed via seqeval strict matching, aggregated over the
resampled documents.

Usage:
    # Single-model 95% CI
    python -m src.nlp.evaluation.bootstrap_ci ci \
        --predictions outputs/.../predictions_testgs91.json --iters 2000

    # Paired comparison (model A vs model B on the same GS split)
    python -m src.nlp.evaluation.bootstrap_ci paired \
        --predictions_a outputs/.../A/predictions_testgs91.json \
        --predictions_b outputs/.../B/predictions_testgs91.json --iters 2000
"""
import argparse
import json
from typing import List, Tuple

import numpy as np

from seqeval.metrics import f1_score
from seqeval.scheme import IOBES, BILOU, IOB2


def _scheme_for(schema: str):
    schema = (schema or "IOBES").upper()
    if schema == "BIO":
        return IOB2
    if schema == "BILOU":
        return BILOU
    return IOBES


def _load(path: str) -> dict:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return json.load(f)


def _records_to_lists(dump: dict) -> Tuple[List[list], List[list]]:
    golds = [r["gold"] for r in dump.get("records", [])]
    preds = [r["pred"] for r in dump.get("records", [])]
    return golds, preds


def _f1_over(indices, golds, preds, scheme) -> float:
    y_true = [golds[i] for i in indices]
    y_pred = [preds[i] for i in indices]
    return f1_score(y_true, y_pred, mode="strict", scheme=scheme, zero_division=0) * 100


def bootstrap_ci(dump: dict, iters: int, seed: int, alpha: float = 0.05) -> dict:
    scheme = _scheme_for(dump.get("schema"))
    golds, preds = _records_to_lists(dump)
    n = len(golds)
    if n == 0:
        raise ValueError("No records in prediction dump.")
    rng = np.random.default_rng(seed)
    point = _f1_over(range(n), golds, preds, scheme)
    samples = np.empty(iters, dtype=float)
    for b in range(iters):
        idx = rng.integers(0, n, size=n)
        samples[b] = _f1_over(idx, golds, preds, scheme)
    lo = float(np.percentile(samples, 100 * (alpha / 2)))
    hi = float(np.percentile(samples, 100 * (1 - alpha / 2)))
    return {
        "n_docs": n,
        "point_f1": point,
        "mean_f1": float(samples.mean()),
        "std_f1": float(samples.std(ddof=1)),
        "ci_low": lo,
        "ci_high": hi,
        "confidence": 1 - alpha,
        "iters": iters,
    }


def paired_bootstrap(dump_a: dict, dump_b: dict, iters: int, seed: int) -> dict:
    scheme_a = _scheme_for(dump_a.get("schema"))
    scheme_b = _scheme_for(dump_b.get("schema"))
    golds_a, preds_a = _records_to_lists(dump_a)
    golds_b, preds_b = _records_to_lists(dump_b)
    n = len(golds_a)
    if n == 0 or len(golds_b) != n:
        raise ValueError(
            f"Paired test requires equal-length, aligned document dumps (a={n}, b={len(golds_b)})."
        )
    rng = np.random.default_rng(seed)
    point_a = _f1_over(range(n), golds_a, preds_a, scheme_a)
    point_b = _f1_over(range(n), golds_b, preds_b, scheme_b)
    observed_diff = point_a - point_b

    diffs = np.empty(iters, dtype=float)
    a_wins = 0
    for bi in range(iters):
        idx = rng.integers(0, n, size=n)
        fa = _f1_over(idx, golds_a, preds_a, scheme_a)
        fb = _f1_over(idx, golds_b, preds_b, scheme_b)
        diffs[bi] = fa - fb
        if fa > fb:
            a_wins += 1
    # Two-sided p-value: fraction of resamples where the difference flips sign
    # relative to the observed direction (centered on 0).
    centered = diffs - diffs.mean()
    p_value = float(np.mean(np.abs(centered) >= abs(observed_diff))) if observed_diff != 0 else 1.0
    return {
        "n_docs": n,
        "point_f1_a": point_a,
        "point_f1_b": point_b,
        "observed_diff": observed_diff,
        "mean_diff": float(diffs.mean()),
        "diff_ci_low": float(np.percentile(diffs, 2.5)),
        "diff_ci_high": float(np.percentile(diffs, 97.5)),
        "prob_a_better": a_wins / iters,
        "p_value": p_value,
        "iters": iters,
    }


def main():
    parser = argparse.ArgumentParser(description="Bootstrap CI & paired significance for entity F1 (reviewer concern #6)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ci = sub.add_parser("ci", help="95% bootstrap CI for one model")
    p_ci.add_argument("--predictions", required=True)
    p_ci.add_argument("--iters", type=int, default=2000)
    p_ci.add_argument("--seed", type=int, default=42)

    p_pair = sub.add_parser("paired", help="Paired bootstrap significance between two models")
    p_pair.add_argument("--predictions_a", required=True)
    p_pair.add_argument("--predictions_b", required=True)
    p_pair.add_argument("--iters", type=int, default=2000)
    p_pair.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    if args.command == "ci":
        res = bootstrap_ci(_load(args.predictions), args.iters, args.seed)
        print(f"Documents: {res['n_docs']}")
        print(f"Point F1: {res['point_f1']:.2f}%")
        print(f"Bootstrap mean F1: {res['mean_f1']:.2f}% (SD {res['std_f1']:.2f})")
        print(f"{int(res['confidence']*100)}% CI: [{res['ci_low']:.2f}%, {res['ci_high']:.2f}%] over {res['iters']} iters")
    else:
        res = paired_bootstrap(_load(args.predictions_a), _load(args.predictions_b), args.iters, args.seed)
        print(f"Documents: {res['n_docs']}")
        print(f"Model A F1: {res['point_f1_a']:.2f}%  |  Model B F1: {res['point_f1_b']:.2f}%")
        print(f"Observed diff (A-B): {res['observed_diff']:.2f} pp")
        print(f"Diff 95% CI: [{res['diff_ci_low']:.2f}, {res['diff_ci_high']:.2f}] pp")
        print(f"P(A better than B): {res['prob_a_better']*100:.1f}%")
        print(f"Two-sided p-value: {res['p_value']:.4f}")


if __name__ == "__main__":
    main()
