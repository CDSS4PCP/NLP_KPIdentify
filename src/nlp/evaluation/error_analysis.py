"""Systematic error analysis for keyphrase sequence labeling (reviewer concern #4).

Consumes per-document gold/predicted tag dumps produced by
``GNAExperiment.evaluate(... dumpPredictions=<dir>)`` and categorizes entity-level
errors into reviewer-requested buckets:

  * true_positive     - exact span + boundary match
  * false_positive    - predicted span with no gold overlap
  * false_negative    - gold span with no predicted overlap
  * boundary_error    - gold and predicted spans overlap but boundaries differ
  * abbreviation      - error where the span is an abbreviation (all-caps / short)
  * nested_phrase     - error involving spans nested inside a longer span

Counts and percentages reconcile with seqeval precision/recall denominators:
  precision_denom = true_positive + false_positive (+ boundary_error predicted side)
  recall_denom    = true_positive + false_negative (+ boundary_error gold side)

Usage:
    python -m src.nlp.evaluation.error_analysis \
        --predictions outputs/.../predictions_testgs91.json \
        --output_report outputs/.../error_analysis_gs91.md \
        --max_examples 8
"""
import argparse
import json
import os
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

Span = Tuple[int, int]  # (start, end_exclusive)


def _load_dump(path: str) -> dict:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return json.load(f)


def extract_spans(tags: List[str]) -> List[Span]:
    """Extract keyphrase entity spans from a BIO/BILOU/IOBES tag sequence.

    A span starts at any non-O tag that begins an entity (B-, S-, U-, or an I-/E-
    that follows O) and continues while the tag stays non-O. This is intentionally
    schema-agnostic and tolerant of imperfect tag sequences from a CRF decoder.
    """
    spans: List[Span] = []
    start = None
    for i, tag in enumerate(tags):
        is_entity = tag != "O"
        if is_entity and start is None:
            start = i
        elif not is_entity and start is not None:
            spans.append((start, i))
            start = None
    if start is not None:
        spans.append((start, len(tags)))
    return spans


def _overlap(a: Span, b: Span) -> int:
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))


def _is_abbreviation(tokens: List[str], span: Span) -> bool:
    """Heuristic: single-token all-uppercase or short (<=4 char) alpha acronym."""
    words = tokens[span[0]:span[1]]
    if len(words) != 1:
        return False
    w = words[0]
    if not w.isalpha():
        return False
    if w.isupper() and len(w) >= 2:
        return True
    return len(w) <= 4 and w.upper() == w


def _span_text(tokens: List[str], span: Span) -> str:
    return " ".join(tokens[span[0]:span[1]])


def analyze_record(tokens: List[str], gold: List[str], pred: List[str]) -> Dict:
    """Categorize one document's spans into error buckets."""
    gold_spans = extract_spans(gold)
    pred_spans = extract_spans(pred)

    matched_gold = set()
    matched_pred = set()
    result = {
        "true_positive": [],
        "false_positive": [],
        "false_negative": [],
        "boundary_error": [],
        "abbreviation": [],
        "nested_phrase": [],
    }

    # 1. Exact matches (true positives)
    gold_lookup = {s: i for i, s in enumerate(gold_spans)}
    for pj, ps in enumerate(pred_spans):
        if ps in gold_lookup:
            gi = gold_lookup[ps]
            if gi not in matched_gold and pj not in matched_pred:
                matched_gold.add(gi)
                matched_pred.add(pj)
                result["true_positive"].append({"span": _span_text(tokens, ps)})

    # 2. Boundary errors: overlapping but not exact
    for pj, ps in enumerate(pred_spans):
        if pj in matched_pred:
            continue
        best_gi, best_ov = None, 0
        for gi, gs in enumerate(gold_spans):
            if gi in matched_gold:
                continue
            ov = _overlap(ps, gs)
            if ov > best_ov:
                best_ov, best_gi = ov, gi
        if best_gi is not None and best_ov > 0:
            gs = gold_spans[best_gi]
            matched_gold.add(best_gi)
            matched_pred.add(pj)
            entry = {
                "gold": _span_text(tokens, gs),
                "pred": _span_text(tokens, ps),
            }
            result["boundary_error"].append(entry)
            # Nested: one span strictly contains the other
            if (ps[0] >= gs[0] and ps[1] <= gs[1]) or (gs[0] >= ps[0] and gs[1] <= ps[1]):
                result["nested_phrase"].append(entry)
            if _is_abbreviation(tokens, ps) or _is_abbreviation(tokens, gs):
                result["abbreviation"].append(entry)

    # 3. Remaining unmatched predicted spans -> false positives
    for pj, ps in enumerate(pred_spans):
        if pj in matched_pred:
            continue
        entry = {"pred": _span_text(tokens, ps)}
        result["false_positive"].append(entry)
        if _is_abbreviation(tokens, ps):
            result["abbreviation"].append(entry)

    # 4. Remaining unmatched gold spans -> false negatives
    for gi, gs in enumerate(gold_spans):
        if gi in matched_gold:
            continue
        entry = {"gold": _span_text(tokens, gs)}
        result["false_negative"].append(entry)
        if _is_abbreviation(tokens, gs):
            result["abbreviation"].append(entry)
        # Nested miss: gold span sits inside a predicted span
        for ps in pred_spans:
            if gs[0] >= ps[0] and gs[1] <= ps[1] and gs != ps:
                result["nested_phrase"].append(entry)
                break

    return result


