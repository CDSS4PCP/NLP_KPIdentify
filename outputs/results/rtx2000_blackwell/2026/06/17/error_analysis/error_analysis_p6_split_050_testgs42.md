# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 861 | 59.6% |
| False Negative | 323 | 22.4% |
| Boundary Error | 261 | 18.1% |
| Abbreviation | 80 | 5.5% |
| Nested Phrase | 247 | 17.1% |
| True Positive | 596 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **34.69%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.51%**
- Total predicted spans: 1718 · Total gold spans: 1180

## Annotated Examples

### False Positive (861 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK> systems`
- spurious pred: `physicians`
- spurious pred: `assistance`
- spurious pred: `treatment`

### False Negative (323 total)
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `<UNK>`
- missed gold: `<UNK>`
- missed gold: `<UNK>`
- missed gold: `development`

### Boundary Error (261 total)
- gold: `clinical practice guidelines` → pred: `guidelines`
- gold: `background process` → pred: `process`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK>`
- gold: `generate` → pred: `generate recommendations`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`

### Abbreviation (80 total)
- spurious pred: `art`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `ed`
- spurious pred: `task`

### Nested Phrase (247 total)
- gold: `clinical practice guidelines` → pred: `guidelines`
- gold: `background process` → pred: `process`
- gold: `<UNK> <UNK> implementation` → pred: `<UNK>`
- gold: `generate` → pred: `generate recommendations`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `clinical decision support systems <UNK>` → pred: `clinical decision support systems`
