# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 969 | 49.9% |
| False Negative | 545 | 28.0% |
| Boundary Error | 429 | 22.1% |
| Abbreviation | 219 | 11.3% |
| Nested Phrase | 427 | 22.0% |
| True Positive | 1599 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **53.35%**
- Strict entity recall (TP / (TP+FN+boundary)): **62.15%**
- Total predicted spans: 2997 · Total gold spans: 2573

## Annotated Examples

### False Positive (969 total)
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `rnn algorithms`
- spurious pred: `model agnostic interpretation`
- spurious pred: `development`
- spurious pred: `development`

### False Negative (545 total)
- missed gold: `settings`
- missed gold: `measures`
- missed gold: `deployed`
- missed gold: `impact`
- missed gold: `interventions`
- missed gold: `searched`

### Boundary Error (429 total)
- gold: `assessment` → pred: `real time assessment`
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `cds challenges`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`

### Abbreviation (219 total)
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `cds`
- spurious pred: `cds`

### Nested Phrase (427 total)
- gold: `assessment` → pred: `real time assessment`
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `cds challenges`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
