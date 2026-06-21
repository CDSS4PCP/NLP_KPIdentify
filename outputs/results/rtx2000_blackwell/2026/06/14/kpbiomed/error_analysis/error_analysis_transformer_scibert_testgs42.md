# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_scibert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 106 | 8.5% |
| False Negative | 1098 | 88.3% |
| Boundary Error | 39 | 3.1% |
| Abbreviation | 47 | 3.8% |
| Nested Phrase | 39 | 3.1% |
| True Positive | 35 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **19.44%**
- Strict entity recall (TP / (TP+FN+boundary)): **2.99%**
- Total predicted spans: 180 · Total gold spans: 1172

## Annotated Examples

### False Positive (106 total)
- spurious pred: `hypertension`
- spurious pred: `domain ontology`
- spurious pred: `domain ontology`
- spurious pred: `domain ontology`
- spurious pred: `ontology`
- spurious pred: `chronic disease`

### False Negative (1098 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (39 total)
- gold: `clinical decision support system cdss` → pred: `support`
- gold: `clinical guidelines` → pred: `guidelines`
- gold: `fuzzy cognitive map framework` → pred: `fuzzy cognitive map`
- gold: `decision support tasks fuzzy cognitive maps fcm` → pred: `fuzzy cognitive maps`
- gold: `medical decision support` → pred: `support`
- gold: `reasoning` → pred: `semantic reasoning`

### Abbreviation (47 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `cdss`
- missed gold: `cdss`
- missed gold: `cdss`
- missed gold: `sdm`

### Nested Phrase (39 total)
- gold: `clinical decision support system cdss` → pred: `support`
- gold: `clinical guidelines` → pred: `guidelines`
- gold: `fuzzy cognitive map framework` → pred: `fuzzy cognitive map`
- gold: `decision support tasks fuzzy cognitive maps fcm` → pred: `fuzzy cognitive maps`
- gold: `medical decision support` → pred: `support`
- gold: `reasoning` → pred: `semantic reasoning`
