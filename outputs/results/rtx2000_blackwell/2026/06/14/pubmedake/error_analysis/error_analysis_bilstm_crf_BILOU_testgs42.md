# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BILOU · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 50 | 4.1% |
| False Negative | 1163 | 94.6% |
| Boundary Error | 17 | 1.4% |
| Abbreviation | 26 | 2.1% |
| Nested Phrase | 17 | 1.4% |
| True Positive | 0 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **0.00%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.00%**
- Total predicted spans: 67 · Total gold spans: 1180

## Annotated Examples

### False Positive (50 total)
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `clinical pathway`

### False Negative (1163 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (17 total)
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `vague knowledge` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`
- gold: `knowledge model` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`

### Abbreviation (26 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `sdm`
- missed gold: `data`
- missed gold: `data`
- missed gold: `data`

### Nested Phrase (17 total)
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `vague knowledge` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`
- gold: `knowledge model` → pred: `knowledge`
- gold: `knowledge sources` → pred: `knowledge`
