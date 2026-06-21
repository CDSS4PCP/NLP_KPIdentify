# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1129 | 49.7% |
| False Negative | 645 | 28.4% |
| Boundary Error | 496 | 21.9% |
| Abbreviation | 115 | 5.1% |
| Nested Phrase | 493 | 21.7% |
| True Positive | 1444 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **47.05%**
- Strict entity recall (TP / (TP+FN+boundary)): **55.86%**
- Total predicted spans: 3069 · Total gold spans: 2585

## Annotated Examples

### False Positive (1129 total)
- spurious pred: `aki`
- spurious pred: `patients`
- spurious pred: `model`
- spurious pred: `<UNK> algorithms`
- spurious pred: `aki`
- spurious pred: `model`

### False Negative (645 total)
- missed gold: `models`
- missed gold: `findings`
- missed gold: `use`
- missed gold: `settings`
- missed gold: `<UNK>`
- missed gold: `indicate`

### Boundary Error (496 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network <UNK>`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`

### Abbreviation (115 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (493 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network <UNK>` → pred: `validated recurrent neural network <UNK>`
- gold: `continuous prediction model` → pred: `prediction model`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
