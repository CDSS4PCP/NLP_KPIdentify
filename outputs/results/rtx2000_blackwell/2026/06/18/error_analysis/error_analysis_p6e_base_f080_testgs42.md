# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 792 | 57.0% |
| False Negative | 349 | 25.1% |
| Boundary Error | 248 | 17.9% |
| Abbreviation | 74 | 5.3% |
| Nested Phrase | 236 | 17.0% |
| True Positive | 583 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.92%**
- Strict entity recall (TP / (TP+FN+boundary)): **49.41%**
- Total predicted spans: 1623 · Total gold spans: 1180

## Annotated Examples

### False Positive (792 total)
- spurious pred: `guideline`
- spurious pred: `<UNK> systems`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`
- spurious pred: `treatment`

### False Negative (349 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`

### Boundary Error (248 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (74 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`

### Nested Phrase (236 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
