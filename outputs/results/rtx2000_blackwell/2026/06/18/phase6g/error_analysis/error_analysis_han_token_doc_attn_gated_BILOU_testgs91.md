# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BILOU · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1066 | 46.0% |
| False Negative | 749 | 32.3% |
| Boundary Error | 503 | 21.7% |
| Abbreviation | 127 | 5.5% |
| Nested Phrase | 493 | 21.3% |
| True Positive | 1333 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **45.93%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.57%**
- Total predicted spans: 2902 · Total gold spans: 2585

## Annotated Examples

### False Positive (1066 total)
- spurious pred: `aki`
- spurious pred: `<UNK>`
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `black box`
- spurious pred: `aki`

### False Negative (749 total)
- missed gold: `measures`
- missed gold: `feature modifications`
- missed gold: `described`
- missed gold: `use`
- missed gold: `<UNK>`
- missed gold: `integration`

### Boundary Error (503 total)
- gold: `clinicians` → pred: `clinicians effective measures`
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`

### Abbreviation (127 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (493 total)
- gold: `clinicians` → pred: `clinicians effective measures`
- gold: `prediction` → pred: `aki prediction`
- missed gold: `measures`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`
