# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 27 | 1.0% |
| False Negative | 2582 | 98.9% |
| Boundary Error | 2 | 0.1% |
| Abbreviation | 50 | 1.9% |
| Nested Phrase | 2 | 0.1% |
| True Positive | 1 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **3.33%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.04%**
- Total predicted spans: 30 · Total gold spans: 2585

## Annotated Examples

### False Positive (27 total)
- spurious pred: `background`
- spurious pred: `one`
- spurious pred: `in`
- spurious pred: `the`
- spurious pred: `results`
- spurious pred: `a`

### False Negative (2582 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (2 total)
- gold: `checklist validation` → pred: `checklist`
- gold: `operative knowledge` → pred: `operative`

### Abbreviation (50 total)
- missed gold: `use`
- missed gold: `gaps`
- spurious pred: `one`
- spurious pred: `in`
- missed gold: `gaps`
- missed gold: `plan`

### Nested Phrase (2 total)
- gold: `checklist validation` → pred: `checklist`
- gold: `operative knowledge` → pred: `operative`
