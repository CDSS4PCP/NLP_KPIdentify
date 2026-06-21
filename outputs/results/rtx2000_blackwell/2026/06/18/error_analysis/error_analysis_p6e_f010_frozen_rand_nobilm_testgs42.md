# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 896 | 59.9% |
| False Negative | 319 | 21.3% |
| Boundary Error | 282 | 18.8% |
| Abbreviation | 76 | 5.1% |
| Nested Phrase | 274 | 18.3% |
| True Positive | 579 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **32.95%**
- Strict entity recall (TP / (TP+FN+boundary)): **49.07%**
- Total predicted spans: 1757 · Total gold spans: 1180

## Annotated Examples

### False Positive (896 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `drug <UNK> system`
- spurious pred: `<UNK> systems`
- spurious pred: `<UNK>`
- spurious pred: `assistance`

### False Negative (319 total)
- missed gold: `clinical practice guidelines`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `triggered`
- missed gold: `<UNK>`
- missed gold: `development`

### Boundary Error (282 total)
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`

### Abbreviation (76 total)
- spurious pred: `cpgs`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `ed`

### Nested Phrase (274 total)
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `<UNK> rules` → pred: `<UNK>`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinicians` → pred: `help clinicians`
