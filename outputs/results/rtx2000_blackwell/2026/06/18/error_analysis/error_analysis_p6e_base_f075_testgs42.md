# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 834 | 58.8% |
| False Negative | 337 | 23.7% |
| Boundary Error | 248 | 17.5% |
| Abbreviation | 79 | 5.6% |
| Nested Phrase | 240 | 16.9% |
| True Positive | 595 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.48%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.42%**
- Total predicted spans: 1677 · Total gold spans: 1180

## Annotated Examples

### False Positive (834 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `assistance`
- spurious pred: `treatment`

### False Negative (337 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construct`

### Boundary Error (248 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK> implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (79 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`

### Nested Phrase (240 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK> implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
