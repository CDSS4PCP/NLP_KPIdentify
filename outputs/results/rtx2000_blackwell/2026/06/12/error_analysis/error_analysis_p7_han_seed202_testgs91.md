# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 202

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1036 | 51.4% |
| False Negative | 527 | 26.2% |
| Boundary Error | 452 | 22.4% |
| Abbreviation | 217 | 10.8% |
| Nested Phrase | 456 | 22.6% |
| True Positive | 1594 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **51.72%**
- Strict entity recall (TP / (TP+FN+boundary)): **61.95%**
- Total predicted spans: 3082 · Total gold spans: 2573

## Annotated Examples

### False Positive (1036 total)
- spurious pred: `patients`
- spurious pred: `rnn algorithms`
- spurious pred: `aki`
- spurious pred: `model`
- spurious pred: `interpretation`
- spurious pred: `patients`

### False Negative (527 total)
- missed gold: `findings`
- missed gold: `use`
- missed gold: `undercontrolled`
- missed gold: `challenges`
- missed gold: `data entry requests`
- missed gold: `measures`

### Boundary Error (452 total)
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `wireless connectivity challenges`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
- gold: `clinical decision support` → pred: `provide clinical decision support`

### Abbreviation (217 total)
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `cds`
- spurious pred: `cds`
- missed gold: `use`

### Nested Phrase (456 total)
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `wireless connectivity challenges`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
- gold: `clinical decision support` → pred: `provide clinical decision support`
