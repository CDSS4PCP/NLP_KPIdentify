# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_biobert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 875 | 60.5% |
| False Negative | 294 | 20.3% |
| Boundary Error | 277 | 19.2% |
| Abbreviation | 165 | 11.4% |
| Nested Phrase | 271 | 18.7% |
| True Positive | 601 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **34.28%**
- Strict entity recall (TP / (TP+FN+boundary)): **51.28%**
- Total predicted spans: 1753 · Total gold spans: 1172

## Annotated Examples

### False Positive (875 total)
- spurious pred: `asti`
- spurious pred: `guideline`
- spurious pred: `ordering system`
- spurious pred: `primary`
- spurious pred: `computer`
- spurious pred: `ordering systems`

### False Negative (294 total)
- missed gold: `enable`
- missed gold: `background process`
- missed gold: `triggered`
- missed gold: `development`
- missed gold: `confirmed`
- missed gold: `correctness`

### Boundary Error (277 total)
- gold: `prescription errors` → pred: `avoid prescription errors`
- gold: `rules` → pred: `elementary rules`
- gold: `infer` → pred: `infer recommendations`
- gold: `generate` → pred: `generate recommendations`
- gold: `domain experts` → pred: `domain`
- gold: `sharable clinical decision support system` → pred: `clinical decision support system`

### Abbreviation (165 total)
- spurious pred: `asti`
- spurious pred: `drug`
- spurious pred: `asti`
- spurious pred: `base`
- spurious pred: `jena`
- spurious pred: `jena`

### Nested Phrase (271 total)
- gold: `prescription errors` → pred: `avoid prescription errors`
- gold: `rules` → pred: `elementary rules`
- gold: `infer` → pred: `infer recommendations`
- gold: `generate` → pred: `generate recommendations`
- gold: `domain experts` → pred: `domain`
- gold: `sharable clinical decision support system` → pred: `clinical decision support system`
