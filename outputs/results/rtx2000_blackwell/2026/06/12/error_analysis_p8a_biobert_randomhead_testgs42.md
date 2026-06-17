# Error Analysis — Gold Standard 42

Source: `testgs42.json` · schema: BIO · model: transformer_biobert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 227 | 16.3% |
| False Negative | 810 | 58.0% |
| Boundary Error | 359 | 25.7% |
| Abbreviation | 0 | 0.0% |
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
- spurious pred: `format which`
- spurious pred: `hypoglycemia`

### False Negative (810 total)
- missed gold: `optimizing`
- missed gold: `developed`
- missed gold: `disseminate`
- missed gold: `enable`
- missed gold: `operates`
- missed gold: `background process`
- missed gold: `triggered`
- missed gold: `rules`

### Boundary Error (359 total)
- gold: `clinical practice guidelines` → pred: `care existing computer based ordering systems for physicians provide effective drug centered checks but offer little assistance for optimizing the overall patient centered treatment strategy evidence based clinical practice guidelines have been`
- gold: `design` → pred: `to design a guideline based ordering system to enable general`
- gold: `prescription errors` → pred: `to avoid prescription errors and to improve compliance with best therapeutic practices the critic mode operates as a background process and corrects the physician 's prescription on the basis of automatically triggered elementary rules that account for isolated guideline recommendations the`
- gold: `decision tree` → pred: `physician to the best treatment by browsing a comprehensive guideline knowledge base represented as a decision tree a first prototype applied to hypertension is currently`
- gold: `construction` → pred: `construction of a clinical decision support system for`
- gold: `clinical decision support system cdss` → pred: `surgery based on domain ontology and rules reasoning objective to construct a clinical decision support system cdss for`
- gold: `rules reasoning` → pred: `surgery based on domain ontology and rules reasoning in the setting of hospitalized diabetic patients materials and`
- gold: `conceptualization formalization implementation` → pred: `the ontology was created with a modified ontology development method including specification and conceptualization formalization implementation and evaluation and maintenance the protege web ontology language editor was used to implement the ontology embedded clinical knowledge was elicited to complement the domain ontology with formal concept analysis the decision rules were translated into`

### Nested Phrase (936 total)
- gold: `clinical practice guidelines` → pred: `care existing computer based ordering systems for physicians provide effective drug centered checks but offer little assistance for optimizing the overall patient centered treatment strategy evidence based clinical practice guidelines have been`
- gold: `design` → pred: `to design a guideline based ordering system to enable general`
- gold: `prescription errors` → pred: `to avoid prescription errors and to improve compliance with best therapeutic practices the critic mode operates as a background process and corrects the physician 's prescription on the basis of automatically triggered elementary rules that account for isolated guideline recommendations the`
- gold: `decision tree` → pred: `physician to the best treatment by browsing a comprehensive guideline knowledge base represented as a decision tree a first prototype applied to hypertension is currently`
- missed gold: `optimizing`
- missed gold: `enable`
- missed gold: `operates`
- missed gold: `background process`
