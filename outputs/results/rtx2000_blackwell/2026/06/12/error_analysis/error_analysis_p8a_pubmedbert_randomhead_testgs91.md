# Error Analysis — Gold Standard 91

Source: `testgs91.json` · schema: BIO · model: transformer_pubmedbert · seed: 42

## Summary

| Category | Count | % of errors |
|----------|-------|-------------|
| False Positive | 3 | 0.1% |
| False Negative | 2454 | 95.6% |
| Boundary Error | 110 | 4.3% |
| Abbreviation | 69 | 2.7% |
| Nested Phrase | 2303 | 89.7% |
| True Positive | 0 | — |

- Strict entity precision (TP / (TP+FP+boundary)): **0.00%**
- Strict entity recall (TP / (TP+FN+boundary)): **0.00%**
- Total predicted spans: 113 · Total gold spans: 2564

## Annotated Examples

### False Positive (3 total)
- spurious pred: `smart medical information technology for healthcare smith introduction this article is part of the focus theme of methods of information in medicine on the german medical informatics initiative smart medical information technology for healthcare`
- spurious pred: `is one of four consortia funded by the german medical informatics initiative mi i to create an alliance of universities university hospitals research institutions and it companies`
- spurious pred: `we continue to expand our use of a services oriented architecture approach for cds across multiple institutions`

### False Negative (2454 total)
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
- missed gold: `clinicians`

### Boundary Error (110 total)
- gold: `demographic data laboratory values vital signs` → pred: `real time clinical decision support based on recurrent neural networks for in hospital acute kidney injury external validation and model interpretation background acute kidney injury aki is commonly encountered in clinical practice and is associated with poor patient outcomes and increased health care costs despite it posing significant challenges for clinicians effective measures for aki prediction and prevention are lacking previously published aki prediction models mostly have a simple design without external validation furthermore little is known about the process of linking model output and clinical decisions due to the black box nature of neural network models objective we aimed to present an externally validated recurrent neural network rnn -based continuous prediction model for in hospital aki and show applicable model interpretations in relation to clinical decision support methods study populations were all patients aged 18 years or older who were hospitalized for more than 48 hours between 2013 and 2017 in 2 tertiary hospitals in korea seoul national university bundang hospital and seoul national university hospital all demographic data laboratory values vital signs and clinical conditions of patients were obtained from electronic health records of each hospital we developed 2 stage hierarchical prediction models model 1 and model 2 using rnn algorithms the outcome variable for model 1 was the occurrence of aki within 7 days from the present model 2 predicted the future trajectory of creatinine values up to 72 hours the performance of each developed model was evaluated using the internal and external validation data sets`
- gold: `clinical decision support cds` → pred: `clinical decision support for the diagnosis and management of adult and pediatric hypertension purpose of review to review literature from 2016 to 2019 on clinical decision support cds for diagnosis and management of hypertension in children and adults recent findings ten studies described hypertension cds systems novel advances included the integration of patient collected blood pressure data automated information retrieval and management support and use of cds in low resource developing world settings and in pediatrics findings suggest that cds increases hypertension detection control yet many children and adults with hypertension remain undetected or undercontrolled cds challenges included poor usability from lack of health record integration excessive data entry requests and wireless connectivity challenges and lack of clinician trust in blood pressure measures hypertension cds has improved but not closed gaps in the detection and control of hypertension in children and adults the studies reviewed indicate that the usability of cds and the system where cds is deployed e g commitment to high quality blood pressure measurement infrastructure may impact cds 's ability to increase hypertension detection and control`
- gold: `learning health system` → pred: `a nice perspective on computable biomedical knowledge introduction the national institute for health and care excellence nice plays a central role in the nhs we distill knowledge of best practice from the best available sources of evidence and share this across the health and care system typically in the form of recommendations we want to ensure that this knowledge is shared in a form that supports improved decision making by professionals working together with patients leading to improved outcomes understanding the role of computable knowledge in the context of a learning health system is therefore of deep interest to nice methods the agency for healthcare research and quality ahrq 4 levels of knowledge have been used as a framework to review current nice products and services and envisage how they may need to evolve discussion nice is mostly still at level 1 of the ahrq knowledge hierarchy but aspires to work towards structured and computable products the nhs long term plan makes clear that the wider health and care system is seeking to drive up interoperability with standards for data exchange at the heart of this nice connect is the name given to nice 's ambition to change in order to keep pace with changing technologies advances in guideline development and analytical methods and the shifting needs of the system and to ensure that it can sustainably and efficiently manage its portfolio of guidance it is seen as`
- gold: `clinical decision support systems cdsss` → pred: `clinical decision support systems for opioid prescribing for chronic non cancer pain in primary care a scoping review background and objectives clinical decision support systems cdsss may help clinicians prescribe opioids for chronic noncancer pain cncp more appropriately this scoping review determined the extent and range of the current evidence on cdsss for opioid prescribing for cncp in primary care and whether investigators followed best evidence and current guidance in designing implementing and evaluating these complex interventions methods we searched 9 electronic databases and other data sources for studies from january 1 2008 to october 11 2019 two reviewers independently screened the citations one reviewer extracted data and a second verified for accuracy inclusion criteria study of a cdss for opioid prescribing for cncp in a primary care clinical setting we reported quantitative results in tables and qualitative results in narrative form results our search yielded 5068 records of which 14 studies met our inclusion criteria all studies were conducted in the united states six studies examined local eg health center cdsss and 8 examined prescription drug monitoring program cdsss three cdsss incorporated evidence based components study aims were heterogeneous and study designs included both quantitative and qualitative methodologies no studies assessed patient health outcomes few studies appeared to be following guidance for evaluating complex interventions conclusions few studies`
- gold: `assessed` → pred: `rigorously assessed the use of cdsss for opioid prescribing for cncp in primary care settings going forward investigators should`
- gold: `fast healthcare interoperability resources fhir` → pred: `experience in developing an fhir medical data management platform to provide clinical decision support this paper is an extension of work originally presented to phealth 2019 16th international conference on wearable micro and nano technologies for personalized health to provide an efficient decision support it is necessary to integrate clinical decision support systems cdsss in information systems routinely operated by healthcare professionals such as hospital information systems hiss or by patients deploying their personal health records phr cdsss should be able to use the semantics and the clinical context of the data imported from other systems and data repositories a cdss platform was developed as a set of separate microservices in this context we implemented the core components of a cdss platform namely its communication services and logical inference components a fast healthcare interoperability resources fhir -based cdss platform addresses the ease of access to clinical decision support services by providing standard based interfaces and workflows this type of cdss may be able to improve the quality of care for doctors who are using his without cdss features the hl7 fhir interoperability standards provide a platform usable by all hiss that are fhir enabled the platform has been implemented and is now productive with a rule based engine processing around 50 000 transactions a day with more than 400 decision support models and a bayes`

