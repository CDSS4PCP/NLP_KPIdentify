# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 904 | 46.5% |
| False Negative | 621 | 31.9% |
| Boundary Error | 421 | 21.6% |
| Abbreviation | 116 | 6.0% |
| Nested Phrase | 419 | 21.5% |
| True Positive | 1543 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **53.80%**
- Strict entity recall (TP / (TP+FN+boundary)): **59.69%**
- Total predicted spans: 2868 · Total gold spans: 2585

## Annotated Examples

### False Positive (904 total)
- spurious pred: `<UNK> algorithms`
- spurious pred: `model`
- spurious pred: `end stage kidney disease`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`

### False Negative (621 total)
- missed gold: `findings`
- missed gold: `settings`
- missed gold: `<UNK>`
- missed gold: `challenges`
- missed gold: `data entry <UNK>`
- missed gold: `challenges`

### Boundary Error (421 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `assessment` → pred: `time assessment`
- gold: `described` → pred: `studies described`
- gold: `increases` → pred: `<UNK> increases`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`

### Abbreviation (116 total)
- spurious pred: `auc`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (419 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `assessment` → pred: `time assessment`
- gold: `described` → pred: `studies described`
- gold: `increases` → pred: `<UNK> increases`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
