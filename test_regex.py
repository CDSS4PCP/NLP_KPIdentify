import re
import nltk
import string
import unidecode
import contractions
import copy
from nltk import sent_tokenize, word_tokenize
# from nlp.classes.text_preprocessing import text_preprocessing

english_punctuations = [',', '.', ':', ';', '``','?', '（','）','(', ')',
                '[', ']', '&', '!', '*', '@', '#', '$', '%','\\','\"','}','{','=','/','>','<']

english_punctuations_arr= ''.join(english_punctuations)

stop_words = nltk.corpus.stopwords.words('english')

#deselect 'no' and 'not' from stop words
stop_words.remove('no')
stop_words.remove('not')

print(stop_words)

# text_preprocessing_obj = text_preprocessing()

sentence = "India won world cup in 2011 on July-7th at 23:54 or 07/07/2011 at 48.5 overs. We have $100 Dollar's in BofA account to validate the special charcter's #given by awesome text/sentence processing! Using a pre-post design, project measures included six stroke management goals as defined by the National Institute of Neurological Disorders and Stroke and three clinical decision support measures based on entry of orders used to trigger documentation reminders for nursing: (1) the National Institutes of Health's Stroke Scale, (2) neurological checks, and (3) dysphagia screening. Data were reviewed 6 months prior (n = 2293) and 6 months following the intervention (n = 2588). The effects of the decision support alerts on the completeness of nursing documentation were not statistically significant (likely due to lack of order entry). For example, an order for the National Institutes of Health Stroke Scale was entered only 10.7% of the time, which meant no alert would fire for nursing in the postintervention group. METHODS This was a retrospective study of adult ED visits admitted to the hospital meeting criteria for sepsis from October 2013 to October 2014. Sepsis was defined as meeting criteria for systemic inflammatory response syndrome with an infectious admitting diagnosis in the ED. ED visits were randomly partitioned into an 80%/20% split for training and validation. A random forest model (machine learning approach) was constructed using over 500 clinical variables from data available within the EHRs of four hospitals to predict in-hospital mortality. RESULTS There were 5,278 visits among 4,676 unique patients who met criteria for sepsis. Of the 4,222 patients in the training group, 210 (5.0%) died during hospitalization, and of the 1,056 patients in the validation group, 50 (4.7%) died during hospitalization. The AUCs with 95% confidence intervals (CIs) for the different models were as follows: random forest model, 0.86 (95% CI = 0.82 to 0.90); CART model, 0.69 (95% CI = 0.62 to 0.77); logistic regression model, 0.76 (95% CI = 0.69 to 0.82); CURB-65, 0.73 (95% CI = 0.67 to 0.80); MEDS, 0.71 (95% CI = 0.63 to 0.77); and mREMS, 0.72 (95% CI = 0.65 to 0.79). The random forest model AUC was statistically different from all other models (p ≤ 0.003 for all comparisons). OBJECTIVE We hypothesized that a daily rounding checklist and a computerized order entry (CPOE) rule that limited the scheduling of complete blood cell counts and chemistry and coagulation panels to a 24-hour interval would reduce laboratory utilization and associated costs. METHODS We performed a retrospective analysis of these initiatives in a pediatric cardiovascular ICU (CVICU) that included all patients with congenital or acquired heart disease admitted to the cardiovascular ICU from September 1, 2008, until April 1, 2011.RESULTS We found a reduction in laboratory utilization frequency in the checklist intervention period and additional reduction in the CPOE intervention period [complete blood count: 31% and 44% (P < .0001); comprehensive chemistry panel: 48% and 72% (P < .0001); coagulation panel: 26% and 55% (P < .0001); point of care blood gas: 43% and 44% (P < .0001)] compared with the preintervention period. Projected yearly cost reduction was $717,538.8. There was no change in adjusted mortality rate (odds ratio 1.1, 95% confidence interval 0.7-1.9, P = .65). CVICU and total length of stay (days) was similar in the pre- and postintervention periods. café --> cafe unaccented string. RESULTS In free-text comments written in response to NFM alerts, prescribers provided more than 1150 unique reasons to justify formulary deviation. The compiled reasons were analyzed and grouped into nine categories through the iterative process, with a high degree of interrater agreement (κ = 0.989; 95% confidence interval, 0.985-0.992).I'll be there within 5 min. Shouldn't you be there too? I'd love to see u there my dear. It's awesome to meet new friends. We've been waiting for this day for so long. I would like to meet new friend's."

sentence = contractions.fix(sentence)

for sent in sent_tokenize(sentence):
#     sent2 = copy.copy(sent)
    
    ## Convert sentence to lowercase and strip whitespaces
    sent = sent.lower().strip()
    print(sent) 
    
    ## Convert unicode characters in sentence to ASCII
    sent = unidecode.unidecode(sent)
    sent = sent.encode("ascii", "ignore").decode()
    
    ## Remove URL's from Sentence
    sent = re.sub('http[s]?://\S+', '', sent)
    
    ## Remove words like 2.0-2
    sent = re.sub('\d+\.*\d*\-+\d+\.*\d*', ' ', sent)
    
    # Remove punctuation characters
    sent = sent.translate(str.maketrans(english_punctuations_arr,' '*len(english_punctuations_arr)))
    
    # Remove Stop Words
    words = [word for word in word_tokenize(sent) if not word in stop_words]
    
    # Remove punctuation only strings from sentence
    words = [word for word in words if not all(c in string.punctuation for c in word) and len(word)>1]
    
    # Remove Numericals from sentence
    words = [x for x in words if not all(c.isdigit() for c in x)] 
    
    print(words, end='\n\n')
    
#     print(text_preprocessing_obj.call_preprocessing(sent2,contractions=False), end='\n\n')
    