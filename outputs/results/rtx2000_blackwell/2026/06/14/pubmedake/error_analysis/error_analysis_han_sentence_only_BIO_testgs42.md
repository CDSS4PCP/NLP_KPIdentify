# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 56 | 4.5% |
| False Negative | 1156 | 93.5% |
| Boundary Error | 24 | 1.9% |
| Abbreviation | 26 | 2.1% |
| Nested Phrase | 24 | 1.9% |
| True Positive | 0 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **0.00%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.00%**
- Total predicted spans: 80 · Total gold spans: 1180

## Annotated Examples

### False Positive (56 total)
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `knowledge`
- spurious pred: `knowledge`
- spurious pred: `fuzzy diabetes`

### False Negative (1156 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (24 total)
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `vague knowledge` → pred: `knowledge`
- gold: `fuzzy knowledge layer fuzzy group relation layer fuzzy group domain layer fuzzy personal relation layer` → pred: `fuzzy knowledge`
- gold: `knowledge construction` → pred: `knowledge`
- gold: `knowledge construction` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`

### Abbreviation (26 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `sdm`
- missed gold: `data`
- missed gold: `data`
- missed gold: `data`

### Nested Phrase (24 total)
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `vague knowledge` → pred: `knowledge`
- gold: `fuzzy knowledge layer fuzzy group relation layer fuzzy group domain layer fuzzy personal relation layer` → pred: `fuzzy knowledge`
- gold: `knowledge construction` → pred: `knowledge`
- gold: `knowledge construction` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`
