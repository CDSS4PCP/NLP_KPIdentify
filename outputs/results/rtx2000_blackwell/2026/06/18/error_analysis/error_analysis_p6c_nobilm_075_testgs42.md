# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 862 | 59.8% |
| False Negative | 325 | 22.5% |
| Boundary Error | 255 | 17.7% |
| Abbreviation | 79 | 5.5% |
| Nested Phrase | 244 | 16.9% |
| True Positive | 600 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **34.94%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.85%**
- Total predicted spans: 1717 · Total gold spans: 1180

## Annotated Examples

### False Positive (862 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK>`
- spurious pred: `drug centered <UNK>`
- spurious pred: `assistance`

### False Negative (325 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construct`

### Boundary Error (255 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (79 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`
- spurious pred: `ae`

### Nested Phrase (244 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
