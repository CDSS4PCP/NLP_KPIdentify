# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 24 | 2.0% |
| False Negative | 1178 | 97.9% |
| Boundary Error | 1 | 0.1% |
| Abbreviation | 29 | 2.4% |
| Nested Phrase | 1 | 0.1% |
| True Positive | 1 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **3.85%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.08%**
- Total predicted spans: 26 · Total gold spans: 1180

## Annotated Examples

### False Positive (24 total)
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `chronic disease`
- spurious pred: `knowledge engineering`
- spurious pred: `hemodialysis`
- spurious pred: `breast cancer`

### False Negative (1178 total)
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
