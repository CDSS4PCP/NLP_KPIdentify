# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1244 | 50.9% |
| False Negative | 655 | 26.8% |
| Boundary Error | 543 | 22.2% |
| Abbreviation | 126 | 5.2% |
| Nested Phrase | 533 | 21.8% |
| True Positive | 1387 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **43.70%**
- Strict entity recall (TP / (TP+FN+boundary)): **53.66%**
- Total predicted spans: 3174 · Total gold spans: 2585

## Annotated Examples

### False Positive (1244 total)
- spurious pred: `aki`
- spurious pred: `<UNK>`
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `black box`
- spurious pred: `-based`

### False Negative (655 total)
- missed gold: `use`
- missed gold: `<UNK>`
- missed gold: `challenges`
- missed gold: `challenges`
- missed gold: `measures`
- missed gold: `improved`

### Boundary Error (543 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `prediction models` → pred: `prediction models model`

### Abbreviation (126 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (533 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
