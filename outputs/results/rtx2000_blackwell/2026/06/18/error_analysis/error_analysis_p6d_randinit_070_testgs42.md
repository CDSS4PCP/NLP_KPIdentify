# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 843 | 59.5% |
| False Negative | 325 | 22.9% |
| Boundary Error | 249 | 17.6% |
| Abbreviation | 85 | 6.0% |
| Nested Phrase | 240 | 16.9% |
| True Positive | 606 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.69%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.36%**
- Total predicted spans: 1698 · Total gold spans: 1180

## Annotated Examples

### False Positive (843 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `drug <UNK> system`
- spurious pred: `assistance`
- spurious pred: `treatment`
- spurious pred: `treatment`

### False Negative (325 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construct`

### Boundary Error (249 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK>`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (85 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`

### Nested Phrase (240 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK>`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
