# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 101

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 848 | 59.8% |
| False Negative | 320 | 22.6% |
| Boundary Error | 249 | 17.6% |
| Abbreviation | 138 | 9.7% |
| Nested Phrase | 240 | 16.9% |
| True Positive | 610 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.74%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.74%**
- Total predicted spans: 1707 · Total gold spans: 1179

## Annotated Examples

### False Positive (848 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`
- spurious pred: `evidence`

### False Negative (320 total)
- missed gold: `operates`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `construct`
- missed gold: `created`
- missed gold: `specification`

### Boundary Error (249 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `conceptualization formalization implementation` → pred: `formalization implementation`

### Abbreviation (138 total)
- spurious pred: `asti`
- spurious pred: `used`
- spurious pred: `asti`
- spurious pred: `jena`
- spurious pred: `jena`
- gold: `jena rules` → pred: `jena`

### Nested Phrase (240 total)
- gold: `disseminate` → pred: `disseminate state`
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `conceptualization formalization implementation` → pred: `formalization implementation`
