# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: IOBES · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 64 | 5.2% |
| False Negative | 1165 | 94.1% |
| Boundary Error | 9 | 0.7% |
| Abbreviation | 29 | 2.3% |
| Nested Phrase | 9 | 0.7% |
| True Positive | 6 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **7.59%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.51%**
- Total predicted spans: 79 · Total gold spans: 1180

## Annotated Examples

### False Positive (64 total)
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`

### False Negative (1165 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `<UNK>`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (9 total)
- gold: `decision support tasks` → pred: `decision support`
- gold: `decision support tasks` → pred: `decision support`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `decision support application` → pred: `decision support`
- gold: `<UNK>` → pred: `semantic <UNK>`

### Abbreviation (29 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `sdm`
- missed gold: `data`
- missed gold: `data`
- missed gold: `data`

### Nested Phrase (9 total)
- gold: `decision support tasks` → pred: `decision support`
- gold: `decision support tasks` → pred: `decision support`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `decision support application` → pred: `decision support`
- gold: `<UNK>` → pred: `semantic <UNK>`
