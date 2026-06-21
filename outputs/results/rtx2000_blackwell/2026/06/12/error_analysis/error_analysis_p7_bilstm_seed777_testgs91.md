# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: IOBES · model: bilstm_crf · seed: 777

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 962 | 48.4% |
| False Negative | 578 | 29.1% |
| Boundary Error | 446 | 22.5% |
| Abbreviation | 209 | 10.5% |
| Nested Phrase | 441 | 22.2% |
| True Positive | 1549 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **52.38%**
- Strict entity recall (TP / (TP+FN+boundary)): **60.20%**
- Total predicted spans: 2957 · Total gold spans: 2573

## Annotated Examples

### False Positive (962 total)
- spurious pred: `rnn algorithms`
- spurious pred: `model`
- spurious pred: `interpretation`
- spurious pred: `patients`
- spurious pred: `development`
- spurious pred: `development`

### False Negative (578 total)
- missed gold: `models`
- missed gold: `findings`
- missed gold: `use`
- missed gold: `undercontrolled`
- missed gold: `data entry requests`
- missed gold: `measures`

### Boundary Error (446 total)
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `cds challenges`
- gold: `deployed` → pred: `deployed e g commitment`
- gold: `impact` → pred: `impact cds`

### Abbreviation (209 total)
- spurious pred: `auc`
- spurious pred: `aki`
- spurious pred: `cds`
- missed gold: `use`
- spurious pred: `cds`
- spurious pred: `cds`

### Nested Phrase (441 total)
- gold: `assessment` → pred: `time assessment`
- gold: `increases` → pred: `cds increases`
- gold: `detection control` → pred: `detection`
- gold: `challenges` → pred: `cds challenges`
- gold: `deployed` → pred: `deployed e g commitment`
- gold: `impact` → pred: `impact cds`
