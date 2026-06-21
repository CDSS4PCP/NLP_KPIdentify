# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 131 | 4.8% |
| False Negative | 2545 | 94.2% |
| Boundary Error | 26 | 1.0% |
| Abbreviation | 37 | 1.4% |
| Nested Phrase | 24 | 0.9% |
| True Positive | 14 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **8.19%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.54%**
- Total predicted spans: 171 · Total gold spans: 2585

## Annotated Examples

### False Positive (131 total)
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2545 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (26 total)
- gold: `patients attitude` → pred: `attitude`
- gold: `accessibility usability` → pred: `usability`
- gold: `knowledge engine` → pred: `engine`
- gold: `integration` → pred: `rule engine integration`
- gold: `integrating telehealth` → pred: `telehealth`
- gold: `cancer management` → pred: `bladder cancer`

### Abbreviation (37 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (24 total)
- gold: `patients attitude` → pred: `attitude`
- gold: `accessibility usability` → pred: `usability`
- gold: `knowledge engine` → pred: `engine`
- gold: `integration` → pred: `rule engine integration`
- gold: `integrating telehealth` → pred: `telehealth`
- gold: `stroke care process` → pred: `stroke`
