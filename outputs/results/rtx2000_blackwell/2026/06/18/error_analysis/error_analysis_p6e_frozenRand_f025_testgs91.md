# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1178 | 50.3% |
| False Negative | 631 | 27.0% |
| Boundary Error | 531 | 22.7% |
| Abbreviation | 123 | 5.3% |
| Nested Phrase | 534 | 22.8% |
| True Positive | 1423 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **45.43%**
- Strict entity recall (TP / (TP+FN+boundary)): **55.05%**
- Total predicted spans: 3132 · Total gold spans: 2585

## Annotated Examples

### False Positive (1178 total)
- spurious pred: `aki`
- spurious pred: `<UNK>`
- spurious pred: `process`
- spurious pred: `patients`
- spurious pred: `patients`
- spurious pred: `model`

### False Negative (631 total)
- missed gold: `settings`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`
- missed gold: `evidence`
- missed gold: `searched`

### Boundary Error (531 total)
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network <UNK>`
- gold: `model interpretations` → pred: `model`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `feature modifications` → pred: `modifications`

### Abbreviation (123 total)
- spurious pred: `aki`
- spurious pred: `ml`
- spurious pred: `auc`
- spurious pred: `plan`
- gold: `fast healthcare <UNK> resources <UNK>` → pred: `fast`
- spurious pred: `rule`

### Nested Phrase (534 total)
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network <UNK>`
- gold: `model interpretations` → pred: `model`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `feature modifications` → pred: `modifications`
