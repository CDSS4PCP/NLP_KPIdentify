# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 967 | 49.6% |
| False Negative | 543 | 27.9% |
| Boundary Error | 439 | 22.5% |
| Abbreviation | 126 | 6.5% |
| Nested Phrase | 440 | 22.6% |
| True Positive | 1603 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **53.27%**
- Strict entity recall (TP / (TP+FN+boundary)): **62.01%**
- Total predicted spans: 3009 · Total gold spans: 2585

## Annotated Examples

### False Positive (967 total)
- spurious pred: `<UNK> algorithms`
- spurious pred: `<UNK> interpretation`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`
- spurious pred: `<UNK> algorithms`

### False Negative (543 total)
- missed gold: `clinical decision support`
- missed gold: `settings`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`
- missed gold: `interventions`

### Boundary Error (439 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `data entry <UNK>` → pred: `data entry`
- gold: `products` → pred: `nice products`

### Abbreviation (126 total)
- spurious pred: `auc`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (440 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `data entry <UNK>` → pred: `data entry`
- gold: `products` → pred: `nice products`
