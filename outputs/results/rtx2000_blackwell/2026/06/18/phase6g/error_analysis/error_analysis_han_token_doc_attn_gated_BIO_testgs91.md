# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1053 | 44.9% |
| False Negative | 817 | 34.9% |
| Boundary Error | 473 | 20.2% |
| Abbreviation | 116 | 5.0% |
| Nested Phrase | 467 | 19.9% |
| True Positive | 1295 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **45.91%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.10%**
- Total predicted spans: 2821 · Total gold spans: 2585

## Annotated Examples

### False Positive (1053 total)
- spurious pred: `aki`
- spurious pred: `hospital aki`
- spurious pred: `hospitals`
- spurious pred: `vital signs`
- spurious pred: `<UNK> algorithms`
- spurious pred: `aki`

### False Negative (817 total)
- missed gold: `clinical decision support`
- missed gold: `feature modifications`
- missed gold: `use`
- missed gold: `<UNK>`
- missed gold: `challenges`
- missed gold: `data entry <UNK>`

### Boundary Error (473 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data`

### Abbreviation (116 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (467 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data`
