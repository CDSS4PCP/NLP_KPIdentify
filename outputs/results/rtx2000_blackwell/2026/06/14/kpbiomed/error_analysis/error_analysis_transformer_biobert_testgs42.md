# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_biobert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 103 | 8.3% |
| False Negative | 1097 | 88.3% |
| Boundary Error | 43 | 3.5% |
| Abbreviation | 43 | 3.5% |
| Nested Phrase | 39 | 3.1% |
| True Positive | 32 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **17.98%**
- Strict entity recall (TP / (TP+FN+boundary)): **2.73%**
- Total predicted spans: 178 · Total gold spans: 1172

## Annotated Examples

### False Positive (103 total)
- spurious pred: `care`
- spurious pred: `hypertension`
- spurious pred: `clinical decision support`
- spurious pred: `surgery`
- spurious pred: `ontology`
- spurious pred: `surgery`

### False Negative (1097 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (43 total)
- gold: `clinical decision support system cdss` → pred: `clinical decision support system`
- gold: `guideline representation models` → pred: `guideline representation`
- gold: `guideline representation models` → pred: `guideline`
- gold: `guideline representation models` → pred: `guideline representation`
- gold: `fuzzy cognitive map framework` → pred: `fuzzy cognitive map`
- gold: `decision support tasks fuzzy cognitive maps fcm` → pred: `fuzzy cognitive`

### Abbreviation (43 total)
- spurious pred: `care`
- missed gold: `used`
- missed gold: `used`
- missed gold: `cdss`
- missed gold: `cdss`
- missed gold: `cdss`

### Nested Phrase (39 total)
- gold: `clinical decision support system cdss` → pred: `clinical decision support system`
- gold: `guideline representation models` → pred: `guideline representation`
- gold: `guideline representation models` → pred: `guideline`
- gold: `guideline representation models` → pred: `guideline representation`
- gold: `fuzzy cognitive map framework` → pred: `fuzzy cognitive map`
- gold: `decision support tasks fuzzy cognitive maps fcm` → pred: `fuzzy cognitive`
