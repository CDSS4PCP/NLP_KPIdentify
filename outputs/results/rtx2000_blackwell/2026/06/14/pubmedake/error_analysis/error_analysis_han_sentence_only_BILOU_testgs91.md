# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BILOU · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 121 | 4.5% |
| False Negative | 2547 | 94.5% |
| Boundary Error | 28 | 1.0% |
| Abbreviation | 38 | 1.4% |
| Nested Phrase | 25 | 0.9% |
| True Positive | 10 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **6.29%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.39%**
- Total predicted spans: 159 · Total gold spans: 2585

## Annotated Examples

### False Positive (121 total)
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2547 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (28 total)
- gold: `knowledge engine` → pred: `engine`
- gold: `integration` → pred: `rule engine integration`
- gold: `integrating telehealth` → pred: `telehealth`
- gold: `process mining` → pred: `mining`
- gold: `process mining` → pred: `mining`
- gold: `cancer management` → pred: `bladder cancer`

### Abbreviation (38 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (25 total)
- gold: `knowledge engine` → pred: `engine`
- gold: `integration` → pred: `rule engine integration`
- gold: `integrating telehealth` → pred: `telehealth`
- gold: `process mining` → pred: `mining`
- gold: `process mining` → pred: `mining`
- gold: `models` → pred: `surgical models`
