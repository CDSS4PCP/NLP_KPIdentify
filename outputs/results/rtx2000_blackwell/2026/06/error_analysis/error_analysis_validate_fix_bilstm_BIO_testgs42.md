# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: bilstm_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 129 | 10.0% |
| False Negative | 1106 | 86.1% |
| Boundary Error | 50 | 3.9% |
| Abbreviation | 28 | 2.2% |
| Nested Phrase | 43 | 3.3% |
| True Positive | 24 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **11.82%**
- Strict entity recall (TP / (TP+FN+boundary)): **2.03%**
- Total predicted spans: 203 · Total gold spans: 1180

## Annotated Examples

### False Positive (129 total)
- spurious pred: `<UNK> system`
- spurious pred: `treatment`
- spurious pred: `treatment`
- spurious pred: `<UNK> system`
- spurious pred: `clinical decision support system`
- spurious pred: `surgery`

### False Negative (1106 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (50 total)
- gold: `clinical decision support system <UNK>` → pred: `clinical decision support system`
- gold: `functions` → pred: `<UNK> functions`
- gold: `workflow model` → pred: `emergency workflow`
- gold: `medical decision support` → pred: `decision support methods`
- gold: `decision support tasks` → pred: `decision support`
- gold: `reasoning` → pred: `semantic reasoning`

### Abbreviation (28 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `sdm`
- missed gold: `data`
- missed gold: `data`
- missed gold: `data`

### Nested Phrase (43 total)
- gold: `clinical decision support system <UNK>` → pred: `clinical decision support system`
- gold: `functions` → pred: `<UNK> functions`
- gold: `decision support tasks` → pred: `decision support`
- gold: `reasoning` → pred: `semantic reasoning`
- gold: `clinical pathways cps` → pred: `clinical pathways`
- gold: `semantic data model` → pred: `semantic data`