def aggregate(dump: dict) -> Tuple[Counter, Dict[str, list]]:
    counts: Counter = Counter()
    examples: Dict[str, list] = defaultdict(list)
    for rec in dump.get("records", []):
        tokens = rec["tokens"]
        gold = rec["gold"]
        pred = rec["pred"]
        cats = analyze_record(tokens, gold, pred)
        for cat, items in cats.items():
            counts[cat] += len(items)
            examples[cat].extend(items)
    return counts, examples


def build_report(dump: dict, counts: Counter, examples: Dict[str, list], max_examples: int) -> str:
    label = dump.get("dataset_label", "Unknown")
    tp = counts["true_positive"]
    fp = counts["false_positive"]
    fn = counts["false_negative"]
    be = counts["boundary_error"]

    # Strict precision/recall denominators (boundary errors count as both wrong-side).
    prec_denom = tp + fp + be
    rec_denom = tp + fn + be
    precision = tp / prec_denom if prec_denom else 0.0
    recall = tp / rec_denom if rec_denom else 0.0

    total_errors = fp + fn + be
    lines = []
    lines.append(f"# Error Analysis — {label}")
    lines.append("")
    lines.append(f"Source: `{dump.get('source_file')}` · schema: {dump.get('schema')} · model: {dump.get('model_type')} · seed: {dump.get('seed')}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Category | Count | % of errors |")
    lines.append("|----------|-------|-------------|")
    for cat in ["false_positive", "false_negative", "boundary_error", "abbreviation", "nested_phrase"]:
        pct = (counts[cat] / total_errors * 100) if total_errors else 0.0
        lines.append(f"| {cat.replace('_', ' ').title()} | {counts[cat]} | {pct:.1f}% |")
    lines.append(f"| True Positive | {tp} | — |")
    lines.append("")
    lines.append(f"- Strict entity precision (TP / (TP+FP+boundary)): **{precision*100:.2f}%**")
    lines.append(f"- Strict entity recall (TP / (TP+FN+boundary)): **{recall*100:.2f}%**")
    lines.append(f"- Total predicted spans: {tp + fp + be} · Total gold spans: {tp + fn + be}")
    lines.append("")
    lines.append("## Annotated Examples")
    for cat in ["false_positive", "false_negative", "boundary_error", "abbreviation", "nested_phrase"]:
        items = examples.get(cat, [])[:max_examples]
        if not items:
            continue
        lines.append("")
        lines.append(f"### {cat.replace('_', ' ').title()} ({counts[cat]} total)")
        for it in items:
            if "gold" in it and "pred" in it:
                lines.append(f"- gold: `{it['gold']}` → pred: `{it['pred']}`")
            elif "gold" in it:
                lines.append(f"- missed gold: `{it['gold']}`")
            else:
                lines.append(f"- spurious pred: `{it['pred']}`")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Entity-level error analysis for keyphrase labeling (reviewer concern #4)")
    parser.add_argument("--predictions", required=True, help="Path to predictions_*.json dumped by evaluate()")
    parser.add_argument("--output_report", default=None, help="Path to write markdown report (default: stdout)")
    parser.add_argument("--max_examples", type=int, default=8, help="Max annotated examples per category")
    args = parser.parse_args()

    dump = _load_dump(args.predictions)
    counts, examples = aggregate(dump)
    report = build_report(dump, counts, examples, args.max_examples)

    if args.output_report:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_report)), exist_ok=True)
        with open(args.output_report, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Error analysis report written to {args.output_report}")
    else:
        print(report)


if __name__ == "__main__":
    main()
