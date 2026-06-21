# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 797 | 57.7% |
| False Negative | 346 | 25.1% |
| Boundary Error | 238 | 17.2% |
| Abbreviation | 135 | 9.8% |
| Nested Phrase | 228 | 16.5% |
| True Positive | 595 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **36.50%**
- Strict entity recall (TP / (TP+FN+boundary)): **50.47%**
- Total predicted spans: 1630 · Total gold spans: 1179

## Annotated Examples

### False Positive (797 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `physicians`
- spurious pred: `treatment`
- spurious pred: `treatment`
- spurious pred: `guidelines`

### False Negative (346 total)
- missed gold: `clinical practice guidelines`
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `operates`
- missed gold: `rules`
- missed gold: `browsing`

### Boundary Error (238 total)
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `conceptualization formalization implementation` → pred: `conceptualization`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`

### Abbreviation (135 total)
- spurious pred: `asti`
- spurious pred: `asti`
- spurious pred: `jena`
- spurious pred: `jena`
- gold: `jena rules` → pred: `jena`
- spurious pred: `cdss`

### Nested Phrase (228 total)
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `conceptualization formalization implementation` → pred: `conceptualization`
- gold: `jena rules` → pred: `jena`
- gold: `evaluation` → pred: `evaluation studies`
