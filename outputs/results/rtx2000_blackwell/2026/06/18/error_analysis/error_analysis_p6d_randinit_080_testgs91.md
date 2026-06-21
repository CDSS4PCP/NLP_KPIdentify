# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 975 | 48.9% |
| False Negative | 574 | 28.8% |
| Boundary Error | 446 | 22.4% |
| Abbreviation | 132 | 6.6% |
| Nested Phrase | 448 | 22.5% |
| True Positive | 1565 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **52.41%**
- Strict entity recall (TP / (TP+FN+boundary)): **60.54%**
- Total predicted spans: 2986 · Total gold spans: 2585

## Annotated Examples

### False Positive (975 total)
- spurious pred: `<UNK>`
- spurious pred: `<UNK>`
- spurious pred: `model <UNK> interpretation`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`

### False Negative (574 total)
- missed gold: `clinical decision support`
- missed gold: `findings`
- missed gold: `described`
- missed gold: `settings`
- missed gold: `<UNK>`
- missed gold: `measures`

### Boundary Error (446 total)
- gold: `assessment` → pred: `real time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `data entry <UNK>` → pred: `data entry`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
- gold: `clinical decision support` → pred: `provide clinical decision support`

### Abbreviation (132 total)
- spurious pred: `auc`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (448 total)
- gold: `assessment` → pred: `real time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `data entry <UNK>` → pred: `data entry`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
- gold: `clinical decision support` → pred: `provide clinical decision support`
