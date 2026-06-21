# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 67 | 5.4% |
| False Negative | 1154 | 92.6% |
| Boundary Error | 25 | 2.0% |
| Abbreviation | 26 | 2.1% |
| Nested Phrase | 25 | 2.0% |
| True Positive | 1 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **1.08%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.08%**
- Total predicted spans: 93 · Total gold spans: 1180

## Annotated Examples

### False Positive (67 total)
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`

### False Negative (1154 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (25 total)
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `vague knowledge` → pred: `knowledge`
- gold: `fuzzy knowledge layer fuzzy group relation layer fuzzy group domain layer fuzzy personal relation layer` → pred: `knowledge`
- gold: `knowledge construction` → pred: `knowledge`
- gold: `knowledge construction` → pred: `knowledge`

### Abbreviation (26 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `sdm`
- missed gold: `data`
- missed gold: `data`
- missed gold: `data`

### Nested Phrase (25 total)
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `vague knowledge` → pred: `knowledge`
- gold: `fuzzy knowledge layer fuzzy group relation layer fuzzy group domain layer fuzzy personal relation layer` → pred: `knowledge`
- gold: `knowledge construction` → pred: `knowledge`
- gold: `knowledge construction` → pred: `knowledge`
