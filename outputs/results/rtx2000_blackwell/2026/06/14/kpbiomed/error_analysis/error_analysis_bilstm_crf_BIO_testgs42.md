# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 72 | 5.8% |
| False Negative | 1147 | 92.8% |
| Boundary Error | 17 | 1.4% |
| Abbreviation | 29 | 2.3% |
| Nested Phrase | 17 | 1.4% |
| True Positive | 16 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **15.24%**
- Strict entity recall (TP / (TP+FN+boundary)): **1.36%**
- Total predicted spans: 105 · Total gold spans: 1180

## Annotated Examples

### False Positive (72 total)
- spurious pred: `clinical decision support system`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`

### False Negative (1147 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `<UNK>`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (17 total)
- gold: `clinical decision support system <UNK>` → pred: `clinical decision support system`
- gold: `decision support tasks` → pred: `decision support`
- gold: `decision support tasks` → pred: `decision support`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `decision support systems` → pred: `decision support`

### Abbreviation (29 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `sdm`
- missed gold: `data`
- missed gold: `data`
- missed gold: `data`

### Nested Phrase (17 total)
- gold: `clinical decision support system <UNK>` → pred: `clinical decision support system`
- gold: `decision support tasks` → pred: `decision support`
- gold: `decision support tasks` → pred: `decision support`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `decision support systems` → pred: `decision support`
