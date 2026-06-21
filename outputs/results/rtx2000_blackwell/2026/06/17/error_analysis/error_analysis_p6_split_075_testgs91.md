# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 968 | 47.9% |
| False Negative | 601 | 29.8% |
| Boundary Error | 450 | 22.3% |
| Abbreviation | 128 | 6.3% |
| Nested Phrase | 450 | 22.3% |
| True Positive | 1534 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **51.96%**
- Strict entity recall (TP / (TP+FN+boundary)): **59.34%**
- Total predicted spans: 2952 · Total gold spans: 2585

## Annotated Examples

### False Positive (968 total)
- spurious pred: `<UNK> algorithms`
- spurious pred: `<UNK>`
- spurious pred: `model`
- spurious pred: `patients`
- spurious pred: `development`
- spurious pred: `development`

### False Negative (601 total)
- missed gold: `training`
- missed gold: `findings`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`
- missed gold: `interventions`

### Boundary Error (450 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `described` → pred: `studies described`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `products` → pred: `nice products`

### Abbreviation (128 total)
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (450 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `described` → pred: `studies described`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `products` → pred: `nice products`
