# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 940 | 48.3% |
| False Negative | 611 | 31.4% |
| Boundary Error | 395 | 20.3% |
| Abbreviation | 106 | 5.4% |
| Nested Phrase | 390 | 20.0% |
| True Positive | 1579 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **54.19%**
- Strict entity recall (TP / (TP+FN+boundary)): **61.08%**
- Total predicted spans: 2914 · Total gold spans: 2585

## Annotated Examples

### False Positive (940 total)
- spurious pred: `<UNK>`
- spurious pred: `model <UNK>`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`
- spurious pred: `model`

### False Negative (611 total)
- missed gold: `settings`
- missed gold: `data entry <UNK>`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`
- missed gold: `evidence`

### Boundary Error (395 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `products` → pred: `nice products`
- gold: `clinical decision support systems <UNK>` → pred: `<UNK>`
- gold: `clinicians <UNK>` → pred: `clinicians`

### Abbreviation (106 total)
- spurious pred: `auc`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (390 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `products` → pred: `nice products`
- gold: `clinical decision support systems <UNK>` → pred: `<UNK>`
- gold: `clinicians <UNK>` → pred: `clinicians`
