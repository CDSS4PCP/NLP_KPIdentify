# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1342 | 53.1% |
| False Negative | 629 | 24.9% |
| Boundary Error | 554 | 21.9% |
| Abbreviation | 161 | 6.4% |
| Nested Phrase | 547 | 21.7% |
| True Positive | 1402 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **42.51%**
- Strict entity recall (TP / (TP+FN+boundary)): **54.24%**
- Total predicted spans: 3298 · Total gold spans: 2585

## Annotated Examples

### False Positive (1342 total)
- spurious pred: `aki`
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `hospital aki`
- spurious pred: `patients`
- spurious pred: `vital signs`

### False Negative (629 total)
- missed gold: `model interpretations`
- missed gold: `described`
- missed gold: `use`
- missed gold: `<UNK>`
- missed gold: `challenges`
- missed gold: `measures`

### Boundary Error (554 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network <UNK>`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data`

### Abbreviation (161 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (547 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network <UNK>`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data`
