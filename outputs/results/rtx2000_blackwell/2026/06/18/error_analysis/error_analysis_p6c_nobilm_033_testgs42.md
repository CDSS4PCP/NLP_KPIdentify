# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 836 | 58.8% |
| False Negative | 337 | 23.7% |
| Boundary Error | 249 | 17.5% |
| Abbreviation | 84 | 5.9% |
| Nested Phrase | 240 | 16.9% |
| True Positive | 594 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.38%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.34%**
- Total predicted spans: 1679 · Total gold spans: 1180

## Annotated Examples

### False Positive (836 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `drug <UNK> system`
- spurious pred: `assistance`
- spurious pred: `patient centered treatment`
- spurious pred: `treatment`

### False Negative (337 total)
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construct`

### Boundary Error (249 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`
- gold: `integration` → pred: `cpgs integration`

### Abbreviation (84 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`

### Nested Phrase (240 total)
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`
- gold: `integration` → pred: `cpgs integration`
