# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 822 | 58.3% |
| False Negative | 328 | 23.3% |
| Boundary Error | 260 | 18.4% |
| Abbreviation | 74 | 5.2% |
| Nested Phrase | 248 | 17.6% |
| True Positive | 592 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.36%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.17%**
- Total predicted spans: 1674 · Total gold spans: 1180

## Annotated Examples

### False Positive (822 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK>`
- spurious pred: `<UNK>`
- spurious pred: `<UNK>`
- spurious pred: `assistance`

### False Negative (328 total)
- missed gold: `disseminate`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construct`

### Boundary Error (260 total)
- gold: `enable` → pred: `enable general practitioners`
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
- spurious pred: `ae`

### Nested Phrase (248 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
