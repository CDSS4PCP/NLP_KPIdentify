# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 777

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 826 | 59.0% |
| False Negative | 322 | 23.0% |
| Boundary Error | 253 | 18.1% |
| Abbreviation | 136 | 9.7% |
| Nested Phrase | 248 | 17.7% |
| True Positive | 604 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.89%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.23%**
- Total predicted spans: 1683 · Total gold spans: 1179

## Annotated Examples

### False Positive (826 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `physicians`
- spurious pred: `assistance`
- spurious pred: `overall patient`
- spurious pred: `treatment`

### False Negative (322 total)
- missed gold: `disseminate`
- missed gold: `operates`
- missed gold: `rules`
- missed gold: `development`
- missed gold: `rules reasoning`
- missed gold: `construct`

### Boundary Error (253 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `automatically triggered`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `conceptualization formalization implementation` → pred: `formalization implementation`
- gold: `jena rules` → pred: `jena`

### Abbreviation (136 total)
- spurious pred: `asti`
- spurious pred: `art`
- spurious pred: `asti`
- spurious pred: `is`
- spurious pred: `jena`
- spurious pred: `jena`

### Nested Phrase (248 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `triggered` → pred: `automatically triggered`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `conceptualization formalization implementation` → pred: `formalization implementation`
- gold: `jena rules` → pred: `jena`
