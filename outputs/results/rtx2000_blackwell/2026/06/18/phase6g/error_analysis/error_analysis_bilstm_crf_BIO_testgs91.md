# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1064 | 45.6% |
| False Negative | 764 | 32.7% |
| Boundary Error | 505 | 21.6% |
| Abbreviation | 129 | 5.5% |
| Nested Phrase | 491 | 21.0% |
| True Positive | 1316 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **45.62%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.91%**
- Total predicted spans: 2885 · Total gold spans: 2585

## Annotated Examples

### False Positive (1064 total)
- spurious pred: `hospital acute`
- spurious pred: `aki`
- spurious pred: `increased`
- spurious pred: `design`
- spurious pred: `hospital aki`
- spurious pred: `vital signs`

### False Negative (764 total)
- missed gold: `model interpretations`
- missed gold: `outcome variable`
- missed gold: `findings`
- missed gold: `described`
- missed gold: `use`
- missed gold: `findings`

### Boundary Error (505 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data`
- gold: `area under the receiver operating characteristic curve auc` → pred: `area under the receiver operating characteristic curve`

### Abbreviation (129 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (491 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data`
- gold: `area under the receiver operating characteristic curve auc` → pred: `area under the receiver operating characteristic curve`
