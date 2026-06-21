# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 792 | 55.9% |
| False Negative | 367 | 25.9% |
| Boundary Error | 257 | 18.1% |
| Abbreviation | 81 | 5.7% |
| Nested Phrase | 251 | 17.7% |
| True Positive | 556 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **34.64%**
- Strict entity recall (TP / (TP+FN+boundary)): **47.12%**
- Total predicted spans: 1605 · Total gold spans: 1180

## Annotated Examples

### False Positive (792 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK>`
- spurious pred: `assistance`
- spurious pred: `patient`

### False Negative (367 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`

### Boundary Error (257 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (81 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `ed`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (251 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
