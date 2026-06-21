# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BILOU · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 869 | 58.8% |
| False Negative | 336 | 22.7% |
| Boundary Error | 274 | 18.5% |
| Abbreviation | 67 | 4.5% |
| Nested Phrase | 268 | 18.1% |
| True Positive | 570 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **33.27%**
- Strict entity recall (TP / (TP+FN+boundary)): **48.31%**
- Total predicted spans: 1713 · Total gold spans: 1180

## Annotated Examples

### False Positive (869 total)
- spurious pred: `guideline`
- spurious pred: `<UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`
- spurious pred: `assistance`

### False Negative (336 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `construct`

### Boundary Error (274 total)
- gold: `triggered` → pred: `triggered elementary rules`
- gold: `development` → pred: `under development`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK> implementation`
- gold: `<UNK> rules` → pred: `<UNK>`

### Abbreviation (67 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (268 total)
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `development` → pred: `under development`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK> implementation`
