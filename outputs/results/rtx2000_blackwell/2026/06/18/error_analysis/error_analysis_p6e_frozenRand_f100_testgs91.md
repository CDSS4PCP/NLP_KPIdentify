# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 946 | 49.1% |
| False Negative | 563 | 29.2% |
| Boundary Error | 417 | 21.7% |
| Abbreviation | 118 | 6.1% |
| Nested Phrase | 417 | 21.7% |
| True Positive | 1605 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **54.08%**
- Strict entity recall (TP / (TP+FN+boundary)): **62.09%**
- Total predicted spans: 2968 · Total gold spans: 2585

## Annotated Examples

### False Positive (946 total)
- spurious pred: `<UNK> algorithms`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`
- spurious pred: `clinical decision support`
- spurious pred: `<UNK> systems`

### False Negative (563 total)
- missed gold: `clinicians`
- missed gold: `models`
- missed gold: `model interpretations`
- missed gold: `models`
- missed gold: `settings`
- missed gold: `data entry <UNK>`

### Boundary Error (417 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `developed models` → pred: `developed`
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `products` → pred: `nice products`

### Abbreviation (118 total)
- spurious pred: `auc`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (417 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `developed models` → pred: `developed`
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `products` → pred: `nice products`
