# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_biobert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 421 | 14.9% |
| False Negative | 2215 | 78.2% |
| Boundary Error | 196 | 6.9% |
| Abbreviation | 119 | 4.2% |
| Nested Phrase | 185 | 6.5% |
| True Positive | 153 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **19.87%**
- Strict entity recall (TP / (TP+FN+boundary)): **5.97%**
- Total predicted spans: 770 · Total gold spans: 2564

## Annotated Examples

### False Positive (421 total)
- spurious pred: `acute kidney injury`
- spurious pred: `acute kidney injury aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`

### False Negative (2215 total)
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`
- missed gold: `measures`

### Boundary Error (196 total)
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `clinical decision support cds` → pred: `clinical decision support`
- gold: `clinical decision support systems cdsss` → pred: `clinical decision support systems`
- gold: `examined prescription drug monitoring` → pred: `prescription drug monitoring`
- gold: `integrate clinical decision support` → pred: `clinical decision support`
- gold: `clinical decision support services` → pred: `clinical decision support`

### Abbreviation (119 total)
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- spurious pred: `aki`
- missed gold: `use`
- missed gold: `gaps`

### Nested Phrase (185 total)
- gold: `recurrent neural network rnn` → pred: `recurrent neural network`
- gold: `clinical decision support cds` → pred: `clinical decision support`
- gold: `clinical decision support systems cdsss` → pred: `clinical decision support systems`
- gold: `examined prescription drug monitoring` → pred: `prescription drug monitoring`
- gold: `integrate clinical decision support` → pred: `clinical decision support`
- gold: `clinical decision support services` → pred: `clinical decision support`
