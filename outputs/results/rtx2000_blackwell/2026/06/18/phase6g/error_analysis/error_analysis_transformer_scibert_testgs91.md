# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_scibert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1383 | 49.8% |
| False Negative | 773 | 27.8% |
| Boundary Error | 621 | 22.4% |
| Abbreviation | 243 | 8.8% |
| Nested Phrase | 632 | 22.8% |
| True Positive | 1170 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **36.86%**
- Strict entity recall (TP / (TP+FN+boundary)): **45.63%**
- Total predicted spans: 3174 · Total gold spans: 2564

## Annotated Examples

### False Positive (1383 total)
- spurious pred: `real`
- spurious pred: `aki`
- spurious pred: `design`
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `signs`

### False Negative (773 total)
- missed gold: `lacking`
- missed gold: `obtained`
- missed gold: `models`
- missed gold: `training`
- missed gold: `internal validation`
- missed gold: `external validation cohorts`

### Boundary Error (621 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model output` → pred: `linking model`
- gold: `models` → pred: `neural network models`
- gold: `recurrent neural network rnn` → pred: `validated recurrent neural network rnn`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data laboratory values`

### Abbreviation (243 total)
- spurious pred: `real`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `cds`
- spurious pred: `cds`

### Nested Phrase (632 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `models` → pred: `neural network models`
- gold: `recurrent neural network rnn` → pred: `validated recurrent neural network rnn`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data laboratory values`
- gold: `prediction models` → pred: `hierarchical prediction models model`
