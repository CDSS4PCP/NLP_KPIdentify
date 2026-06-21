# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1222 | 50.8% |
| False Negative | 664 | 27.6% |
| Boundary Error | 519 | 21.6% |
| Abbreviation | 139 | 5.8% |
| Nested Phrase | 508 | 21.1% |
| True Positive | 1402 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **44.61%**
- Strict entity recall (TP / (TP+FN+boundary)): **54.24%**
- Total predicted spans: 3143 · Total gold spans: 2585

## Annotated Examples

### False Positive (1222 total)
- spurious pred: `aki`
- spurious pred: `process`
- spurious pred: `patients`
- spurious pred: `patients`
- spurious pred: `algorithms`
- spurious pred: `aki`

### False Negative (664 total)
- missed gold: `model output`
- missed gold: `feature modifications`
- missed gold: `use`
- missed gold: `settings`
- missed gold: `<UNK>`
- missed gold: `clinician trust`

### Boundary Error (519 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `models` → pred: `neural network models`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`

### Abbreviation (139 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (508 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `models` → pred: `neural network models`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`
- gold: `developed` → pred: `developed model`
