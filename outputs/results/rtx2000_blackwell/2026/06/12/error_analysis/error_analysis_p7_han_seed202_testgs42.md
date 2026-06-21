# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 202

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 848 | 60.1% |
| False Negative | 317 | 22.5% |
| Boundary Error | 245 | 17.4% |
| Abbreviation | 128 | 9.1% |
| Nested Phrase | 239 | 17.0% |
| True Positive | 617 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **36.08%**
- Strict entity recall (TP / (TP+FN+boundary)): **52.33%**
- Total predicted spans: 1710 · Total gold spans: 1179

## Annotated Examples

### False Positive (848 total)
- spurious pred: `asti`
- spurious pred: `drug ordering system`
- spurious pred: `physicians`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`

### False Negative (317 total)
- missed gold: `operates`
- missed gold: `triggered`
- missed gold: `browsing`
- missed gold: `development`
- missed gold: `construct`
- missed gold: `created`

### Boundary Error (245 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `conceptualization formalization implementation` → pred: `implementation`
- gold: `jena rules` → pred: `jena`

### Abbreviation (128 total)
- spurious pred: `asti`
- spurious pred: `asti`
- spurious pred: `jena`
- spurious pred: `jena`
- gold: `jena rules` → pred: `jena`
- spurious pred: `cdss`

### Nested Phrase (239 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `conceptualization formalization implementation` → pred: `implementation`
- gold: `jena rules` → pred: `jena`
