# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_pubmedbert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 195 | 15.2% |
| False Negative | 986 | 76.7% |
| Boundary Error | 104 | 8.1% |
| Abbreviation | 50 | 3.9% |
| Nested Phrase | 98 | 7.6% |
| True Positive | 82 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **21.52%**
- Strict entity recall (TP / (TP+FN+boundary)): **7.00%**
- Total predicted spans: 381 · Total gold spans: 1172

## Annotated Examples

### False Positive (195 total)
- spurious pred: `primary care`
- spurious pred: `clinical decision support system`
- spurious pred: `surgery`
- spurious pred: `ontology`
- spurious pred: `surgery`
- spurious pred: `ontology`

### False Negative (986 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (104 total)
- gold: `clinical decision support system cdss` → pred: `clinical decision support system`
- gold: `sharable clinical decision support system` → pred: `clinical decision support`
- gold: `clinical decision support systems cdsss` → pred: `decision support`
- gold: `clinical decision support systems` → pred: `clinical decision support`
- gold: `developing clinical decision support systems` → pred: `clinical decision support systems`
- gold: `workflow model` → pred: `emergency workflow`

### Abbreviation (50 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `cdss`
- missed gold: `cdss`
- missed gold: `cdss`
- missed gold: `sdm`

### Nested Phrase (98 total)
- gold: `clinical decision support system cdss` → pred: `clinical decision support system`
- gold: `sharable clinical decision support system` → pred: `clinical decision support`
- gold: `clinical decision support systems cdsss` → pred: `decision support`
- gold: `clinical decision support systems` → pred: `clinical decision support`
- gold: `developing clinical decision support systems` → pred: `clinical decision support systems`
- gold: `transform architecture` → pred: `transform`
