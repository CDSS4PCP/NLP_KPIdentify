# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 82 | 6.6% |
| False Negative | 1111 | 89.0% |
| Boundary Error | 56 | 4.5% |
| Abbreviation | 26 | 2.1% |
| Nested Phrase | 53 | 4.2% |
| True Positive | 13 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **8.61%**
- Strict entity recall (TP / (TP+FN+boundary)): **1.10%**
- Total predicted spans: 151 · Total gold spans: 1180

## Annotated Examples

### False Positive (82 total)
- spurious pred: `drug <UNK> system`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`
- spurious pred: `ontology`

### False Negative (1111 total)
- missed gold: `optimizing`
- missed gold: `clinical practice guidelines`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `design`
- missed gold: `enable`

### Boundary Error (56 total)
- gold: `developing clinical decision support systems` → pred: `clinical decision support`
- gold: `guideline representation models` → pred: `representation models`
- gold: `guideline representation models` → pred: `representation models`
- gold: `guideline representation models` → pred: `representation models`
- gold: `decision support systems` → pred: `decision support`
- gold: `guideline representation models` → pred: `representation models`

### Abbreviation (26 total)
- missed gold: `used`
- missed gold: `used`
- missed gold: `sdm`
- missed gold: `data`
- missed gold: `data`
- missed gold: `data`

### Nested Phrase (53 total)
- gold: `developing clinical decision support systems` → pred: `clinical decision support`
- gold: `guideline representation models` → pred: `representation models`
- gold: `guideline representation models` → pred: `representation models`
- gold: `guideline representation models` → pred: `representation models`
- gold: `decision support systems` → pred: `decision support`
- gold: `guideline representation models` → pred: `representation models`
