# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1241 | 51.1% |
| False Negative | 648 | 26.7% |
| Boundary Error | 540 | 22.2% |
| Abbreviation | 103 | 4.2% |
| Nested Phrase | 535 | 22.0% |
| True Positive | 1397 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **43.96%**
- Strict entity recall (TP / (TP+FN+boundary)): **54.04%**
- Total predicted spans: 3178 · Total gold spans: 2585

## Annotated Examples

### False Positive (1241 total)
- spurious pred: `process`
- spurious pred: `patients`
- spurious pred: `patients`
- spurious pred: `model`
- spurious pred: `<UNK> algorithms`
- spurious pred: `model`

### False Negative (648 total)
- missed gold: `clinicians`
- missed gold: `trajectory`
- missed gold: `findings`
- missed gold: `described`
- missed gold: `settings`
- missed gold: `undetected`

### Boundary Error (540 total)
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `demographic data laboratory values vital signs` → pred: `laboratory values vital signs`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `internal validation` → pred: `validation`

### Abbreviation (103 total)
- spurious pred: `auc`
- spurious pred: `use`
- spurious pred: `use`
- gold: `fast healthcare <UNK> resources <UNK>` → pred: `fast`
- spurious pred: `rule`
- spurious pred: `ed`

### Nested Phrase (535 total)
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `demographic data laboratory values vital signs` → pred: `laboratory values vital signs`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `internal validation` → pred: `validation`
- gold: `internal validation` → pred: `validation`
