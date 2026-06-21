# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BILOU · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1185 | 49.3% |
| False Negative | 692 | 28.8% |
| Boundary Error | 525 | 21.9% |
| Abbreviation | 121 | 5.0% |
| Nested Phrase | 515 | 21.4% |
| True Positive | 1368 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **44.44%**
- Strict entity recall (TP / (TP+FN+boundary)): **52.92%**
- Total predicted spans: 3078 · Total gold spans: 2585

## Annotated Examples

### False Positive (1185 total)
- spurious pred: `aki`
- spurious pred: `<UNK>`
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `hospital aki`
- spurious pred: `<UNK>`

### False Negative (692 total)
- missed gold: `use`
- missed gold: `<UNK>`
- missed gold: `challenges`
- missed gold: `challenges`
- missed gold: `measures`
- missed gold: `improved`

### Boundary Error (525 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network <UNK> -based`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `prediction models` → pred: `prediction models model`

### Abbreviation (121 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (515 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network <UNK> -based`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `prediction models` → pred: `prediction models model`
