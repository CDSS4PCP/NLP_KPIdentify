# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 833 | 56.4% |
| False Negative | 384 | 26.0% |
| Boundary Error | 259 | 17.5% |
| Abbreviation | 78 | 5.3% |
| Nested Phrase | 253 | 17.1% |
| True Positive | 537 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **32.97%**
- Strict entity recall (TP / (TP+FN+boundary)): **45.51%**
- Total predicted spans: 1629 · Total gold spans: 1180

## Annotated Examples

### False Positive (833 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `assistance`
- spurious pred: `treatment`

### False Negative (384 total)
- missed gold: `clinical practice guidelines`
- missed gold: `disseminate`
- missed gold: `<UNK>`
- missed gold: `triggered`
- missed gold: `<UNK>`
- missed gold: `development`

### Boundary Error (259 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules` → pred: `elementary rules`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `generate` → pred: `generate recommendations`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (78 total)
- spurious pred: `used`
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (253 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules` → pred: `elementary rules`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `generate` → pred: `generate recommendations`
- gold: `evaluation` → pred: `evaluation studies`
