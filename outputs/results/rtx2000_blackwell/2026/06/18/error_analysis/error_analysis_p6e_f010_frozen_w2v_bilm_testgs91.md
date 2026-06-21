# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1222 | 50.6% |
| False Negative | 676 | 28.0% |
| Boundary Error | 516 | 21.4% |
| Abbreviation | 142 | 5.9% |
| Nested Phrase | 518 | 21.5% |
| True Positive | 1393 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **44.49%**
- Strict entity recall (TP / (TP+FN+boundary)): **53.89%**
- Total predicted spans: 3131 · Total gold spans: 2585

## Annotated Examples

### False Positive (1222 total)
- spurious pred: `aki`
- spurious pred: `clinical practice`
- spurious pred: `process`
- spurious pred: `vital signs`
- spurious pred: `clinical conditions`
- spurious pred: `patients`

### False Negative (676 total)
- missed gold: `feature modifications`
- missed gold: `findings`
- missed gold: `described`
- missed gold: `findings`
- missed gold: `increases`
- missed gold: `challenges`

### Boundary Error (516 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `model interpretation` → pred: `model`
- gold: `prediction` → pred: `aki prediction`
- gold: `model output` → pred: `linking model output`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction model`

### Abbreviation (142 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `nice`

### Nested Phrase (518 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `model interpretation` → pred: `model`
- gold: `prediction` → pred: `aki prediction`
- gold: `model output` → pred: `linking model output`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `model interpretations` → pred: `model`
