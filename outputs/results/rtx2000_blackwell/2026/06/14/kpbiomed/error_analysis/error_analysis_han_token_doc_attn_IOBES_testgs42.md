# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 10 | 0.8% |
| False Negative | 1179 | 99.1% |
| Boundary Error | 1 | 0.1% |
| Abbreviation | 29 | 2.4% |
| Nested Phrase | 1 | 0.1% |
| True Positive | 0 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **0.00%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.00%**
- Total predicted spans: 11 · Total gold spans: 1180

## Annotated Examples

### False Positive (10 total)
- spurious pred: `breast cancer`
- spurious pred: `breast cancer`
- spurious pred: `breast cancer`
- spurious pred: `breast cancer`
- spurious pred: `ontology`
- spurious pred: `ontology`

### False Negative (1179 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `<UNK>`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (1 total)
- gold: `reasoning` → pred: `semantic reasoning`

### Abbreviation (29 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `sdm`
- missed gold: `data`
- missed gold: `data`
- missed gold: `data`

### Nested Phrase (1 total)
- gold: `reasoning` → pred: `semantic reasoning`
