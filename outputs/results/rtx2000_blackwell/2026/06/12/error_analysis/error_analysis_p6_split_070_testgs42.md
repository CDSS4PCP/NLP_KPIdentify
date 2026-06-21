# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 857 | 59.9% |
| False Negative | 319 | 22.3% |
| Boundary Error | 254 | 17.8% |
| Abbreviation | 144 | 10.1% |
| Nested Phrase | 244 | 17.1% |
| True Positive | 606 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.29%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.40%**
- Total predicted spans: 1717 · Total gold spans: 1179

## Annotated Examples

### False Positive (857 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `drug ordering system`
- spurious pred: `physicians`
- spurious pred: `assistance`
- spurious pred: `patient`

### False Negative (319 total)
- missed gold: `enable`
- missed gold: `operates`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construct`

### Boundary Error (254 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (144 total)
- spurious pred: `asti`
- spurious pred: `asti`
- spurious pred: `jena`
- spurious pred: `jena`
- gold: `jena rules` → pred: `jena`
- spurious pred: `cdss`

### Nested Phrase (244 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
