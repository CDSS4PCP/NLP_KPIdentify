# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 979 | 47.5% |
| False Negative | 621 | 30.1% |
| Boundary Error | 462 | 22.4% |
| Abbreviation | 232 | 11.3% |
| Nested Phrase | 458 | 22.2% |
| True Positive | 1490 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **50.84%**
- Strict entity recall (TP / (TP+FN+boundary)): **57.91%**
- Total predicted spans: 2931 · Total gold spans: 2573

## Annotated Examples

### False Positive (979 total)
- spurious pred: `rnn algorithms`
- spurious pred: `model`
- spurious pred: `patients`
- spurious pred: `development`
- spurious pred: `development`
- spurious pred: `auc`

### False Negative (621 total)
- missed gold: `continuous prediction model`
- missed gold: `settings`
- missed gold: `measures`
- missed gold: `impact`
- missed gold: `searched`
- missed gold: `interventions`

### Boundary Error (462 total)
- gold: `recurrent neural network rnn` → pred: `recurrent neural network rnn -based continuous prediction model`
- gold: `developed` → pred: `developed model`
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `cds increases`
- gold: `challenges` → pred: `cds challenges`
- gold: `products` → pred: `nice products`

### Abbreviation (232 total)
- spurious pred: `auc`
- spurious pred: `cds`
- spurious pred: `cds`
- spurious pred: `cds`
- spurious pred: `cds`
- spurious pred: `cds`

### Nested Phrase (458 total)
- gold: `recurrent neural network rnn` → pred: `recurrent neural network rnn -based continuous prediction model`
- missed gold: `continuous prediction model`
- gold: `developed` → pred: `developed model`
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `cds increases`
- gold: `challenges` → pred: `cds challenges`
