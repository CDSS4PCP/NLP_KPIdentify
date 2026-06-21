# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1066 | 48.8% |
| False Negative | 646 | 29.6% |
| Boundary Error | 474 | 21.7% |
| Abbreviation | 100 | 4.6% |
| Nested Phrase | 482 | 22.0% |
| True Positive | 1465 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **48.75%**
- Strict entity recall (TP / (TP+FN+boundary)): **56.67%**
- Total predicted spans: 3005 · Total gold spans: 2585

## Annotated Examples

### False Positive (1066 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `patients`
- spurious pred: `model`
- spurious pred: `algorithms`

### False Negative (646 total)
- missed gold: `feature modifications`
- missed gold: `use`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`
- missed gold: `<UNK>`

### Boundary Error (474 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `models` → pred: `neural network models`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `aki prediction model`
- gold: `assessment` → pred: `time assessment`

### Abbreviation (100 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (482 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `models` → pred: `neural network models`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `aki prediction model`
- gold: `assessment` → pred: `time assessment`
