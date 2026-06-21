# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 849 | 59.0% |
| False Negative | 337 | 23.4% |
| Boundary Error | 252 | 17.5% |
| Abbreviation | 80 | 5.6% |
| Nested Phrase | 244 | 17.0% |
| True Positive | 591 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **34.93%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.08%**
- Total predicted spans: 1692 · Total gold spans: 1180

## Annotated Examples

### False Positive (849 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `drug <UNK> system`
- spurious pred: `assistance`
- spurious pred: `treatment`
- spurious pred: `evidence`

### False Negative (337 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`

### Boundary Error (252 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK> implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (80 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `care`
- spurious pred: `task`
- spurious pred: `ed`

### Nested Phrase (244 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK> implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
