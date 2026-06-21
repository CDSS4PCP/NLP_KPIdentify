# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1145 | 47.6% |
| False Negative | 731 | 30.4% |
| Boundary Error | 531 | 22.1% |
| Abbreviation | 116 | 4.8% |
| Nested Phrase | 535 | 22.2% |
| True Positive | 1323 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **44.11%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.18%**
- Total predicted spans: 2999 · Total gold spans: 2585

## Annotated Examples

### False Positive (1145 total)
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `patients`
- spurious pred: `patients`
- spurious pred: `<UNK> algorithms`
- spurious pred: `model 1`

### False Negative (731 total)
- missed gold: `lacking`
- missed gold: `described`
- missed gold: `use`
- missed gold: `settings`
- missed gold: `increases`
- missed gold: `<UNK>`

### Boundary Error (531 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `recurrent neural networks` → pred: `recurrent`
- gold: `model output` → pred: `linking model output`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`

### Abbreviation (116 total)
- spurious pred: `auc`
- missed gold: `use`
- spurious pred: `plan`
- spurious pred: `pace`
- gold: `fast healthcare <UNK> resources <UNK>` → pred: `fast`
- spurious pred: `ed`

### Nested Phrase (535 total)
- gold: `clinical decision support` → pred: `time clinical decision support`
- gold: `recurrent neural networks` → pred: `recurrent`
- gold: `model output` → pred: `linking model output`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `demographic data laboratory values vital signs` → pred: `vital signs`
