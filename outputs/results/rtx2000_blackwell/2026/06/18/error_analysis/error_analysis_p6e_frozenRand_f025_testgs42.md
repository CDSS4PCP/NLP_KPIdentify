# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 879 | 60.7% |
| False Negative | 333 | 23.0% |
| Boundary Error | 236 | 16.3% |
| Abbreviation | 77 | 5.3% |
| Nested Phrase | 229 | 15.8% |
| True Positive | 611 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.40%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.78%**
- Total predicted spans: 1726 · Total gold spans: 1180

## Annotated Examples

### False Positive (879 total)
- spurious pred: `<UNK>`
- spurious pred: `guideline`
- spurious pred: `<UNK> systems`
- spurious pred: `assistance`
- spurious pred: `treatment`
- spurious pred: `evidence`

### False Negative (333 total)
- missed gold: `clinical practice guidelines`
- missed gold: `disseminate`
- missed gold: `<UNK>`
- missed gold: `rules`
- missed gold: `<UNK>`
- missed gold: `<UNK>`

### Boundary Error (236 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `triggered elementary rules`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `infer` → pred: `infer recommendations`
- gold: `generate` → pred: `generate recommendations`

### Abbreviation (77 total)
- spurious pred: `used`
- missed gold: `used`
- missed gold: `used`
- spurious pred: `task`
- spurious pred: `task`
- spurious pred: `task`

### Nested Phrase (229 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `<UNK> <UNK> implementation` → pred: `implementation`
- gold: `infer` → pred: `infer recommendations`
