# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BILOU · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 37 | 3.0% |
| False Negative | 1159 | 95.2% |
| Boundary Error | 21 | 1.7% |
| Abbreviation | 26 | 2.1% |
| Nested Phrase | 21 | 1.7% |
| True Positive | 0 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **0.00%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.00%**
- Total predicted spans: 58 · Total gold spans: 1180

## Annotated Examples

### False Positive (37 total)
- spurious pred: `ontology`
- spurious pred: `support architecture`
- spurious pred: `clinical pathway`
- spurious pred: `knowledge`
- spurious pred: `knowledge`
- spurious pred: `diabetes`

### False Negative (1159 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (21 total)
- gold: `knowledge construction` → pred: `knowledge`
- gold: `knowledge construction` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`
- gold: `knowledge model` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`
- gold: `defined knowledge model` → pred: `knowledge`

### Abbreviation (26 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `sdm`
- missed gold: `data`
- missed gold: `data`
- missed gold: `data`

### Nested Phrase (21 total)
- gold: `knowledge construction` → pred: `knowledge`
- gold: `knowledge construction` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`
- gold: `knowledge model` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`
- gold: `defined knowledge model` → pred: `knowledge`
