# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 777

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 992 | 49.7% |
| False Negative | 564 | 28.3% |
| Boundary Error | 439 | 22.0% |
| Abbreviation | 226 | 11.3% |
| Nested Phrase | 443 | 22.2% |
| True Positive | 1570 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **52.32%**
- Strict entity recall (TP / (TP+FN+boundary)): **61.02%**
- Total predicted spans: 3001 · Total gold spans: 2573

## Annotated Examples

### False Positive (992 total)
- spurious pred: `rnn algorithms`
- spurious pred: `aki`
- spurious pred: `model`
- spurious pred: `plots`
- spurious pred: `patients`
- spurious pred: `aki development`

### False Negative (564 total)
- missed gold: `findings`
- missed gold: `use`
- missed gold: `settings`
- missed gold: `undercontrolled`
- missed gold: `challenges`
- missed gold: `data entry requests`

### Boundary Error (439 total)
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `cds increases`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
- gold: `clinical decision support` → pred: `provide clinical decision support`
- gold: `integrate clinical decision support` → pred: `integrate clinical decision support systems cdsss`

### Abbreviation (226 total)
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `cds`

### Nested Phrase (443 total)
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `cds increases`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
- gold: `clinical decision support` → pred: `provide clinical decision support`
- gold: `integrate clinical decision support` → pred: `integrate clinical decision support systems cdsss`
