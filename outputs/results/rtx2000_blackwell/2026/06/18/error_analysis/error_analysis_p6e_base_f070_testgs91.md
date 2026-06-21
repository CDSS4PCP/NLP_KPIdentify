# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 905 | 46.6% |
| False Negative | 614 | 31.6% |
| Boundary Error | 424 | 21.8% |
| Abbreviation | 107 | 5.5% |
| Nested Phrase | 424 | 21.8% |
| True Positive | 1547 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **53.79%**
- Strict entity recall (TP / (TP+FN+boundary)): **59.85%**
- Total predicted spans: 2876 · Total gold spans: 2585

## Annotated Examples

### False Positive (905 total)
- spurious pred: `<UNK>`
- spurious pred: `<UNK>`
- spurious pred: `patients`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`

### False Negative (614 total)
- missed gold: `clinicians`
- missed gold: `data entry <UNK>`
- missed gold: `measures`
- missed gold: `impact`
- missed gold: `interventions`
- missed gold: `searched`

### Boundary Error (424 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `products` → pred: `nice products`
- gold: `clinicians <UNK>` → pred: `clinicians`
- gold: `investigators followed` → pred: `investigators`

### Abbreviation (107 total)
- spurious pred: `auc`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (424 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `products` → pred: `nice products`
- gold: `clinicians <UNK>` → pred: `clinicians`
- gold: `investigators followed` → pred: `investigators`
