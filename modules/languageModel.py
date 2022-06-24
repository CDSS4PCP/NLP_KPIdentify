import argparse
import json 
import os

import spacy
import scispacy
from scispacy.linking import EntityLinker
import pubmed_parser as pp
from tqdm import tqdm

from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
import unidecode
import contractions
import string
import re

import utils

# Get the absolute path under the current working directory
WORKING_PATH = os.getcwd()

DATA_FOLDER = 'data'
PUBMED_PROCESSED_DATA = 'data/pubmed_data/processed_data/processed_full_data.xml'
PUBMED_PROCESSED_DATA_GS = 'data/pubmed_data/processed_data/processed_44_abstracts_test.xml'
HOLDOUT_DATA = 'data/HoldOut_Total.txt'
JSON_DATA = 'data/pubmed_data/json_data_synthetic_labels'
PRE_PROCESSED_DATA = 'data/pubmed_data/preprocess_data'
INTERIM_DATA = 'interim_data/'
VOCAB = INTERIM_DATA+'/vocab/'
MODEL_FOLDER = INTERIM_DATA+'/models/'
RESULT_FOLDER = INTERIM_DATA+'results/'

# json_data_folder = os.path.join(WORKING_PATH, JSON_DATA)
# if not os.path.exists(json_data_folder): os.mkdir(json_data_folder)
# interim_data_folder = os.path.join(WORKING_PATH, INTERIM_DATA)
# if not os.path.exists(interim_data_folder): os.mkdir(interim_data_folder)

stop_words = stopwords.words('english')

#deselect 'no' and 'not' from stop words
stop_words.remove('no')
stop_words.remove('not')

english_punctuations = [',', '.', ':', ';', '``','?', '（','）','(', ')',
                '[', ']', '&', '!', '*', '@', '#', '$', '%','\\','\"','}','{','=','/','>','<','|','+','_','~']

english_punctuations_arr= ''.join(english_punctuations)

