# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 93 | 3.5% |
| False Negative | 2558 | 95.8% |
| Boundary Error | 19 | 0.7% |
| Abbreviation | 37 | 1.4% |
| Nested Phrase | 17 | 0.6% |
| True Positive | 8 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **6.67%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.31%**
- Total predicted spans: 120 · Total gold spans: 2585

## Annotated Examples

### False Positive (93 total)
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2558 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (19 total)
- gold: `patients attitude` → pred: `attitude`
- gold: `integrating telehealth` → pred: `telehealth`
- gold: `cancer management` → pred: `bladder cancer`
- gold: `cancer management` → pred: `bladder cancer`
- gold: `stroke care process` → pred: `stroke`
- gold: `prevention` → pred: `falls prevention`

### Abbreviation (37 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (17 total)
- gold: `patients attitude` → pred: `attitude`
- gold: `integrating telehealth` → pred: `telehealth`
- gold: `stroke care process` → pred: `stroke`
- gold: `prevention` → pred: `falls prevention`
- gold: `knowledge management` → pred: `knowledge`
- gold: `operative knowledge` → pred: `knowledge`
