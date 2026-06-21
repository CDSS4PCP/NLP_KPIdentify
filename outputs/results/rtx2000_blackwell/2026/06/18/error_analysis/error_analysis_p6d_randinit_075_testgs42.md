# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 859 | 59.8% |
| False Negative | 324 | 22.5% |
| Boundary Error | 254 | 17.7% |
| Abbreviation | 86 | 6.0% |
| Nested Phrase | 246 | 17.1% |
| True Positive | 602 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.10%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.02%**
- Total predicted spans: 1715 · Total gold spans: 1180

## Annotated Examples

### False Positive (859 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `assistance`
- spurious pred: `patient`

### False Negative (324 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`

### Boundary Error (254 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`

### Abbreviation (86 total)
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`

### Nested Phrase (246 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`
