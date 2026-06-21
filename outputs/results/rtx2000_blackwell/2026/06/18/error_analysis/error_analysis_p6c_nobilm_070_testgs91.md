# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: han_crf · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 970 | 49.1% |
| False Negative | 576 | 29.2% |
| Boundary Error | 428 | 21.7% |
| Abbreviation | 110 | 5.6% |
| Nested Phrase | 427 | 21.6% |
| True Positive | 1581 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **53.07%**
- Strict entity recall (TP / (TP+FN+boundary)): **61.16%**
- Total predicted spans: 2979 · Total gold spans: 2585

## Annotated Examples

### False Positive (970 total)
- spurious pred: `aki`
- spurious pred: `costs`
- spurious pred: `design`
- spurious pred: `patients`
- spurious pred: `patients`
- spurious pred: `model`

### False Negative (576 total)
- missed gold: `clinical decision support`
- missed gold: `settings`
- missed gold: `challenges`
- missed gold: `measures`
- missed gold: `<UNK>`
- missed gold: `impact`

### Boundary Error (428 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `prediction model`
- gold: `assessment` → pred: `provide real time assessment`

### Abbreviation (110 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### Nested Phrase (427 total)
- gold: `prediction` → pred: `aki prediction`
- gold: `recurrent neural network <UNK>` → pred: `recurrent neural network`
- gold: `prediction models` → pred: `prediction models model`
- gold: `developed` → pred: `developed model`
- gold: `prediction` → pred: `prediction model`
- gold: `assessment` → pred: `provide real time assessment`
