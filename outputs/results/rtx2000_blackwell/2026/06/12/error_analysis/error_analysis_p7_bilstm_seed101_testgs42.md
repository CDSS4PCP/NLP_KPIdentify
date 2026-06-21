# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: bilstm_crf · seed: 101

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 818 | 58.2% |
| False Negative | 346 | 24.6% |
| Boundary Error | 241 | 17.2% |
| Abbreviation | 135 | 9.6% |
| Nested Phrase | 234 | 16.7% |
| True Positive | 592 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **35.86%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.21%**
- Total predicted spans: 1651 · Total gold spans: 1179

## Annotated Examples

### False Positive (818 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `assistance`
- spurious pred: `patient`
- spurious pred: `treatment`
- spurious pred: `evidence`

### False Negative (346 total)
- missed gold: `clinical practice guidelines`
- missed gold: `disseminate`
- missed gold: `operates`
- missed gold: `triggered`
- missed gold: `rules`
- missed gold: `development`

### Boundary Error (241 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (135 total)
- spurious pred: `asti`
- spurious pred: `asti`
- spurious pred: `jena`
- spurious pred: `jena`
- gold: `jena rules` → pred: `jena`
- spurious pred: `cdss`

### Nested Phrase (234 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`
