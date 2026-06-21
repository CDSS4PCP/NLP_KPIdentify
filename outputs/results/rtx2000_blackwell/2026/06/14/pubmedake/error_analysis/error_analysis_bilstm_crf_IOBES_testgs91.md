# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 108 | 4.0% |
| False Negative | 2550 | 95.1% |
| Boundary Error | 24 | 0.9% |
| Abbreviation | 37 | 1.4% |
| Nested Phrase | 21 | 0.8% |
| True Positive | 11 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **7.69%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.43%**
- Total predicted spans: 143 · Total gold spans: 2585

## Annotated Examples

### False Positive (108 total)
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `blood pressure`

### False Negative (2550 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (24 total)
- gold: `accessibility usability` → pred: `usability`
- gold: `integration` → pred: `rule engine integration`
- gold: `quality` → pred: `quality of care`
- gold: `integrating telehealth` → pred: `telehealth`
- gold: `therapy` → pred: `insulin therapy`
- gold: `care model` → pred: `chronic care`

### Abbreviation (37 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (21 total)
- gold: `accessibility usability` → pred: `usability`
- gold: `integration` → pred: `rule engine integration`
- gold: `quality` → pred: `quality of care`
- gold: `integrating telehealth` → pred: `telehealth`
- gold: `therapy` → pred: `insulin therapy`
- gold: `improving diabetes` → pred: `diabetes`
