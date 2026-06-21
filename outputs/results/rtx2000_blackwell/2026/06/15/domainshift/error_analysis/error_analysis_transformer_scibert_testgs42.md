# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_scibert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 168 | 12.9% |
| False Negative | 1082 | 83.1% |
| Boundary Error | 52 | 4.0% |
| Abbreviation | 54 | 4.1% |
| Nested Phrase | 52 | 4.0% |
| True Positive | 38 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **14.73%**
- Strict entity recall (TP / (TP+FN+boundary)): **3.24%**
- Total predicted spans: 258 · Total gold spans: 1172

## Annotated Examples

### False Positive (168 total)
- spurious pred: `primary care`
- spurious pred: `hypertension`
- spurious pred: `clinical decision support system`
- spurious pred: `domain ontology`
- spurious pred: `domain ontology`
- spurious pred: `ontology`

### False Negative (1082 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (52 total)
- gold: `clinical decision support system cdss` → pred: `clinical decision support system`
- gold: `clinical decision support systems` → pred: `support`
- gold: `developing clinical decision support systems` → pred: `clinical decision support systems`
- gold: `fuzzy cognitive map framework` → pred: `fuzzy cognitive map`
- gold: `decision support tasks fuzzy cognitive maps fcm` → pred: `fuzzy cognitive maps`
- gold: `clinical pathways cps` → pred: `clinical pathways`

### Abbreviation (54 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `cdss`
- missed gold: `cdss`
- missed gold: `cdss`
- missed gold: `sdm`

### Nested Phrase (52 total)
- gold: `clinical decision support system cdss` → pred: `clinical decision support system`
- gold: `clinical decision support systems` → pred: `support`
- gold: `developing clinical decision support systems` → pred: `clinical decision support systems`
- gold: `fuzzy cognitive map framework` → pred: `fuzzy cognitive map`
- gold: `decision support tasks fuzzy cognitive maps fcm` → pred: `fuzzy cognitive maps`
- gold: `clinical pathways cps` → pred: `clinical pathways`
