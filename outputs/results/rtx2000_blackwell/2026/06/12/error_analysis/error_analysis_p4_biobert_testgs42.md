# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_biobert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 691 | 53.2% |
| False Negative | 373 | 28.7% |
| Boundary Error | 235 | 18.1% |
| Abbreviation | 119 | 9.2% |
| Nested Phrase | 225 | 17.3% |
| True Positive | 564 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **37.85%**
- Strict entity recall (TP / (TP+FN+boundary)): **48.12%**
- Total predicted spans: 1490 · Total gold spans: 1172

## Annotated Examples

### False Positive (691 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `computer`
- spurious pred: `physicians`
- spurious pred: `patient`
- spurious pred: `treatment`

### False Negative (373 total)
- missed gold: `operates`
- missed gold: `background process`
- missed gold: `rules`
- missed gold: `browsing`
- missed gold: `construct`
- missed gold: `created`

### Boundary Error (235 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `triggered` → pred: `triggered elementary rules`
- gold: `infer` → pred: `infer recommendations`
- gold: `generate` → pred: `generate recommendations`
- gold: `evaluation` → pred: `evaluation studies`
- gold: `sharable clinical decision support system` → pred: `clinical decision support system`

### Abbreviation (119 total)
- spurious pred: `asti`
- spurious pred: `asti`
- spurious pred: `jena`
- spurious pred: `cdss`
- spurious pred: `cdss`
- spurious pred: `cdss`

### Nested Phrase (225 total)
- gold: `enable` → pred: `enable general practitioners`
- gold: `triggered` → pred: `triggered elementary rules`
- missed gold: `rules`
- gold: `infer` → pred: `infer recommendations`
- gold: `generate` → pred: `generate recommendations`
- gold: `evaluation` → pred: `evaluation studies`
