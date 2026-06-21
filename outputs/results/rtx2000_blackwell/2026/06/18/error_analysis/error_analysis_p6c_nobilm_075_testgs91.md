# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 980 | 49.5% |
| False Negative | 568 | 28.7% |
| Boundary Error | 432 | 21.8% |
| Abbreviation | 112 | 5.7% |
| Nested Phrase | 425 | 21.5% |
| True Positive | 1585 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **52.89%**
- Strict entity recall (TP / (TP+FN+boundary)): **61.32%**
- Total predicted spans: 2997 · Total gold spans: 2585

## Annotated Examples

### False Positive (980 total)
- spurious pred: `<UNK> algorithms`
- spurious pred: `model`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`
- spurious pred: `<UNK>`

### False Negative (568 total)
- missed gold: `models`
- missed gold: `findings`
- missed gold: `findings`
- missed gold: `<UNK>`
- missed gold: `data entry <UNK>`
- missed gold: `clinician trust`

### Boundary Error (432 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `assessment` → pred: `real time assessment`
- gold: `described` → pred: `studies described`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`

### Abbreviation (112 total)
- spurious pred: `auc`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (425 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `assessment` → pred: `real time assessment`
- gold: `described` → pred: `studies described`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
