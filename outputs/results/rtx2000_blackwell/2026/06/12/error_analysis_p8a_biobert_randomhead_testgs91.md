# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_biobert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 396 | 13.4% |
| False Negative | 1803 | 61.2% |
| Boundary Error | 748 | 25.4% |
| Abbreviation | 0 | 0.0% |
| Nested Phrase | 2006 | 68.1% |
| True Positive | 13 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **1.12%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.51%**
- Total predicted spans: 1157 · Total gold spans: 2564

## Annotated Examples

### False Positive (396 total)
- spurious pred: `black box`
- spurious pred: `of`
- spurious pred: `tertiary hospitals in`
- spurious pred: `seoul national university bundang hospital and`
- spurious pred: `hypertension`
- spurious pred: `of review to review literature from 2016 to`
- spurious pred: `children and`
- spurious pred: `hypertension`

### False Negative (1803 total)
- missed gold: `recurrent neural networks`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`
- missed gold: `measures`
- missed gold: `prediction`
- missed gold: `prevention`
- missed gold: `lacking`

### Boundary Error (748 total)
- gold: `clinical decision support` → pred: `real time clinical decision support based on recurrent`
- gold: `external validation` → pred: `networks for in hospital acute kidney injury external validation and model interpretation background acute kidney injury aki is commonly encountered in clinical practice and is associated with poor patient outcomes and increased health care costs despite it`
- gold: `prediction models` → pred: `significant challenges for clinicians effective measures for aki prediction and prevention are lacking previously published aki prediction models`
- gold: `external validation` → pred: `have a simple design without external validation furthermore little is known about the process of linking model output and clinical decisions due to`
- gold: `models` → pred: `network models objective we`
- gold: `recurrent neural network rnn` → pred: `to present an externally validated recurrent`
- gold: `continuous prediction model` → pred: `network rnn -based continuous prediction model for in hospital aki and show applicable model interpretations in`
- gold: `clinical decision support` → pred: `to clinical decision support`

### Nested Phrase (2006 total)
- gold: `clinical decision support` → pred: `real time clinical decision support based on recurrent`
- gold: `external validation` → pred: `networks for in hospital acute kidney injury external validation and model interpretation background acute kidney injury aki is commonly encountered in clinical practice and is associated with poor patient outcomes and increased health care costs despite it`
- gold: `prediction models` → pred: `significant challenges for clinicians effective measures for aki prediction and prevention are lacking previously published aki prediction models`
- gold: `external validation` → pred: `have a simple design without external validation furthermore little is known about the process of linking model output and clinical decisions due to`
- gold: `models` → pred: `network models objective we`
- gold: `continuous prediction model` → pred: `network rnn -based continuous prediction model for in hospital aki and show applicable model interpretations in`
- gold: `clinical decision support` → pred: `to clinical decision support`
- gold: `hospitalized` → pred: `study populations were all patients aged 18 years or older who were hospitalized for more than 48 hours between 2013 and 2017 in`
