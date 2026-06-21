# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1251 | 51.2% |
| False Negative | 645 | 26.4% |
| Boundary Error | 547 | 22.4% |
| Abbreviation | 120 | 4.9% |
| Nested Phrase | 528 | 21.6% |
| True Positive | 1393 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **43.65%**
- Strict entity recall (TP / (TP+FN+boundary)): **53.89%**
- Total predicted spans: 3191 · Total gold spans: 2585

## Annotated Examples

### False Positive (1251 total)
- spurious pred: `aki`
- spurious pred: `design`
- spurious pred: `black box`
- spurious pred: `hospital aki`
- spurious pred: `patients`
- spurious pred: `patients`

### False Negative (645 total)
- missed gold: `model interpretations`
- missed gold: `feature modifications`
- missed gold: `use`
- missed gold: `<UNK>`
- missed gold: `challenges`
- missed gold: `measures`

### Boundary Error (547 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `<UNK>`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`

### Abbreviation (120 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (528 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `<UNK>`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
