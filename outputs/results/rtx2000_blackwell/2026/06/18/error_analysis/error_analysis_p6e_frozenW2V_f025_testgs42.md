# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 857 | 58.4% |
| False Negative | 363 | 24.7% |
| Boundary Error | 248 | 16.9% |
| Abbreviation | 71 | 4.8% |
| Nested Phrase | 241 | 16.4% |
| True Positive | 569 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **33.99%**
- Strict entity recall (TP / (TP+FN+boundary)): **48.22%**
- Total predicted spans: 1674 · Total gold spans: 1180

## Annotated Examples

### False Positive (857 total)
- spurious pred: `<UNK>`
- spurious pred: `<UNK> systems`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`

### False Negative (363 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construction`
- missed gold: `construct`

### Boundary Error (248 total)
- gold: `background process` → pred: `process`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `generate` → pred: `generate recommendations`
- gold: `satisfaction` → pred: `recommendations satisfaction`
- gold: `clinical decision support systems <UNK>` → pred: `<UNK>`
- gold: `implementation` → pred: `<UNK> implementation`

### Abbreviation (71 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (241 total)
- gold: `background process` → pred: `process`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `generate` → pred: `generate recommendations`
- gold: `satisfaction` → pred: `recommendations satisfaction`
- gold: `clinical decision support systems <UNK>` → pred: `<UNK>`
- gold: `implementation` → pred: `<UNK> implementation`
