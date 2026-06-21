# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1238 | 51.8% |
| False Negative | 640 | 26.8% |
| Boundary Error | 510 | 21.4% |
| Abbreviation | 141 | 5.9% |
| Nested Phrase | 502 | 21.0% |
| True Positive | 1435 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **45.08%**
- Strict entity recall (TP / (TP+FN+boundary)): **55.51%**
- Total predicted spans: 3183 · Total gold spans: 2585

## Annotated Examples

### False Positive (1238 total)
- spurious pred: `aki`
- spurious pred: `clinical practice`
- spurious pred: `increased`
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `hospital aki`

### False Negative (640 total)
- missed gold: `feature modifications`
- missed gold: `described`
- missed gold: `use`
- missed gold: `<UNK>`
- missed gold: `challenges`
- missed gold: `integration`

### Boundary Error (510 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model output` → pred: `linking model output`
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network <UNK> -based`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `model interpretations` → pred: `applicable model interpretations`

### Abbreviation (141 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (502 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model output` → pred: `linking model output`
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network <UNK> -based`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `model interpretations` → pred: `applicable model interpretations`
