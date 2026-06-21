# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 13

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 827 | 58.9% |
| False Negative | 324 | 23.1% |
| Boundary Error | 253 | 18.0% |
| Abbreviation | 132 | 9.4% |
| Nested Phrase | 244 | 17.4% |
| True Positive | 602 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.79%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.06%**
- Total predicted spans: 1682 · Total gold spans: 1179

## Annotated Examples

### False Positive (827 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `physicians`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`

### False Negative (324 total)
- missed gold: `clinical practice guidelines`
- missed gold: `disseminate`
- missed gold: `operates`
- missed gold: `background process`
- missed gold: `triggered`
- missed gold: `rules`

### Boundary Error (253 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `conceptualization formalization implementation` → pred: `implementation`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (132 total)
- spurious pred: `asti`
- spurious pred: `art`
- spurious pred: `asti`
- spurious pred: `jena`
- spurious pred: `jena`
- gold: `jena rules` → pred: `jena`

### Nested Phrase (244 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `conceptualization formalization implementation` → pred: `implementation`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`
