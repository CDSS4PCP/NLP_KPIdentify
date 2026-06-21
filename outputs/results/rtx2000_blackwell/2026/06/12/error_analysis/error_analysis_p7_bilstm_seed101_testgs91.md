# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: bilstm_crf · seed: 101

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 960 | 48.5% |
| False Negative | 585 | 29.6% |
| Boundary Error | 434 | 21.9% |
| Abbreviation | 213 | 10.8% |
| Nested Phrase | 437 | 22.1% |
| True Positive | 1554 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **52.71%**
- Strict entity recall (TP / (TP+FN+boundary)): **60.40%**
- Total predicted spans: 2948 · Total gold spans: 2573

## Annotated Examples

### False Positive (960 total)
- spurious pred: `rnn algorithms`
- spurious pred: `model agnostic interpretation`
- spurious pred: `patients`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`

### False Negative (585 total)
- missed gold: `findings`
- missed gold: `use`
- missed gold: `settings`
- missed gold: `challenges`
- missed gold: `measures`
- missed gold: `impact`

### Boundary Error (434 total)
- gold: `prediction models` → pred: `prediction models model`
- gold: `assessment` → pred: `time assessment`
- gold: `described` → pred: `studies described`
- gold: `increases` → pred: `cds increases`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`

### Abbreviation (213 total)
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `cds`
- spurious pred: `cds`
- missed gold: `use`
- spurious pred: `cds`

### Nested Phrase (437 total)
- gold: `prediction models` → pred: `prediction models model`
- gold: `assessment` → pred: `time assessment`
- gold: `described` → pred: `studies described`
- gold: `increases` → pred: `cds increases`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
