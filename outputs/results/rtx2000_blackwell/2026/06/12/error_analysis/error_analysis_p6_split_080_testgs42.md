# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 821 | 58.8% |
| False Negative | 332 | 23.8% |
| Boundary Error | 243 | 17.4% |
| Abbreviation | 132 | 9.5% |
| Nested Phrase | 236 | 16.9% |
| True Positive | 604 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **36.21%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.23%**
- Total predicted spans: 1668 · Total gold spans: 1179

## Annotated Examples

### False Positive (821 total)
- spurious pred: `asti`
- spurious pred: `drug ordering system`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`
- spurious pred: `treatment`

### False Negative (332 total)
- missed gold: `enable`
- missed gold: `operates`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construction`

### Boundary Error (243 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (132 total)
- spurious pred: `asti`
- spurious pred: `asti`
- spurious pred: `jena`
- gold: `jena rules` → pred: `jena`
- spurious pred: `cdss`
- spurious pred: `cdss`

### Nested Phrase (236 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
