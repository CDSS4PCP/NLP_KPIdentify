# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: bilstm_crf · seed: 13

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 937 | 48.1% |
| False Negative | 574 | 29.5% |
| Boundary Error | 438 | 22.5% |
| Abbreviation | 216 | 11.1% |
| Nested Phrase | 440 | 22.6% |
| True Positive | 1561 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **53.17%**
- Strict entity recall (TP / (TP+FN+boundary)): **60.67%**
- Total predicted spans: 2936 · Total gold spans: 2573

## Annotated Examples

### False Positive (937 total)
- spurious pred: `rnn algorithms`
- spurious pred: `model agnostic interpretation`
- spurious pred: `patients`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`

### False Negative (574 total)
- missed gold: `assessment`
- missed gold: `findings`
- missed gold: `use`
- missed gold: `settings`
- missed gold: `undercontrolled`
- missed gold: `challenges`

### Boundary Error (438 total)
- gold: `increases` → pred: `cds increases`
- gold: `data entry requests` → pred: `integration excessive data entry requests`
- gold: `impact` → pred: `impact cds`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
- gold: `clinical decision support` → pred: `provide clinical decision support`

### Abbreviation (216 total)
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `cds`
- spurious pred: `cds`
- missed gold: `use`
- spurious pred: `cds`

### Nested Phrase (440 total)
- gold: `increases` → pred: `cds increases`
- gold: `data entry requests` → pred: `integration excessive data entry requests`
- missed gold: `integration`
- gold: `impact` → pred: `impact cds`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
