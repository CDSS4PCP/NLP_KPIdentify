# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_pubmedbert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1324 | 47.4% |
| False Negative | 863 | 30.9% |
| Boundary Error | 607 | 21.7% |
| Abbreviation | 229 | 8.2% |
| Nested Phrase | 622 | 22.3% |
| True Positive | 1094 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **36.17%**
- Strict entity recall (TP / (TP+FN+boundary)): **42.67%**
- Total predicted spans: 3025 · Total gold spans: 2564

## Annotated Examples

### False Positive (1324 total)
- spurious pred: `aki`
- spurious pred: `challenges`
- spurious pred: `design`
- spurious pred: `neural network`
- spurious pred: `aki`
- spurious pred: `patients`

### False Negative (863 total)
- missed gold: `lacking`
- missed gold: `models`
- missed gold: `obtained`
- missed gold: `models`
- missed gold: `training`
- missed gold: `internal validation`

### Boundary Error (607 total)
- gold: `clinical decision support` → pred: `real time clinical decision support`
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model output` → pred: `linking model output`
- gold: `recurrent neural network rnn` → pred: `externally validated recurrent neural network rnn`
- gold: `demographic data laboratory values vital signs` → pred: `laboratory`

### Abbreviation (229 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `cds`
- spurious pred: `cds`
- spurious pred: `cds`

### Nested Phrase (622 total)
- gold: `clinical decision support` → pred: `real time clinical decision support`
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `model output` → pred: `linking model output`
- gold: `recurrent neural network rnn` → pred: `externally validated recurrent neural network rnn`
- gold: `demographic data laboratory values vital signs` → pred: `laboratory`
