# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 101

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1000 | 50.1% |
| False Negative | 552 | 27.7% |
| Boundary Error | 443 | 22.2% |
| Abbreviation | 221 | 11.1% |
| Nested Phrase | 444 | 22.3% |
| True Positive | 1578 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **52.23%**
- Strict entity recall (TP / (TP+FN+boundary)): **61.33%**
- Total predicted spans: 3021 · Total gold spans: 2573

## Annotated Examples

### False Positive (1000 total)
- spurious pred: `patients`
- spurious pred: `model`
- spurious pred: `rnn algorithms`
- spurious pred: `model`
- spurious pred: `aki`
- spurious pred: `model agnostic interpretation`

### False Negative (552 total)
- missed gold: `findings`
- missed gold: `data entry requests`
- missed gold: `measures`
- missed gold: `impact`
- missed gold: `interventions`
- missed gold: `accuracy`

### Boundary Error (443 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `described` → pred: `studies described`
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `cds challenges`
- gold: `products` → pred: `nice products`

### Abbreviation (221 total)
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `cds`
- spurious pred: `cds`
- spurious pred: `cds`

### Nested Phrase (444 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `described` → pred: `studies described`
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `cds challenges`
- gold: `products` → pred: `nice products`
