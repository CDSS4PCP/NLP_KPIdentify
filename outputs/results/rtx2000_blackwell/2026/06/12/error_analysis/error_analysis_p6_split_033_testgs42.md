# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 803 | 56.7% |
| False Negative | 351 | 24.8% |
| Boundary Error | 263 | 18.6% |
| Abbreviation | 144 | 10.2% |
| Nested Phrase | 256 | 18.1% |
| True Positive | 565 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **34.64%**
- Strict entity recall (TP / (TP+FN+boundary)): **47.92%**
- Total predicted spans: 1631 · Total gold spans: 1179

## Annotated Examples

### False Positive (803 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `treatment`
- spurious pred: `treatment`
- spurious pred: `guidelines`
- spurious pred: `asti`

### False Negative (351 total)
- missed gold: `disseminate`
- missed gold: `operates`
- missed gold: `triggered`
- missed gold: `rules`
- missed gold: `directs`
- missed gold: `browsing`

### Boundary Error (263 total)
- gold: `clinical practice guidelines` → pred: `guidelines`
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `jena rules` → pred: `jena`

### Abbreviation (144 total)
- spurious pred: `asti`
- spurious pred: `asti`
- spurious pred: `jena`
- spurious pred: `jena`
- gold: `jena rules` → pred: `jena`
- spurious pred: `cdss`

### Nested Phrase (256 total)
- gold: `clinical practice guidelines` → pred: `guidelines`
- gold: `enable` → pred: `enable general practitioners`
- gold: `background process` → pred: `process`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `rules reasoning` → pred: `reasoning`
- gold: `jena rules` → pred: `jena`
