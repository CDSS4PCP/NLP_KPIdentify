# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1023 | 48.7% |
| False Negative | 639 | 30.4% |
| Boundary Error | 440 | 20.9% |
| Abbreviation | 141 | 6.7% |
| Nested Phrase | 448 | 21.3% |
| True Positive | 1506 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **50.72%**
- Strict entity recall (TP / (TP+FN+boundary)): **58.26%**
- Total predicted spans: 2969 · Total gold spans: 2585

## Annotated Examples

### False Positive (1023 total)
- spurious pred: `<UNK> algorithms`
- spurious pred: `model`
- spurious pred: `patients`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`

### False Negative (639 total)
- missed gold: `findings`
- missed gold: `described`
- missed gold: `use`
- missed gold: `challenges`
- missed gold: `challenges`
- missed gold: `measures`

### Boundary Error (440 total)
- gold: `continuous prediction model` → pred: `prediction`
- gold: `developed` → pred: `developed model`
- gold: `assessment` → pred: `real time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `data entry <UNK>` → pred: `data entry`
- gold: `products` → pred: `nice products`

### Abbreviation (141 total)
- spurious pred: `auc`
- missed gold: `use`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (448 total)
- gold: `continuous prediction model` → pred: `prediction`
- gold: `developed` → pred: `developed model`
- gold: `assessment` → pred: `real time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `data entry <UNK>` → pred: `data entry`
- gold: `products` → pred: `nice products`
