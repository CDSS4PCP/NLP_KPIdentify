# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 838 | 58.9% |
| False Negative | 325 | 22.8% |
| Boundary Error | 260 | 18.3% |
| Abbreviation | 81 | 5.7% |
| Nested Phrase | 249 | 17.5% |
| True Positive | 595 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.14%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.42%**
- Total predicted spans: 1693 · Total gold spans: 1180

## Annotated Examples

### False Positive (838 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`
- spurious pred: `evidence`

### False Negative (325 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construct`

### Boundary Error (260 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK> implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`

### Abbreviation (81 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`

### Nested Phrase (249 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK> implementation`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`
