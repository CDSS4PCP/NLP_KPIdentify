# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 874 | 58.2% |
| False Negative | 354 | 23.6% |
| Boundary Error | 273 | 18.2% |
| Abbreviation | 80 | 5.3% |
| Nested Phrase | 269 | 17.9% |
| True Positive | 553 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **32.53%**
- Strict entity recall (TP / (TP+FN+boundary)): **46.86%**
- Total predicted spans: 1700 · Total gold spans: 1180

## Annotated Examples

### False Positive (874 total)
- spurious pred: `guideline`
- spurious pred: `computer`
- spurious pred: `<UNK> systems`
- spurious pred: `<UNK>`
- spurious pred: `treatment`
- spurious pred: `art`

### False Negative (354 total)
- missed gold: `disseminate`
- missed gold: `<UNK>`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `development`
- missed gold: `construct`

### Boundary Error (273 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `prescription errors` → pred: `avoid prescription errors`
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `triggered elementary rules`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`

### Abbreviation (80 total)
- spurious pred: `art`
- spurious pred: `used`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (269 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `prescription errors` → pred: `avoid prescription errors`
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `rules reasoning` → pred: `reasoning`
