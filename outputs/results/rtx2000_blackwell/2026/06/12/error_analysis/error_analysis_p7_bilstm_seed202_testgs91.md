# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: bilstm_crf · seed: 202

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 984 | 49.2% |
| False Negative | 582 | 29.1% |
| Boundary Error | 435 | 21.7% |
| Abbreviation | 221 | 11.0% |
| Nested Phrase | 433 | 21.6% |
| True Positive | 1556 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **52.30%**
- Strict entity recall (TP / (TP+FN+boundary)): **60.47%**
- Total predicted spans: 2975 · Total gold spans: 2573

## Annotated Examples

### False Positive (984 total)
- spurious pred: `aki`
- spurious pred: `rnn algorithms`
- spurious pred: `model agnostic interpretation`
- spurious pred: `patients`
- spurious pred: `development`
- spurious pred: `development`

### False Negative (582 total)
- missed gold: `findings`
- missed gold: `use`
- missed gold: `settings`
- missed gold: `undercontrolled`
- missed gold: `challenges`
- missed gold: `usability`

### Boundary Error (435 total)
- gold: `continuous prediction model` → pred: `continuous prediction`
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`

### Abbreviation (221 total)
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `cds`
- spurious pred: `cds`

### Nested Phrase (433 total)
- gold: `continuous prediction model` → pred: `continuous prediction`
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
