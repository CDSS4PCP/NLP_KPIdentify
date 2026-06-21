# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1221 | 50.6% |
| False Negative | 669 | 27.7% |
| Boundary Error | 525 | 21.7% |
| Abbreviation | 146 | 6.0% |
| Nested Phrase | 512 | 21.2% |
| True Positive | 1391 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **44.34%**
- Strict entity recall (TP / (TP+FN+boundary)): **53.81%**
- Total predicted spans: 3137 · Total gold spans: 2585

## Annotated Examples

### False Positive (1221 total)
- spurious pred: `aki`
- spurious pred: `clinical practice`
- spurious pred: `<UNK>`
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `black`

### False Negative (669 total)
- missed gold: `findings`
- missed gold: `use`
- missed gold: `<UNK>`
- missed gold: `challenges`
- missed gold: `challenges`
- missed gold: `measures`

### Boundary Error (525 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network <UNK>`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model`

### Abbreviation (146 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (512 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `prediction` → pred: `aki prediction`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network <UNK>`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `prediction models` → pred: `prediction models model`
- gold: `external validation` → pred: `internal and external validation`
