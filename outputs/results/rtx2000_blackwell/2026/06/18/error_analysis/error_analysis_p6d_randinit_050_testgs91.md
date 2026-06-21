# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1054 | 49.9% |
| False Negative | 575 | 27.2% |
| Boundary Error | 484 | 22.9% |
| Abbreviation | 140 | 6.6% |
| Nested Phrase | 484 | 22.9% |
| True Positive | 1526 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **49.80%**
- Strict entity recall (TP / (TP+FN+boundary)): **59.03%**
- Total predicted spans: 3064 · Total gold spans: 2585

## Annotated Examples

### False Positive (1054 total)
- spurious pred: `aki`
- spurious pred: `<UNK> algorithms`
- spurious pred: `model`
- spurious pred: `patients`
- spurious pred: `development`
- spurious pred: `development`

### False Negative (575 total)
- missed gold: `findings`
- missed gold: `described`
- missed gold: `use`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`

### Boundary Error (484 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `assessment` → pred: `real time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `<UNK> challenges`

### Abbreviation (140 total)
- spurious pred: `aki`
- spurious pred: `auc`
- missed gold: `use`
- spurious pred: `nice`
- spurious pred: `nice`
- spurious pred: `nice`

### Nested Phrase (484 total)
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `assessment` → pred: `real time assessment`
- gold: `increases` → pred: `<UNK> increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `<UNK> challenges`
