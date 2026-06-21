# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 884 | 59.1% |
| False Negative | 345 | 23.1% |
| Boundary Error | 267 | 17.8% |
| Abbreviation | 72 | 4.8% |
| Nested Phrase | 267 | 17.8% |
| True Positive | 568 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **33.04%**
- Strict entity recall (TP / (TP+FN+boundary)): **48.14%**
- Total predicted spans: 1719 · Total gold spans: 1180

## Annotated Examples

### False Positive (884 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `<UNK>`

### False Negative (345 total)
- missed gold: `<UNK>`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `construct`
- missed gold: `created`
- missed gold: `specification`

### Boundary Error (267 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (72 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (267 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
