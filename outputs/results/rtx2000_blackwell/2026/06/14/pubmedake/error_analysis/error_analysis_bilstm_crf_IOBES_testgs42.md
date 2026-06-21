# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 48 | 3.9% |
| False Negative | 1167 | 95.0% |
| Boundary Error | 13 | 1.1% |
| Abbreviation | 26 | 2.1% |
| Nested Phrase | 13 | 1.1% |
| True Positive | 0 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **0.00%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.00%**
- Total predicted spans: 61 · Total gold spans: 1180

## Annotated Examples

### False Positive (48 total)
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `clinical pathway`
- spurious pred: `knowledge`

### False Negative (1167 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (13 total)
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
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

### Nested Phrase (13 total)
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `knowledge sources` → pred: `knowledge`
- gold: `knowledge model` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`
- gold: `defined knowledge model` → pred: `knowledge`
