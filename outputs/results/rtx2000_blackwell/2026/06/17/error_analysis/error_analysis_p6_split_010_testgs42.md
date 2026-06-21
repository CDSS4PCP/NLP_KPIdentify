# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 857 | 57.7% |
| False Negative | 357 | 24.0% |
| Boundary Error | 272 | 18.3% |
| Abbreviation | 75 | 5.0% |
| Nested Phrase | 268 | 18.0% |
| True Positive | 551 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **32.80%**
- Strict entity recall (TP / (TP+FN+boundary)): **46.69%**
- Total predicted spans: 1680 · Total gold spans: 1180

## Annotated Examples

### False Positive (857 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `assistance`
- spurious pred: `patient`

### False Negative (357 total)
- missed gold: `<UNK>`
- missed gold: `triggered`
- missed gold: `<UNK>`
- missed gold: `development`
- missed gold: `construction`
- missed gold: `construct`

### Boundary Error (272 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules` → pred: `elementary rules`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `infer` → pred: `infer recommendations`
- gold: `generate` → pred: `generate recommendations`

### Abbreviation (75 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`

### Nested Phrase (268 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules` → pred: `elementary rules`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `infer` → pred: `infer recommendations`
- gold: `generate` → pred: `generate recommendations`
