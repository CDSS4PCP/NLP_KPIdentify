# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_biobert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1434 | 50.3% |
| False Negative | 831 | 29.1% |
| Boundary Error | 587 | 20.6% |
| Abbreviation | 261 | 9.2% |
| Nested Phrase | 593 | 20.8% |
| True Positive | 1146 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **36.19%**
- Strict entity recall (TP / (TP+FN+boundary)): **44.70%**
- Total predicted spans: 3167 · Total gold spans: 2564

## Annotated Examples

### False Positive (1434 total)
- spurious pred: `real`
- spurious pred: `aki`
- spurious pred: `clinical`
- spurious pred: `design`
- spurious pred: `aki`
- spurious pred: `patients`

### False Negative (831 total)
- missed gold: `lacking`
- missed gold: `obtained`
- missed gold: `trajectory`
- missed gold: `performance`
- missed gold: `developed`
- missed gold: `evaluated`

### Boundary Error (587 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model output` → pred: `linking model output`
- gold: `models` → pred: `network models`
- gold: `recurrent neural network rnn` → pred: `externally validated recurrent neural network rnn`
- gold: `demographic data laboratory values vital signs` → pred: `data`

### Abbreviation (261 total)
- gold: `demographic data laboratory values vital signs` → pred: `data`
- spurious pred: `real`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `cds`

### Nested Phrase (593 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model output` → pred: `linking model output`
- gold: `models` → pred: `network models`
- gold: `recurrent neural network rnn` → pred: `externally validated recurrent neural network rnn`
- gold: `demographic data laboratory values vital signs` → pred: `data`