class LanguageModel:
    
    def __init__(self):
        self.nlp = spacy.load("en_core_sci_lg")
        self.nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})

        self.raw_data = None
        self.processed_data = None

    def load_pubmed_data(self,path):
        '''
        Load PubMed XML parsed Data with PMIDS
        '''
        self.raw_data = pp.parse_medline_xml(path,
                                    year_info_only=False,
                                    nlm_category=False,
                                    author_list=False,
                                    reference_list=False)

        return self.raw_data

    def sent2words(self, sent):
        '''Pre-process sentence text to words'''
        
        ## Expand Words
        sent = contractions.fix(sent)
        
        ## Convert sentence to lowercase and strip whitespaces
        sent = sent.lower().strip()
        
        ## Convert unicode characters in sentence to ASCII
        sent = unidecode.unidecode(sent)
        sent = sent.encode("ascii", "ignore").decode()
        
        ## Remove URL's from Sentence
        sent = re.sub('http[s]?://\S+', '', sent)
        
        ## Remove words like 2.0-2
        sent = re.sub('\d+\.*\d*\-+\d+\.*\d*', ' ', sent)
        
        # Remove punctuation characters
        sent = sent.translate(str.maketrans(english_punctuations_arr,' '*len(english_punctuations_arr)))
        
        pos, length = {}, {}
        words = word_tokenize(sent)
        for i, (w, p) in enumerate(pos_tag(words)):
            # Computational features
            pos[w] = p
            length[w] = len(w)
        
        # Remove Stop Words
        words = [word for word in word_tokenize(sent) if not word in stop_words]
        
        # Remove punctuation only strings from sentence
        words = [word for word in words if not all(c in string.punctuation for c in word) and len(word)>1]
        
        # Remove Numericals from sentence
        words = [x for x in words if not all(c.isdigit() for c in x)] 
        
        ## Return words, POS tags, lengths of words, processed sentence
        return words, pos, length, ' '.join(words)

    def generate_synthetic_dataset(self, fullData, predictData=False, min_sentences=3, filter_kp = False):
        '''
        Create Train & Test Datasets as JSON with Synthetic Keywords
        '''

        if filter_kp:
            nlp2 = spacy.load('en_ner_bc5cdr_md')
            nlp2.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})

        outlier_kws=[
        'http','www','university','department','antibiotic','antimicrobial','institute','ministry', 'pubmed',
        '.gov','.org','.com','.edu','.net',
        'city','disease','injury','trauma','syndrome','country','national','regimen','swelling','cholesterol','cerebrovascular','leukemia'
        'surgery', 'medication','infection','stroke','diabetes','bleeding','comorbid','java','python',
        "united states",'united kingdom','india','china','germany','france','ghana','australia','italy','england','japan',
        'english','spanish','french','british','spain'
        ]

        comb_arr=[]
        pmid_arr =[]
        dataset = []
        p_id=0
        total_len = len(fullData)
        with tqdm(enumerate(fullData),total=total_len) as pbar1:
            for index, paper in pbar1:
        # for paper in fullData:
                comb_arr.append(paper['title']+' '+paper['abstract'])
                pmid_arr.append(paper['pmid'])
                data = {}
                data["id"] = paper['pmid']
                data["title"] = paper['title']
                data["abstract"] = paper['abstract']
                data["methods"] = ""
                data["results"] = ""
                dataset.append(data)
                p_id += 1
                pbar1.set_description("JSON pre-processing is completed for %s-th document!"%(p_id))

        if predictData==True:
            with open(os.path.join(json_data_path, "testgs.json"), "w") as outfile:
                json.dump(dataset, outfile)
            return True
                
        idx=0
        remove_sent_no_outliers = []
        with tqdm(self.nlp.pipe(comb_arr),total=total_len) as pbar1:
            # for doc in nlp.pipe(comb_arr):
            for doc in pbar1:
                # text = [token.orth_ for token in doc if not token.is_punct | token.is_space] 
                sents = [" ".join([token.orth_.lower() for token in sent if not token.is_punct | token.is_space]) for sent in doc.sents]
                sents = [self.sent2words(sent)[0] for sent in sents]
                text = [token.orth_ for token in doc if not token.is_punct | token.is_space] 

                ## Skip documents without minimum sentences
                if len(sents)<min_sentences:
                    remove_sent_no_outliers.append(idx)
                    idx+=1
                    continue

                kws = [str(x) for x in doc.ents]

                ## Filter KWS for DISEASES/GPE/Institutes
                if filter_kp:
                    rule_out_ents = [str(_) for _ in nlp2(comb_arr[idx]).ents]
                    rule_out_ents = [_ for _ in rule_out_ents if not _.isupper()]
                    if rule_out_ents!=[]:
                        kws = [_ for _ in kws if _ not in rule_out_ents]
                    kws = [_ for _ in kws if all([True if n_ not in _.lower() else False for n_ in outlier_kws])]

                kws.sort(reverse=True, key=len)
                
                dataset[idx]['fullText'] = text
                dataset[idx]["keywords"]= kws
                dataset[idx]['sentences'] = sents
                idx+=1
                pbar1.set_description("Synthetic Keywrods generated for %s-th document!"%idx)

        ## Filter Docs with less than minimum senetences
        i=0
        j=0
        print("Total Articles removed: ",len(remove_sent_no_outliers))
        print([pmid_arr[x] for x in remove_sent_no_outliers])
        while i<idx:
            if i not in remove_sent_no_outliers:
                dataset[j]=dataset[i]
                j+=1
            i+=1
        dataset[j:]=[]

        return dataset

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Language Model Experiments")

    parser.add_argument('-bd','--bidirection', type=bool, help="Uni/Bi-Directional Context. Options: [True/False]", default=True)
    parser.add_argument('-w','--wordEmbdType', type=str, help="Word Embedding Type. Options: [simple, fastText, Word2Vec]", default="simple")
    parser.add_argument("--minSentences", "-minSentences", default=3, help="Minimum Sentences in Each Text")
    parser.add_argument("--filterKP","-filterKP", default=False, help="Filter KP generation for DISEASE/GPE/HEALTH/MEDICATION")

    args = parser.parse_args()

    print('='*50)
    print('Context: {}\nWord Embedding: {}'.format(args.bidirection, args.wordEmbdType))
    print('='*50)

    lm = LanguageModel()

    ## Read PubMed XML processed Data - For all CDSS
    pubmed_data_folder = os.path.join(WORKING_PATH, PUBMED_PROCESSED_DATA)
    fullData = lm.load_pubmed_data(pubmed_data_folder)

    ## Remove HoldOut Data from Fulltext
    pmids_HO = utils.read_text(HOLDOUT_DATA)
    
    N=len(fullData)
    i=0
    j=0
    while i<N:
        if fullData[i]['pmid'] not in pmids_HO:
            fullData[j]=fullData[i]
            j+=1
        i+=1
    fullData[j:]=[]
    
    ## Processed Data
    processed_data = lm.generate_synthetic_dataset(fullData, min_sentences=args.minSentences, filter_kp=args.filterKP)
    
    dataset_length = len(processed_data)

    train_data = processed_data[:dataset_length//3]
    test_data = processed_data[dataset_length//3:]

    train_corpus_sentences = []
    for x in train_data:
        train_corpus_sentences.extend(x['sentences'])
    print("Total Sentences in Train Corpus: ", len(train_corpus_sentences))

    test_corpus_sentences = []
    for x in test_data:
        test_corpus_sentences.extend(x['sentences'])
    print("Total Sentences in Test Corpus: ", len(test_corpus_sentences))

    print('Sample: ', train_corpus_sentences[0])