### Abbreviation (69 total)
- missed gold: `use`
- missed gold: `gaps`
- missed gold: `fhir`
- missed gold: `fhir`
- missed gold: `gaps`
- missed gold: `plan`

### Nested Phrase (2303 total)
- gold: `demographic data laboratory values vital signs` → pred: `real time clinical decision support based on recurrent neural networks for in hospital acute kidney injury external validation and model interpretation background acute kidney injury aki is commonly encountered in clinical practice and is associated with poor patient outcomes and increased health care costs despite it posing significant challenges for clinicians effective measures for aki prediction and prevention are lacking previously published aki prediction models mostly have a simple design without external validation furthermore little is known about the process of linking model output and clinical decisions due to the black box nature of neural network models objective we aimed to present an externally validated recurrent neural network rnn -based continuous prediction model for in hospital aki and show applicable model interpretations in relation to clinical decision support methods study populations were all patients aged 18 years or older who were hospitalized for more than 48 hours between 2013 and 2017 in 2 tertiary hospitals in korea seoul national university bundang hospital and seoul national university hospital all demographic data laboratory values vital signs and clinical conditions of patients were obtained from electronic health records of each hospital we developed 2 stage hierarchical prediction models model 1 and model 2 using rnn algorithms the outcome variable for model 1 was the occurrence of aki within 7 days from the present model 2 predicted the future trajectory of creatinine values up to 72 hours the performance of each developed model was evaluated using the internal and external validation data sets`
- missed gold: `clinical decision support`
- missed gold: `recurrent neural networks`
- missed gold: `external validation`
- missed gold: `model interpretation`
- missed gold: `patient outcomes`
