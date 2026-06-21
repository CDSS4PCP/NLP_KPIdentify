# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 136 | 5.0% |
| False Negative | 2540 | 93.8% |
| Boundary Error | 31 | 1.1% |
| Abbreviation | 37 | 1.4% |
| Nested Phrase | 28 | 1.0% |
| True Positive | 14 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **7.73%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.54%**
- Total predicted spans: 181 · Total gold spans: 2585

## Annotated Examples

### False Positive (136 total)
- spurious pred: `acute kidney injury`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2540 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (31 total)
- gold: `patients attitude` → pred: `attitude`
- gold: `integrating workflow` → pred: `workflow`
- gold: `knowledge engine` → pred: `engine`
- gold: `integrates workflow` → pred: `workflow`
- gold: `integration` → pred: `rule engine integration`
- gold: `integrating telehealth` → pred: `telehealth`

### Abbreviation (37 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (28 total)
- gold: `patients attitude` → pred: `attitude`
- gold: `integrating workflow` → pred: `workflow`
- gold: `knowledge engine` → pred: `engine`
- gold: `integrates workflow` → pred: `workflow`
- gold: `integration` → pred: `rule engine integration`
- gold: `integrating telehealth` → pred: `telehealth`
