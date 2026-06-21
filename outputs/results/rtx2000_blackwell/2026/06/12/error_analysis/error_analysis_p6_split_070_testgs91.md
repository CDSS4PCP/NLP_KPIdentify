# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 1083 | 52.3% |
| False Negative | 532 | 25.7% |
| Boundary Error | 457 | 22.1% |
| Abbreviation | 219 | 10.6% |
| Nested Phrase | 458 | 22.1% |
| True Positive | 1584 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **50.70%**
- Strict entity recall (TP / (TP+FN+boundary)): **61.56%**
- Total predicted spans: 3124 · Total gold spans: 2573

## Annotated Examples

### False Positive (1083 total)
- spurious pred: `rnn algorithms`
- spurious pred: `model agnostic interpretation`
- spurious pred: `patients`
- spurious pred: `end stage kidney`
- spurious pred: `development`
- spurious pred: `development`

### False Negative (532 total)
- missed gold: `clinical decision support`
- missed gold: `clinicians`
- missed gold: `measures`
- missed gold: `impact`
- missed gold: `interventions`
- missed gold: `searched`

### Boundary Error (457 total)
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `settings` → pred: `resource developing world settings`
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `cds challenges`
- gold: `deployed` → pred: `deployed e g`

### Abbreviation (219 total)
- spurious pred: `auc`
- spurious pred: `cds`
- spurious pred: `cds`
- spurious pred: `cds`
- spurious pred: `cds`
- spurious pred: `cds`

### Nested Phrase (458 total)
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `settings` → pred: `resource developing world settings`
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `cds challenges`
- gold: `deployed` → pred: `deployed e g`
