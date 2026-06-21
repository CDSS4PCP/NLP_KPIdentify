# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_biobert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 227 | 16.3% |
| False Negative | 810 | 58.0% |
| Boundary Error | 359 | 25.7% |
| Abbreviation | 80 | 5.7% |
| Nested Phrase | 936 | 67.0% |
| True Positive | 3 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **0.51%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.26%**
- Total predicted spans: 589 · Total gold spans: 1172

## Annotated Examples

### False Positive (227 total)
- spurious pred: `asti a guideline based drug ordering system for`
- spurious pred: `to`
- spurious pred: `state`
- spurious pred: `information concerning treatment strategy but these guidelines are`
- spurious pred: `used in routine practice the asti project`
- spurious pred: `mode`

### False Negative (810 total)
- missed gold: `optimizing`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `operates`
- missed gold: `background process`

### Boundary Error (359 total)
- gold: `clinical practice guidelines` → pred: `care existing computer based ordering systems for physicians provide effective drug centered checks but offer little assistance for optimizing the overall patient centered treatment strategy evidence based clinical practice guidelines have been`
- gold: `design` → pred: `to design a guideline based ordering system to enable general`
- gold: `prescription errors` → pred: `to avoid prescription errors and to improve compliance with best therapeutic practices the critic mode operates as a background process and corrects the physician 's prescription on the basis of automatically triggered elementary rules that account for isolated guideline recommendations the`
- gold: `decision tree` → pred: `physician to the best treatment by browsing a comprehensive guideline knowledge base represented as a decision tree a first prototype applied to hypertension is currently`
- gold: `construction` → pred: `construction of a clinical decision support system for`
- gold: `clinical decision support system cdss` → pred: `surgery based on domain ontology and rules reasoning objective to construct a clinical decision support system cdss for`

### Abbreviation (80 total)
- spurious pred: `to`
- spurious pred: `mode`
- gold: `used` → pred: `defects we used`
- gold: `used` → pred: `disease a typical case was used to validate the cdss functions and accuracy two clients were`
- spurious pred: `for`
- spurious pred: `of`

### Nested Phrase (936 total)
- gold: `clinical practice guidelines` → pred: `care existing computer based ordering systems for physicians provide effective drug centered checks but offer little assistance for optimizing the overall patient centered treatment strategy evidence based clinical practice guidelines have been`
- gold: `design` → pred: `to design a guideline based ordering system to enable general`
- gold: `prescription errors` → pred: `to avoid prescription errors and to improve compliance with best therapeutic practices the critic mode operates as a background process and corrects the physician 's prescription on the basis of automatically triggered elementary rules that account for isolated guideline recommendations the`
- gold: `decision tree` → pred: `physician to the best treatment by browsing a comprehensive guideline knowledge base represented as a decision tree a first prototype applied to hypertension is currently`
- missed gold: `optimizing`
- missed gold: `enable`
