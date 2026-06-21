# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BILOU · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 58 | 4.7% |
| False Negative | 1148 | 93.1% |
| Boundary Error | 27 | 2.2% |
| Abbreviation | 26 | 2.1% |
| Nested Phrase | 27 | 2.2% |
| True Positive | 5 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **5.56%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.42%**
- Total predicted spans: 90 · Total gold spans: 1180

## Annotated Examples

### False Positive (58 total)
- spurious pred: `chronic disease`
- spurious pred: `chronic disease`
- spurious pred: `knowledge translation`
- spurious pred: `knowledge`
- spurious pred: `knowledge`
- spurious pred: `knowledge`

### False Negative (1148 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (27 total)
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

### Nested Phrase (27 total)
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `vague knowledge` → pred: `knowledge`
- gold: `fuzzy knowledge layer fuzzy group relation layer fuzzy group domain layer fuzzy personal relation layer` → pred: `fuzzy knowledge`
- gold: `knowledge construction` → pred: `knowledge`
- gold: `knowledge construction` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`
