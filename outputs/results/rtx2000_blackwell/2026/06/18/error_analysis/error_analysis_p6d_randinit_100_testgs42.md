# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 846 | 59.6% |
| False Negative | 317 | 22.3% |
| Boundary Error | 257 | 18.1% |
| Abbreviation | 83 | 5.8% |
| Nested Phrase | 248 | 17.5% |
| True Positive | 606 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.46%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.36%**
- Total predicted spans: 1709 · Total gold spans: 1180

## Annotated Examples

### False Positive (846 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `drug <UNK> system`
- spurious pred: `existing`
- spurious pred: `assistance`
- spurious pred: `treatment`

### False Negative (317 total)
- missed gold: `clinical practice guidelines`
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`

### Boundary Error (257 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK>`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (83 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`

### Nested Phrase (248 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK>`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
