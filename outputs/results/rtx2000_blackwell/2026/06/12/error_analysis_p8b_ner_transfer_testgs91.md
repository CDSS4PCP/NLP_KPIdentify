# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: zeroshot_transfer:d4data/biomedical-ner-all · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1328 | 36.5% |
| False Negative | 1845 | 50.7% |
| Boundary Error | 465 | 12.8% |
| Abbreviation | 0 | 0.0% |
| Nested Phrase | 448 | 12.3% |
| True Positive | 254 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **12.41%**
- Strict entity recall (TP / (TP+FN+boundary)): **9.91%**
- Total predicted spans: 2047 · Total gold spans: 2564

## Annotated Examples

### False Positive (1328 total)
- spurious pred: `real`
- spurious pred: `acute kidney injury aki`
- spurious pred: `poor`
- spurious pred: `increased`
- spurious pred: `care`
- spurious pred: `aki`
- spurious pred: `simple`
- spurious pred: `black box`

### False Negative (1845 total)
- missed gold: `clinicians`
- missed gold: `measures`
- missed gold: `prediction`
- missed gold: `prevention`
- missed gold: `lacking`
- missed gold: `model output`
- missed gold: `clinical decisions`
- missed gold: `models`

### Boundary Error (465 total)
- gold: `external validation` → pred: `hospital acute kidney injury external validation`
- gold: `patient outcomes` → pred: `outcomes`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network rnn` → pred: `externally validated recurrent neural network rnn`
- gold: `continuous prediction model` → pred: `continuous prediction`
- gold: `clinical decision support` → pred: `clinical decision support methods`
- gold: `prediction models` → pred: `2 stage hierarchical prediction models`
- gold: `outcome variable` → pred: `outcome`

### Nested Phrase (448 total)
- gold: `external validation` → pred: `hospital acute kidney injury external validation`
- gold: `patient outcomes` → pred: `outcomes`
- gold: `prediction models` → pred: `aki prediction models`
- gold: `recurrent neural network rnn` → pred: `externally validated recurrent neural network rnn`
- gold: `continuous prediction model` → pred: `continuous prediction`
- gold: `clinical decision support` → pred: `clinical decision support methods`
- gold: `prediction models` → pred: `2 stage hierarchical prediction models`
- gold: `outcome variable` → pred: `outcome`
