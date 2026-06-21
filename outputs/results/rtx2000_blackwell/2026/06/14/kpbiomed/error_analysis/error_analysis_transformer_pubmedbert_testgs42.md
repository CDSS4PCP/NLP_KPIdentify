# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_pubmedbert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 99 | 8.1% |
| False Negative | 1066 | 86.7% |
| Boundary Error | 64 | 5.2% |
| Abbreviation | 40 | 3.3% |
| Nested Phrase | 59 | 4.8% |
| True Positive | 42 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **20.49%**
- Strict entity recall (TP / (TP+FN+boundary)): **3.58%**
- Total predicted spans: 205 · Total gold spans: 1172

## Annotated Examples

### False Positive (99 total)
- spurious pred: `clinical decision support`
- spurious pred: `domain ontology`
- spurious pred: `domain ontology`
- spurious pred: `ontology`
- spurious pred: `domain ontology`
- spurious pred: `ontology`

### False Negative (1066 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (64 total)
- gold: `clinical decision support system cdss` → pred: `clinical decision support`
- gold: `sharable clinical decision support system` → pred: `clinical decision support`
- gold: `clinical decision support systems cdsss` → pred: `chronic disease clinical decision support`
- gold: `clinical decision support systems` → pred: `clinical decision support`
- gold: `developing clinical decision support systems` → pred: `clinical decision support`
- gold: `workflow model` → pred: `workflow`

### Abbreviation (40 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `cdss`
- missed gold: `cdss`
- missed gold: `cdss`
- missed gold: `sdm`

### Nested Phrase (59 total)
- gold: `clinical decision support system cdss` → pred: `clinical decision support`
- gold: `sharable clinical decision support system` → pred: `clinical decision support`
- gold: `clinical decision support systems` → pred: `clinical decision support`
- gold: `developing clinical decision support systems` → pred: `clinical decision support`
- gold: `workflow model` → pred: `workflow`
- gold: `workflow model` → pred: `workflow`
