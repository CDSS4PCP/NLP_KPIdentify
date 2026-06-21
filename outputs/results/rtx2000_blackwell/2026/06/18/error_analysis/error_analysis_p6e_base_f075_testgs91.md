# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 962 | 49.2% |
| False Negative | 584 | 29.8% |
| Boundary Error | 411 | 21.0% |
| Abbreviation | 125 | 6.4% |
| Nested Phrase | 417 | 21.3% |
| True Positive | 1590 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **53.66%**
- Strict entity recall (TP / (TP+FN+boundary)): **61.51%**
- Total predicted spans: 2963 · Total gold spans: 2585

## Annotated Examples

### False Positive (962 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `model`
- spurious pred: `<UNK> algorithms`
- spurious pred: `model`

### False Negative (584 total)
- missed gold: `findings`
- missed gold: `settings`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`
- missed gold: `evidence`

### Boundary Error (411 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `developed` → pred: `developed model`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `products` → pred: `nice products`
- gold: `clinicians <UNK>` → pred: `clinicians`

### Abbreviation (125 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (417 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `developed` → pred: `developed model`
- gold: `increases` → pred: `<UNK> increases`
- gold: `challenges` → pred: `<UNK> challenges`
- gold: `products` → pred: `nice products`
- gold: `clinicians <UNK>` → pred: `clinicians`
