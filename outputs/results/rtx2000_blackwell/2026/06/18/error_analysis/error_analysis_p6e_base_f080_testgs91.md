# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 915 | 46.5% |
| False Negative | 628 | 31.9% |
| Boundary Error | 424 | 21.6% |
| Abbreviation | 109 | 5.5% |
| Nested Phrase | 427 | 21.7% |
| True Positive | 1533 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **53.38%**
- Strict entity recall (TP / (TP+FN+boundary)): **59.30%**
- Total predicted spans: 2872 · Total gold spans: 2585

## Annotated Examples

### False Positive (915 total)
- spurious pred: `model`
- spurious pred: `patients`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`
- spurious pred: `patients`

### False Negative (628 total)
- missed gold: `training`
- missed gold: `findings`
- missed gold: `described`
- missed gold: `settings`
- missed gold: `data entry <UNK>`
- missed gold: `measures`

### Boundary Error (424 total)
- gold: `prediction models` → pred: `prediction models model`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `challenges` → pred: `<UNK> connectivity challenges`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
- gold: `clinical decision support` → pred: `provide clinical decision support`

### Abbreviation (109 total)
- spurious pred: `auc`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (427 total)
- gold: `prediction models` → pred: `prediction models model`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `challenges` → pred: `<UNK> connectivity challenges`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
- gold: `clinical decision support` → pred: `provide clinical decision support`
