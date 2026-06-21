# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 145 | 5.3% |
| False Negative | 2539 | 93.4% |
| Boundary Error | 33 | 1.2% |
| Abbreviation | 38 | 1.4% |
| Nested Phrase | 30 | 1.1% |
| True Positive | 13 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **6.81%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.50%**
- Total predicted spans: 191 · Total gold spans: 2585

## Annotated Examples

### False Positive (145 total)
- spurious pred: `acute kidney injury`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2539 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (33 total)
- gold: `patients attitude` → pred: `attitude`
- gold: `mapping` → pred: `data mapping`
- gold: `alert communication` → pred: `communication`
- gold: `knowledge management` → pred: `knowledge`
- gold: `knowledge management` → pred: `knowledge`
- gold: `knowledge engine` → pred: `engine`

### Abbreviation (38 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (30 total)
- gold: `patients attitude` → pred: `attitude`
- gold: `mapping` → pred: `data mapping`
- gold: `alert communication` → pred: `communication`
- gold: `knowledge management` → pred: `knowledge`
- gold: `knowledge management` → pred: `knowledge`
- gold: `knowledge engine` → pred: `engine`
