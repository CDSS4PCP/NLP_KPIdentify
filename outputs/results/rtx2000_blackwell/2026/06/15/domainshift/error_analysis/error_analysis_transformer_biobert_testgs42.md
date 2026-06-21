# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_biobert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 181 | 14.0% |
| False Negative | 1037 | 80.1% |
| Boundary Error | 77 | 5.9% |
| Abbreviation | 51 | 3.9% |
| Nested Phrase | 71 | 5.5% |
| True Positive | 58 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **18.35%**
- Strict entity recall (TP / (TP+FN+boundary)): **4.95%**
- Total predicted spans: 316 · Total gold spans: 1172

## Annotated Examples

### False Positive (181 total)
- spurious pred: `asti`
- spurious pred: `asti`
- spurious pred: `hypertension`
- spurious pred: `clinical decision support system`
- spurious pred: `surgery`
- spurious pred: `ontology`

### False Negative (1037 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (77 total)
- gold: `rules reasoning` → pred: `rules`
- gold: `clinical decision support system cdss` → pred: `clinical decision support system`
- gold: `sharable clinical decision support system` → pred: `clinical decision support`
- gold: `clinical decision support systems` → pred: `clinical decision support`
- gold: `developing clinical decision support systems` → pred: `clinical decision support systems`
- gold: `transform architecture` → pred: `transform`

### Abbreviation (51 total)
- spurious pred: `asti`
- spurious pred: `asti`
- missed gold: `used`
- missed gold: `used`
- missed gold: `cdss`
- missed gold: `cdss`

### Nested Phrase (71 total)
- gold: `rules reasoning` → pred: `rules`
- gold: `clinical decision support system cdss` → pred: `clinical decision support system`
- gold: `sharable clinical decision support system` → pred: `clinical decision support`
- gold: `clinical decision support systems` → pred: `clinical decision support`
- gold: `developing clinical decision support systems` → pred: `clinical decision support systems`
- gold: `transform architecture` → pred: `transform`
