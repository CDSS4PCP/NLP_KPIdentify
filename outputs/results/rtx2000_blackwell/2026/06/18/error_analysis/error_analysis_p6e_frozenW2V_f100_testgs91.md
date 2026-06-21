# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 904 | 47.7% |
| False Negative | 569 | 30.0% |
| Boundary Error | 423 | 22.3% |
| Abbreviation | 113 | 6.0% |
| Nested Phrase | 426 | 22.5% |
| True Positive | 1593 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **54.55%**
- Strict entity recall (TP / (TP+FN+boundary)): **61.62%**
- Total predicted spans: 2920 · Total gold spans: 2585

## Annotated Examples

### False Positive (904 total)
- spurious pred: `<UNK> algorithms`
- spurious pred: `model <UNK>`
- spurious pred: `patients`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`

### False Negative (569 total)
- missed gold: `clinicians`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`
- missed gold: `interventions`
- missed gold: `searched`

### Boundary Error (423 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `data entry <UNK>` → pred: `<UNK>`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`

### Abbreviation (113 total)
- spurious pred: `auc`
- spurious pred: `real`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (426 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `data entry <UNK>` → pred: `<UNK>`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
