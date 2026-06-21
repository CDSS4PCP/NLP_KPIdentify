# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BILOU · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1122 | 48.1% |
| False Negative | 679 | 29.1% |
| Boundary Error | 530 | 22.7% |
| Abbreviation | 121 | 5.2% |
| Nested Phrase | 519 | 22.3% |
| True Positive | 1376 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **45.44%**
- Strict entity recall (TP / (TP+FN+boundary)): **53.23%**
- Total predicted spans: 3028 · Total gold spans: 2585

## Annotated Examples

### False Positive (1122 total)
- spurious pred: `aki`
- spurious pred: `clinical practice`
- spurious pred: `increased`
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `hospital aki`

### False Negative (679 total)
- missed gold: `feature modifications`
- missed gold: `described`
- missed gold: `use`
- missed gold: `<UNK>`
- missed gold: `challenges`
- missed gold: `integration`

### Boundary Error (530 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model output` → pred: `linking model output`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data`

### Abbreviation (121 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (519 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model output` → pred: `linking model output`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data`
