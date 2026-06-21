# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 966 | 49.5% |
| False Negative | 563 | 28.8% |
| Boundary Error | 424 | 21.7% |
| Abbreviation | 115 | 5.9% |
| Nested Phrase | 429 | 22.0% |
| True Positive | 1598 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **53.48%**
- Strict entity recall (TP / (TP+FN+boundary)): **61.82%**
- Total predicted spans: 2988 · Total gold spans: 2585

## Annotated Examples

### False Positive (966 total)
- spurious pred: `aki`
- spurious pred: `challenges`
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `model`
- spurious pred: `<UNK> algorithms`

### False Negative (563 total)
- missed gold: `clinical decision support`
- missed gold: `training`
- missed gold: `settings`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`

### Boundary Error (424 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `model interpretations` → pred: `model`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `prediction model`
- gold: `increases` → pred: `<UNK> increases`

### Abbreviation (115 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (429 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `model interpretations` → pred: `model`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `prediction model`
- gold: `increases` → pred: `<UNK> increases`
