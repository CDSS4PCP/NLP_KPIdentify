# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 981 | 48.0% |
| False Negative | 631 | 30.9% |
| Boundary Error | 430 | 21.1% |
| Abbreviation | 120 | 5.9% |
| Nested Phrase | 425 | 20.8% |
| True Positive | 1524 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **51.93%**
- Strict entity recall (TP / (TP+FN+boundary)): **58.96%**
- Total predicted spans: 2935 · Total gold spans: 2585

## Annotated Examples

### False Positive (981 total)
- spurious pred: `aki`
- spurious pred: `process`
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `patients`
- spurious pred: `model`

### False Negative (631 total)
- missed gold: `clinical decision support`
- missed gold: `training`
- missed gold: `feature modifications`
- missed gold: `use`
- missed gold: `settings`
- missed gold: `measures`

### Boundary Error (430 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `demographic data laboratory values vital signs` → pred: `laboratory values vital signs`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `aki prediction model`

### Abbreviation (120 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (425 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `demographic data laboratory values vital signs` → pred: `laboratory values vital signs`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `aki prediction model`
