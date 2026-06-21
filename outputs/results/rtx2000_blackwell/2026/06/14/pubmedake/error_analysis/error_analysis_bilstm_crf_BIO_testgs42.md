# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 32 | 2.6% |
| False Negative | 1166 | 96.2% |
| Boundary Error | 14 | 1.2% |
| Abbreviation | 26 | 2.1% |
| Nested Phrase | 14 | 1.2% |
| True Positive | 0 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **0.00%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.00%**
- Total predicted spans: 46 · Total gold spans: 1180

## Annotated Examples

### False Positive (32 total)
- spurious pred: `ontology`
- spurious pred: `diabetes`
- spurious pred: `knowledge`
- spurious pred: `diabetes`
- spurious pred: `knowledge`
- spurious pred: `diabetes`

### False Negative (1166 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (14 total)
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `knowledge sources` → pred: `knowledge`
- gold: `knowledge model` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`
- gold: `defined knowledge model` → pred: `knowledge`
- gold: `encapsulated knowledge` → pred: `knowledge`

### Abbreviation (26 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `sdm`
- missed gold: `data`
- missed gold: `data`
- missed gold: `data`

### Nested Phrase (14 total)
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `knowledge sources` → pred: `knowledge`
- gold: `knowledge model` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`
- gold: `defined knowledge model` → pred: `knowledge`
- gold: `encapsulated knowledge` → pred: `knowledge`
