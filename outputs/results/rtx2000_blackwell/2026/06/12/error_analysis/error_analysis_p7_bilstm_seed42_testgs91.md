# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 958 | 48.3% |
| False Negative | 583 | 29.4% |
| Boundary Error | 441 | 22.3% |
| Abbreviation | 219 | 11.0% |
| Nested Phrase | 445 | 22.5% |
| True Positive | 1549 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **52.54%**
- Strict entity recall (TP / (TP+FN+boundary)): **60.20%**
- Total predicted spans: 2948 · Total gold spans: 2573

## Annotated Examples

### False Positive (958 total)
- spurious pred: `rnn algorithms`
- spurious pred: `model agnostic interpretation`
- spurious pred: `patients`
- spurious pred: `ml`
- spurious pred: `development`
- spurious pred: `development`

### False Negative (583 total)
- missed gold: `findings`
- missed gold: `findings`
- missed gold: `undercontrolled`
- missed gold: `challenges`
- missed gold: `measures`
- missed gold: `interventions`

### Boundary Error (441 total)
- gold: `assessment` → pred: `time assessment`
- gold: `described` → pred: `studies described`
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `impact` → pred: `impact cds`
- gold: `products` → pred: `nice products`

### Abbreviation (219 total)
- spurious pred: `ml`
- spurious pred: `auc`
- spurious pred: `cds`
- spurious pred: `cds`
- spurious pred: `cds`
- spurious pred: `cds`

### Nested Phrase (445 total)
- gold: `assessment` → pred: `time assessment`
- gold: `described` → pred: `studies described`
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `impact` → pred: `impact cds`
- gold: `products` → pred: `nice products`
