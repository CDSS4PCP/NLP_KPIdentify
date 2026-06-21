# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 843 | 59.4% |
| False Negative | 328 | 23.1% |
| Boundary Error | 248 | 17.5% |
| Abbreviation | 84 | 5.9% |
| Nested Phrase | 237 | 16.7% |
| True Positive | 604 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.63%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.19%**
- Total predicted spans: 1695 · Total gold spans: 1180

## Annotated Examples

### False Positive (843 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK>`
- spurious pred: `physicians`
- spurious pred: `assistance`

### False Negative (328 total)
- missed gold: `clinical practice guidelines`
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`

### Boundary Error (248 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (84 total)
- spurious pred: `art`
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (237 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
