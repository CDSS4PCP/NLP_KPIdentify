# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 129 | 4.8% |
| False Negative | 2542 | 94.2% |
| Boundary Error | 28 | 1.0% |
| Abbreviation | 38 | 1.4% |
| Nested Phrase | 25 | 0.9% |
| True Positive | 15 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **8.72%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.58%**
- Total predicted spans: 172 · Total gold spans: 2585

## Annotated Examples

### False Positive (129 total)
- spurious pred: `acute kidney injury`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`
- spurious pred: `hypertension`

### False Negative (2542 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (28 total)
- gold: `<UNK>` → pred: `<UNK> knowledge`
- gold: `accessibility usability` → pred: `usability`
- gold: `monitoring` → pred: `patient monitoring`
- gold: `knowledge engine` → pred: `engine`
- gold: `integrates workflow` → pred: `workflow`
- gold: `integrating telehealth` → pred: `telehealth`

### Abbreviation (38 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `gaps`
- missed gold: `plan`
- missed gold: `plan`
- missed gold: `used`

### Nested Phrase (25 total)
- gold: `<UNK>` → pred: `<UNK> knowledge`
- gold: `accessibility usability` → pred: `usability`
- gold: `monitoring` → pred: `patient monitoring`
- gold: `knowledge engine` → pred: `engine`
- gold: `integrates workflow` → pred: `workflow`
- gold: `integrating telehealth` → pred: `telehealth`
