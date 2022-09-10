import json
import unidecode
import contractions
from nltk import sent_tokenize, word_tokenize
import nltk
import logging
import re
import string
import spacy
from sklearn.metrics import confusion_matrix
from seqeval.metrics import classification_report, accuracy_score, f1_score, recall_score, precision_score
from seqeval.scheme import IOB2

logger = logging.getLogger(__name__)
stop_words = nltk.corpus.stopwords.words('english')
#deselect 'no' and 'not' from stop words
stop_words.remove('no')
stop_words.remove('not')

## Do not remove '.' ',' ';' ':'
english_punctuations = ['``','?', '（','）','(', ')',
                '[', ']', '&', '!', '*', '@', '#', '$', '%','\\','\"','}','{','=','/','>','<','|','+','_','~']
english_punctuations_arr= ''.join(english_punctuations)

