import spacy
import unidecode
from word2number import w2n
# from pycontractions import Contractions
import gensim.downloader as api
import json

class text_preprocessing:
    def __init__(self):

        self.nlp = spacy.load('en_core_web_sm')

        # Choose model accordingly for contractions function
        self.model = api.load("glove-twitter-25")
        # model = api.load("glove-twitter-100")
        # model = api.load("word2vec-google-news-300")

#         self.cont = Contractions(kv_model=self.model)
#         self.cont.load_models()

        # exclude words from spacy stopwords list
        deselect_stop_words = ['no', 'not']
        for w in deselect_stop_words:
            self.nlp.vocab[w].is_stop = False
    


    def remove_whitespace(self,text):
        """remove extra whitespaces from text"""
        text = text.strip()
        return " ".join(text.split())


    def remove_accented_chars(self,text):
        """remove accented characters from text, e.g. café --> cafe"""
        text = unidecode.unidecode(text)
        return text


    def expand_contractions(self,text):
        """expand shortened words, e.g. don't to do not"""
        text = list(self.cont.expand_texts([text], precise=True))[0]
        return text


    def call_preprocessing(self, text, accented_chars=True, contractions=True, 
                           convert_num=True, extra_whitespace=True, 
                           lemmatization=True, lowercase=True, punctuations=True, 
                           remove_num=True, special_chars=True, 
                           stop_words=True):
        """preprocess text with default option set to true for all steps"""

        if extra_whitespace == True: #remove extra whitespaces
            text = self.remove_whitespace(text)
        if accented_chars == True: #remove accented characters
            text = self.remove_accented_chars(text)
        if contractions == True: #expand contractions
            pass
#             text = self.expand_contractions(text)
        if lowercase == True: #convert all characters to lowercase
            text = text.lower()

        doc = self.nlp(text) #tokenise text
        #print(doc)
        clean_text = []

        #remove_unwanted_dict={'objective'}

        for token in doc:
            #print(token)
            flag = True
            edit = token.text
            '''
            #remove unwanted like objective, methods
            if token.text in remove_unwanted_dict:
                flag = False
            '''

            # remove stop words
            if stop_words == True and token.is_stop and token.pos_ != 'NUM': 
                flag = False
            # remove punctuations
            if punctuations == True and token.pos_ == 'PUNCT' and flag == True: 
                flag = False
            # remove special characters
            if special_chars == True and token.pos_ == 'SYM' and flag == True: 
                flag = False
            # remove numbers
            if remove_num == True and (token.pos_ == 'NUM' or token.text.isnumeric()) and flag == True:
                flag = False
            # convert number words to numeric numbers
            if convert_num == True and token.pos_ == 'NUM' and flag == True:
                edit = w2n.word_to_num(token.text)
            # convert tokens to base form
            elif lemmatization == True and token.lemma_ != "-PRON-" and flag == True:
                edit = token.lemma_
            # append tokens edited and not removed to list 
            if edit != "" and flag == True:
                clean_text.append(edit)        
        return clean_text
