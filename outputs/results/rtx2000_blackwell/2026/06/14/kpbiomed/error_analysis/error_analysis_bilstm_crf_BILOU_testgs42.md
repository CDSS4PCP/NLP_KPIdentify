# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BILOU · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 63 | 5.1% |
| False Negative | 1166 | 94.3% |
| Boundary Error | 8 | 0.6% |
| Abbreviation | 29 | 2.3% |
| Nested Phrase | 8 | 0.6% |
| True Positive | 6 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **7.79%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.51%**
- Total predicted spans: 77 · Total gold spans: 1180

## Annotated Examples

### False Positive (63 total)
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`

### False Negative (1166 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `<UNK>`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (8 total)
- gold: `decision support tasks` → pred: `decision support`
- gold: `decision support tasks` → pred: `decision support`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `<UNK>` → pred: `semantic <UNK>`
- gold: `decision support services` → pred: `decision support`

### Abbreviation (29 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `sdm`
- missed gold: `data`
- missed gold: `data`
- missed gold: `data`

### Nested Phrase (8 total)
- gold: `decision support tasks` → pred: `decision support`
- gold: `decision support tasks` → pred: `decision support`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `<UNK>` → pred: `semantic <UNK>`
- gold: `decision support services` → pred: `decision support`
