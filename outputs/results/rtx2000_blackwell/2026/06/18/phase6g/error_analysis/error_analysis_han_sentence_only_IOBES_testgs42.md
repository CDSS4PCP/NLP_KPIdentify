# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 884 | 58.6% |
| False Negative | 347 | 23.0% |
| Boundary Error | 277 | 18.4% |
| Abbreviation | 79 | 5.2% |
| Nested Phrase | 270 | 17.9% |
| True Positive | 556 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **32.38%**
- Strict entity recall (TP / (TP+FN+boundary)): **47.12%**
- Total predicted spans: 1717 · Total gold spans: 1180

## Annotated Examples

### False Positive (884 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`
- spurious pred: `assistance`

### False Negative (347 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `construct`

### Boundary Error (277 total)
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (79 total)
- spurious pred: `used`
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (270 total)
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
