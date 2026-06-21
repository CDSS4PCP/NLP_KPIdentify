# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 953 | 48.1% |
| False Negative | 587 | 29.6% |
| Boundary Error | 440 | 22.2% |
| Abbreviation | 222 | 11.2% |
| Nested Phrase | 442 | 22.3% |
| True Positive | 1546 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **52.60%**
- Strict entity recall (TP / (TP+FN+boundary)): **60.09%**
- Total predicted spans: 2939 · Total gold spans: 2573

## Annotated Examples

### False Positive (953 total)
- spurious pred: `rnn algorithms`
- spurious pred: `model`
- spurious pred: `patients`
- spurious pred: `end stage`
- spurious pred: `development`
- spurious pred: `development`

### False Negative (587 total)
- missed gold: `models`
- missed gold: `findings`
- missed gold: `use`
- missed gold: `undercontrolled`
- missed gold: `challenges`
- missed gold: `data entry requests`

### Boundary Error (440 total)
- gold: `described` → pred: `studies described`
- gold: `increases` → pred: `cds increases`
- gold: `challenges` → pred: `connectivity challenges`
- gold: `clinician trust` → pred: `clinician`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`

### Abbreviation (222 total)
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `cds`
- missed gold: `use`
- spurious pred: `cds`

### Nested Phrase (442 total)
- gold: `described` → pred: `studies described`
- gold: `increases` → pred: `cds increases`
- gold: `challenges` → pred: `connectivity challenges`
- gold: `clinician trust` → pred: `clinician`
- gold: `products` → pred: `nice products`
- gold: `incorporated evidence` → pred: `evidence`
