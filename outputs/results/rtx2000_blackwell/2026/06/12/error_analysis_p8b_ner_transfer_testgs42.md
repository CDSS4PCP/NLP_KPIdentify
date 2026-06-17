# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: zeroshot_transfer:d4data/biomedical-ner-all · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 632 | 37.5% |
| False Negative | 830 | 49.2% |
| Boundary Error | 225 | 13.3% |
| Abbreviation | 0 | 0.0% |
| Nested Phrase | 221 | 13.1% |
| True Positive | 117 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **12.01%**
- Strict entity recall (TP / (TP+FN+boundary)): **9.98%**
- Total predicted spans: 974 · Total gold spans: 1172

## Annotated Examples

### False Positive (632 total)
- spurious pred: `guideline based drug ordering`
- spurious pred: `primary care`
- spurious pred: `computer based ordering`
- spurious pred: `drug centered checks`
- spurious pred: `treatment`
- spurious pred: `evidence`
- spurious pred: `critic mode`
- spurious pred: `isolated`

### False Negative (830 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`
- missed gold: `prescription errors`
- missed gold: `operates`

### Boundary Error (225 total)
- gold: `triggered` → pred: `triggered elementary rules`
- gold: `clinical decision support system cdss` → pred: `cdss`
- gold: `rules reasoning` → pred: `rules`
- gold: `domain experts` → pred: `domain`
- gold: `sharable clinical decision support system` → pred: `service oriented sharable clinical decision support system`
- gold: `clinical decision support systems cdsss` → pred: `decision support systems cdsss`
- gold: `reasoning` → pred: `ontology reasoning`
- gold: `clinical decision support systems` → pred: `decision support`

### Nested Phrase (221 total)
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `clinical decision support system cdss` → pred: `cdss`
- gold: `rules reasoning` → pred: `rules`
- gold: `domain experts` → pred: `domain`
- gold: `sharable clinical decision support system` → pred: `service oriented sharable clinical decision support system`
- gold: `clinical decision support systems cdsss` → pred: `decision support systems cdsss`
- gold: `reasoning` → pred: `ontology reasoning`
