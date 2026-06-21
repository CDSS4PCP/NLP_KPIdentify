# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1061 | 46.0% |
| False Negative | 746 | 32.4% |
| Boundary Error | 498 | 21.6% |
| Abbreviation | 131 | 5.7% |
| Nested Phrase | 487 | 21.1% |
| True Positive | 1341 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **46.24%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.88%**
- Total predicted spans: 2900 · Total gold spans: 2585

## Annotated Examples

### False Positive (1061 total)
- spurious pred: `aki`
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `black box`
- spurious pred: `hospital aki`
- spurious pred: `vital signs`

### False Negative (746 total)
- missed gold: `measures`
- missed gold: `model interpretations`
- missed gold: `described`
- missed gold: `use`
- missed gold: `<UNK>`
- missed gold: `integration`

### Boundary Error (498 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `clinicians` → pred: `clinicians effective measures`
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction`

### Abbreviation (131 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (487 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `clinicians` → pred: `clinicians effective measures`
- gold: `prediction` → pred: `aki prediction`
- missed gold: `measures`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `continuous prediction model` → pred: `prediction`
