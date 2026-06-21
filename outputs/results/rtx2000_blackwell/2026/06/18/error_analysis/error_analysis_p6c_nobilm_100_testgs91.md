# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 961 | 49.4% |
| False Negative | 542 | 27.9% |
| Boundary Error | 441 | 22.7% |
| Abbreviation | 117 | 6.0% |
| Nested Phrase | 443 | 22.8% |
| True Positive | 1602 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **53.33%**
- Strict entity recall (TP / (TP+FN+boundary)): **61.97%**
- Total predicted spans: 3004 · Total gold spans: 2585

## Annotated Examples

### False Positive (961 total)
- spurious pred: `patients`
- spurious pred: `algorithms`
- spurious pred: `interpretation`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`

### False Negative (542 total)
- missed gold: `clinicians`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`
- missed gold: `interventions`
- missed gold: `searched`

### Boundary Error (441 total)
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `data entry <UNK>` → pred: `data entry`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
- gold: `clinical decision support` → pred: `provide clinical decision support`

### Abbreviation (117 total)
- spurious pred: `auc`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (443 total)
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `data entry <UNK>` → pred: `data entry`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
- gold: `clinical decision support` → pred: `provide clinical decision support`
