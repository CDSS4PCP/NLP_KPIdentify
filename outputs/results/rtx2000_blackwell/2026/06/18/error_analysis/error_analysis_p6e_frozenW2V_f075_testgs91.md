# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 905 | 46.8% |
| False Negative | 595 | 30.8% |
| Boundary Error | 433 | 22.4% |
| Abbreviation | 111 | 5.7% |
| Nested Phrase | 427 | 22.1% |
| True Positive | 1557 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **53.78%**
- Strict entity recall (TP / (TP+FN+boundary)): **60.23%**
- Total predicted spans: 2895 · Total gold spans: 2585

## Annotated Examples

### False Positive (905 total)
- spurious pred: `patients`
- spurious pred: `korea seoul national university <UNK> hospital`
- spurious pred: `patients`
- spurious pred: `model`
- spurious pred: `<UNK>`
- spurious pred: `model`

### False Negative (595 total)
- missed gold: `clinical decision support`
- missed gold: `findings`
- missed gold: `described`
- missed gold: `use`
- missed gold: `settings`
- missed gold: `challenges`

### Boundary Error (433 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `prediction models` → pred: `prediction models model`
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `data entry <UNK>` → pred: `<UNK>`
- gold: `products` → pred: `nice products`

### Abbreviation (111 total)
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- missed gold: `use`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (427 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `prediction models` → pred: `prediction models model`
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `data entry <UNK>` → pred: `<UNK>`
- gold: `products` → pred: `nice products`
