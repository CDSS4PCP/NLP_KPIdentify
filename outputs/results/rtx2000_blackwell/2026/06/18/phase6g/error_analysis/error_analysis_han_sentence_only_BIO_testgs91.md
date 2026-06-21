# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1127 | 48.2% |
| False Negative | 719 | 30.7% |
| Boundary Error | 494 | 21.1% |
| Abbreviation | 122 | 5.2% |
| Nested Phrase | 483 | 20.6% |
| True Positive | 1372 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **45.84%**
- Strict entity recall (TP / (TP+FN+boundary)): **53.08%**
- Total predicted spans: 2993 · Total gold spans: 2585

## Annotated Examples

### False Positive (1127 total)
- spurious pred: `aki`
- spurious pred: `design`
- spurious pred: `process`
- spurious pred: `hospital aki`
- spurious pred: `vital signs`
- spurious pred: `<UNK> algorithms`

### False Negative (719 total)
- missed gold: `findings`
- missed gold: `described`
- missed gold: `use`
- missed gold: `<UNK>`
- missed gold: `challenges`
- missed gold: `measures`

### Boundary Error (494 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network <UNK> -based`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data`

### Abbreviation (122 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (483 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network <UNK> -based`
- gold: `continuous prediction model` → pred: `prediction`
- gold: `model interpretations` → pred: `applicable model interpretations`
- gold: `demographic data laboratory values vital signs` → pred: `demographic data`
