# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1022 | 51.0% |
| False Negative | 569 | 28.4% |
| Boundary Error | 413 | 20.6% |
| Abbreviation | 129 | 6.4% |
| Nested Phrase | 418 | 20.9% |
| True Positive | 1603 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **52.76%**
- Strict entity recall (TP / (TP+FN+boundary)): **62.01%**
- Total predicted spans: 3038 · Total gold spans: 2585

## Annotated Examples

### False Positive (1022 total)
- spurious pred: `<UNK> algorithms`
- spurious pred: `model`
- spurious pred: `model`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`

### False Negative (569 total)
- missed gold: `models`
- missed gold: `challenges`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`
- missed gold: `interventions`

### Boundary Error (413 total)
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `products` → pred: `nice products`
- gold: `clinical decision support systems <UNK>` → pred: `<UNK>`
- gold: `clinical setting` → pred: `primary care clinical setting`
- gold: `examined prescription drug monitoring` → pred: `examined`

### Abbreviation (129 total)
- spurious pred: `auc`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (418 total)
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `products` → pred: `nice products`
- gold: `clinical decision support systems <UNK>` → pred: `<UNK>`
- gold: `clinical setting` → pred: `primary care clinical setting`
- gold: `examined prescription drug monitoring` → pred: `examined`
