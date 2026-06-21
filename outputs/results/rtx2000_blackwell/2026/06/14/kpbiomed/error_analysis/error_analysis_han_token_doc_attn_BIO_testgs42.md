# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 34 | 2.8% |
| False Negative | 1177 | 97.0% |
| Boundary Error | 3 | 0.2% |
| Abbreviation | 29 | 2.4% |
| Nested Phrase | 3 | 0.2% |
| True Positive | 0 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **0.00%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.00%**
- Total predicted spans: 37 · Total gold spans: 1180

## Annotated Examples

### False Positive (34 total)
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`

### False Negative (1177 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `<UNK>`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (3 total)
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `surgical training system` → pred: `surgical training`

### Abbreviation (29 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `sdm`
- missed gold: `data`
- missed gold: `data`
- missed gold: `data`

### Nested Phrase (3 total)
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `surgical training system` → pred: `surgical training`
