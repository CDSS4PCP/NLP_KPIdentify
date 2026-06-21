# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 13

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1008 | 50.7% |
| False Negative | 551 | 27.7% |
| Boundary Error | 429 | 21.6% |
| Abbreviation | 211 | 10.6% |
| Nested Phrase | 433 | 21.8% |
| True Positive | 1593 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **52.57%**
- Strict entity recall (TP / (TP+FN+boundary)): **61.91%**
- Total predicted spans: 3030 · Total gold spans: 2573

## Annotated Examples

### False Positive (1008 total)
- spurious pred: `rnn algorithms`
- spurious pred: `model agnostic interpretation`
- spurious pred: `plots`
- spurious pred: `patients`
- spurious pred: `end stage`
- spurious pred: `development`

### False Negative (551 total)
- missed gold: `findings`
- missed gold: `described`
- missed gold: `undercontrolled`
- missed gold: `challenges`
- missed gold: `measures`
- missed gold: `impact`

### Boundary Error (429 total)
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
- gold: `integrate clinical decision support` → pred: `integrate clinical decision support systems cdsss`
- gold: `hospital information systems hiss` → pred: `hospital information systems`

### Abbreviation (211 total)
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `cds`
- spurious pred: `cds`
- spurious pred: `cds`
- spurious pred: `cds`

### Nested Phrase (433 total)
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
- gold: `integrate clinical decision support` → pred: `integrate clinical decision support systems cdsss`
- gold: `hospital information systems hiss` → pred: `hospital information systems`
