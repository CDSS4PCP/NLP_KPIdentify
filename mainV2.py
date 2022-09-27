#################################
## Author: Rohan Goli
## Usage: Experiment with model training/testing and prediction using Document-level attention by Hierarchical Attention BiLSTM-CRF
## Date: 09/21/22
#################################

import argparse
import configV2 as config
import os
import shutil
import time
import sys
import json

import gensim
from gensim.models import KeyedVectors

from modules import utils
from modules import createDataset as data
from modules import preProcessData as ppd

from modules.languageModel import LanguageModel, WordLSTM_v2, Trainer, EmbeddingsReader
from modules.hierAttnNtwk import BiLSTM_CRF, hierAttnNtwkTrainer

import numpy as np

import torch
torch.manual_seed(1)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Get the absolute path under the current working directory
WORKING_PATH = os.getcwd()
BI_LM_MODEL_FILE = "BiLM.pt"
WORD_EMBED_FILE = 'LM_word2vec.bin'
BILSTMCRF_MODEL_NAME = 'hierAttn-BiLSMT-CRF'
START_TAG = "<START>"
STOP_TAG = "<STOP>"
EMBEDDING_DIM = 300
DROPOUT = 0.2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keyphrase extraction using hierAttn-BiLSTM-CRF")

    parser.add_argument('--mode','-m', default='train', type=str, help='Mode of opertion: train/test/testgs/predict/createData/preTrain')
    parser.add_argument('--sections','-s', default=['title','abstract'], type=str, nargs='+', help='Sections in research paper to include: title/abstract/methods/results')
    parser.add_argument('--features','-f', default=['CEM','WFOF','POS','LEN','TI','TR'], type=str, nargs='+',
                        help=("Features to include:",
                        "CEM - Char Embeddings",
                        "DEM - Document Embeddings",
                        "PEM - Phrase Embeddings",
                        "TI - TFIDF(Term Frequency Inverse Document Frequency)",
                        "TR - Text Rank",
                        "TopR - Topic Rank",
                        "PosR - Position Rank "
                        "MR - Multi-partite Rank",
                        "WFOT - Word First Occurence in Text",
                        "LEN - Length of word",
                        ))
    parser.add_argument("--stem", "-stem",default="no",help="Vocabulary Stemming - yes/no")
    parser.add_argument("--minSentences", "-minSentences", default=3, help="CreateSynthDS :::: Minimum Sentences in Each Text")
    parser.add_argument("--filterKP","-filterKP", default=False, help="CreateSynthDS :::: Filter KP generation for DISEASE/GPE/HEALTH/MEDICATION")
    parser.add_argument("-seqLen","--seqLength", type=int, default = 5, help="BiLM :::: To create Train Dataset with sequence length sliding window over sentence. Deafult(5)")
    
    args = parser.parse_args()

    print("="*100)
    print("Mode: {}".format(args.mode))
    print("="*100)

    json_data_folder = os.path.join(WORKING_PATH, config.JSON_DATA)
    if not os.path.exists(json_data_folder): os.mkdir(json_data_folder)
    interim_data_folder = os.path.join(WORKING_PATH, config.INTERIM_DATA)
    if not os.path.exists(interim_data_folder): os.mkdir(interim_data_folder)

    if args.mode == "createData":
        ## Read PubMed XML processed Data - For all CDSS
        pubmed_data_folder = os.path.join(WORKING_PATH, config.PUBMED_PROCESSED_DATA)
        fullData = data.load_pubmed_data(pubmed_data_folder)

        pubmed_data_folder = os.path.join(WORKING_PATH, config.PUBMED_PROCESSED_DATA_GS)
        test42Abstracts = data.load_pubmed_data(pubmed_data_folder)

        ## Read Manual Formatted JSON ACM Data - 12
        miscData = utils.read_json_array(os.path.join(config.DATA_FOLDER,"ACM_MiscPubMed_Abstracts.json"))

        ## Generate JSON Files from XML
        data.generate_synthetic_dataset(
            fullData+test42Abstracts,
            json_data_folder,
            min_sentences=args.minSentences,
            filter_kp=args.filterKP,
            model_name=os.path.join(WORKING_PATH,"cdssSciSpacy/model-best"),
            additional_data = miscData
            )

        ## Annotated GS Labels
        GS_DATA_FILES = ["4Rohan_FirstAnnotationResults_GS_CleanedAfter.txt", "4Rohan_SecondTimeGS.txt", "4Rohan_ACM_GS.txt"]
        testGSAbs = []
        Labels = ["First-Time","Second-Time","Second-Time ACM"]
        for idx, datFile in enumerate(GS_DATA_FILES):
            with open(os.path.join(WORKING_PATH, config.DATA_FOLDER, datFile),'r') as f:
                testGSAbs.append(f.read().split('\n\n'))
            print("{} GS: {}".format(Labels[idx],len(testGSAbs[-1])))

        ## Read Synthetic Labeled Data
        trainData = utils.read_json_array(os.path.join(config.JSON_DATA, "train.json"))
        testData = utils.read_json_array(os.path.join(config.JSON_DATA, "test.json"))
        totalData = trainData + testData

        ## Read GS Labels - 42 GS
        gs42Abs = {}
        for abstract in testGSAbs[0]:
            temp = abstract.split('\n')
            gs42Abs[temp[0].split(':')[1]] = temp[1:]
        ## Read GS Labels - 91 GS
        gs91Abs = {}
        for abstract in testGSAbs[1]:
            temp = abstract.split('\n')
            gs91Abs[temp[0].split(':')[1]] = temp[1:]
        ## Read GS Labels - 8 ACM GS
        for abstract in testGSAbs[2]:
            temp = abstract.split('\n')
            gs91Abs[temp[0]] = temp[1:]        
        
        ## Remove GS Data from totalData
        ## 1. FULL DATA with Synthetic Labels
        ## 2. Replace Synthetic with GS
        count = 0
        gs91Data = []
        gs42Data = []
        visited = set()
        i=0
        j=0
        print("Total data length: ", len(totalData))
        while i<len(totalData):
            abstract = totalData[i]
            if abstract['id'] in gs91Abs and abstract['id'] not in visited:
                abstract['keywords'] = gs91Abs[abstract['id']]
                gs91Data.append(abstract)
                visited.add(abstract['id'])
                count+=1
            elif abstract['id'] in gs42Abs and abstract['id'] not in visited:
                abstract['keywords'] = gs42Abs[abstract['id']]
                gs42Data.append(abstract)
                visited.add(abstract['id'])
                count+=1
            else:
                totalData[i] = totalData[j]
                j+=1
            i+=1
        totalData[j:]=[]
        
        ## Write JSON Data
        print("Saving GS91: ", len(gs91Data))
        utils.save_json(gs91Data, os.path.join(config.JSON_DATA,"testgs91.json"))

        print("Saving GS42: ", len(gs42Data))
        utils.save_json(gs42Data, os.path.join(config.JSON_DATA,"testgs42.json"))

        dataset_length = len(totalData)
        print("Saving Train: ", dataset_length//3)
        utils.save_json(totalData[:dataset_length//3],os.path.join(config.JSON_DATA,"train.json"))

        print("Saving Test: ", dataset_length-dataset_length//3)
        utils.save_json(totalData[dataset_length//3:],os.path.join(config.JSON_DATA,"test.json"))
        pass

    elif args.mode == "preTrain":
        ###############
        ## Load Data ##
        ###############
        trainData = utils.read_json_array(os.path.join(config.JSON_DATA, "train.json"))
        testData = utils.read_json_array(os.path.join(config.JSON_DATA, "test.json"))

        ## Store All Sentences of Corpus
        train_corpus_sentences = []
        for x in trainData:
            train_corpus_sentences.extend(x['sentences'])
        print("Total Sentences in Train Corpus: ", len(train_corpus_sentences))
        test_corpus_sentences = []
        for x in testData:
            test_corpus_sentences.extend(x['sentences'])
        print("Total Sentences in Test Corpus: ", len(test_corpus_sentences))

        ## Total Data
        total_corpus_sentences = train_corpus_sentences+test_corpus_sentences

        ############################
        ## Create Word Embeddings ##
        ############################
        modelW2V = gensim.models.Word2Vec(
                    sentences=total_corpus_sentences,
                    vector_size=300, window=5,
                    min_count=0,workers=10,
                    sg=1,seed=42,compute_loss=True
                    )
        
        ## Save Word Embeddings
        modelW2V.wv.save_word2vec_format(os.path.join(config.INTERIM_DATA,WORD_EMBED_FILE), binary=True)

        ## Load Word Embeddings
        modelW2V = KeyedVectors.load_word2vec_format(os.path.join(config.INTERIM_DATA,WORD_EMBED_FILE), binary=True)

        ## Create Integer-to-Token mapping
        int2token = {0:'<UNK>'}
        cnt = 1
        for word in modelW2V.key_to_index.keys():
            int2token[cnt] = word
            cnt+=1
        ## Create Token-to-Integer mapping
        token2int = {t: i for i, t in int2token.items()}

        ## Store Vocab Size - For further reference
        vocab_size = len(int2token)
        print("Vocabulary Size: {}".format(vocab_size))

        ## Save Int2Token and Token2Int mappings
        utils.save_json(token2int, os.path.join(config.INTERIM_DATA,"token2int.json"))
        utils.save_json(int2token, os.path.join(config.INTERIM_DATA,"int2token.json"))

        ##########################################
        ## Create Bi-Directional Language Model ##
        ##########################################
        lang_model = LanguageModel(token2int=token2int)

        ## Create Data Input/Targets for BiLM
        def splitData_Input_Targets(csLM, corpus_sents, token2int):
            ## Create Sequences
            sequences = [csLM.create_seq(i, seq_len=args.seqLength) for i in corpus_sents]
            ## Merge list-of-lists into a single list
            sequences = sum(sequences, [])

            ## Split Data into Input/Target text
            inputs, targets = [], []
            for sequence in sequences:
                ## Split Sentence into Tokens
                seqTokens = sequence.split()
                ## Convert Text Sequences to Integer Sequences
                seqInts = csLM.get_integer_seq(seqTokens, tokenized=True)
                
                if len(seqInts) != args.seqLength+1:
                    continue
                
                inputs.append(seqInts[:-1])
                targets.append(seqInts[1:])
            return np.array(inputs, dtype="int32"),np.array(targets, dtype="int32")

        x_train, y_train = splitData_Input_Targets(lang_model, train_corpus_sentences, token2int)
        x_test, y_test = splitData_Input_Targets(lang_model, test_corpus_sentences, token2int)

        ## Initiate Bi-LM Network
        biLMNet = WordLSTM_v2(
            n_layers = 1,
            bidirection = True,
            pretrainedWE = os.path.join(config.INTERIM_DATA,WORD_EMBED_FILE),
            vocab = token2int
            )

        ## Move Bi-LM Network to GPU
        biLMNet.cuda()
        print("Bi-Directional Language Model :")
        print(biLMNet)

        ## Initiate Trainer
        trainer = Trainer(
            token2int=token2int,
            int2token=int2token,
            X_train = x_train,
            y_train = y_train,
            X_test = x_test,
            y_test = y_test
            )

        ## Initiate BiLM Training
        trainer.train(
            biLMNet,
            batch_size = 64,
            epochs=20
            )

        ## Save BiLM Model
        trainer.saveModel(
            biLMNet,
            os.path.join(config.INTERIM_DATA,BI_LM_MODEL_FILE)
        )

        print(trainer.sample(biLMNet, 45, prime = "clinical decision support systems"),"\n")
        print(trainer.sample(biLMNet, 45, prime = "prescription errors"),"\n")
        print(trainer.sample(biLMNet, 45, prime = "one of the"),"\n")
        print(trainer.sample(biLMNet, 45, prime = "asthma management programs for primary care providers increasing adherence to asthma guidelines"),"\n")
        
        # (pytorch) [rgoli@node1397 NLP_KPIdentify]$ python mainV2.py -m preTrain
        # Word Embedding Type:  word2vec
        # ====================================================================================================
        # Mode: preTrain
        # ====================================================================================================
        # Total Sentences in Train Corpus:  13603
        # Total Sentences in Test Corpus:  22766
        # Vocabulary Size: 5043
        # /home/rgoli/.local/lib/python3.8/site-packages/torch/nn/modules/rnn.py:62: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.3 and num_layers=1
        #   warnings.warn("dropout option adds dropout after all but last "
        # Bi-Directional Language Model :
        # WordLSTM_v2(
        #   (emb_layer): Embedding(5043, 300)
        #   (lstm): LSTM(300, 128, batch_first=True, dropout=0.3, bidirectional=True)
        #   (dropout): Dropout(p=0.3, inplace=False)
        #   (fc): Linear(in_features=256, out_features=5043, bias=True)
        # )
        # Epoch: 1/20... mean_loss : 0.88, Perplexity : 2.41
        # Epoch: 2/20... mean_loss : 0.23, Perplexity : 1.26
        # Epoch: 3/20... mean_loss : 0.15, Perplexity : 1.17
        # Epoch: 4/20... mean_loss : 0.11, Perplexity : 1.11
        # Epoch: 5/20... mean_loss : 0.07, Perplexity : 1.08
        # Epoch: 6/20... mean_loss : 0.05, Perplexity : 1.06
        # Epoch: 7/20... mean_loss : 0.04, Perplexity : 1.04
        # Epoch: 8/20... mean_loss : 0.03, Perplexity : 1.03
        # Epoch: 9/20... mean_loss : 0.03, Perplexity : 1.03
        # Epoch: 10/20... mean_loss : 0.02, Perplexity : 1.02
        # Epoch: 11/20... mean_loss : 0.02, Perplexity : 1.02
        # Epoch: 12/20... mean_loss : 0.02, Perplexity : 1.02
        # Epoch: 13/20... mean_loss : 0.02, Perplexity : 1.02
        # Epoch: 14/20... mean_loss : 0.01, Perplexity : 1.02
        # Epoch: 15/20... mean_loss : 0.01, Perplexity : 1.01
        # Epoch: 16/20... mean_loss : 0.01, Perplexity : 1.01
        # Epoch: 17/20... mean_loss : 0.01, Perplexity : 1.01
        # Epoch: 18/20... mean_loss : 0.01, Perplexity : 1.01
        # Epoch: 19/20... mean_loss : 0.01, Perplexity : 1.01
        # Epoch: 20/20... mean_loss : 0.01, Perplexity : 1.01
        # Test Perplexity: 31.14
        # clinical decision support systems to healthcare smith data sources of the evidence the evidence and evidence statements evidence statements pertaining statements and pertaining to medication events addressing the medication profiles which were presented to phealth phealth phealth health questionnaire pssuq network ssn network sensor data transfer tasks tasks e.g. 

        # prescription errors of review of evidence and current guidance on safe for medication use as an ehr an electronic medical electronic medical records medical record ehr medical ehr data is known for their use of the studies studies appeared could get a individualized therapy therapy and therapy 

        # one of the gl-dss of gl-dss of multiple than when than than 48 between 2013 between groups considered the interaction probability prespecification analysis is vital values increased in increased to increased to increased in children with minor head trauma and mht among among people among people can sustainably 

        # asthma management programs for primary care providers increasing adherence to asthma guidelines designed in need to our services to detect potential drug-drug potential to potential drug-drug interactions or discussed are currently represented without without external without any without ct without ct scan ct scan results no difference in terms between stakeholders and often and 3 and often
        
        pass

    elif args.mode == "train":
        trainData = utils.read_json_array(os.path.join(config.JSON_DATA, "train.json"))
        testData = utils.read_json_array(os.path.join(config.JSON_DATA, "test.json"))

        ## Load Word Embeddings
        modelW2V = KeyedVectors.load_word2vec_format(os.path.join(config.INTERIM_DATA,WORD_EMBED_FILE), binary=True)

        ## Create Integer-to-Token mapping
        ix_to_word = {0:'<UNK>'}
        cnt = 1
        for word in modelW2V.key_to_index.keys():
            ix_to_word[cnt] = word
            cnt+=1
        ## Create Token-to-Integer mapping
        word_to_ix = {t: i for i, t in ix_to_word.items()}

        ## Store Vocab Size - For further reference
        vocab_size = len(ix_to_word)
        print("Vocabulary Size: {}".format(vocab_size))

        ## Load Word Embeddings Binary
        word_embeddings = EmbeddingsReader.from_binary(
            filename = os.path.join(config.INTERIM_DATA,WORD_EMBED_FILE),
            vocab = word_to_ix
            )

        tag_to_ix = {"O": 0, "B-KP": 1, "I-KP": 2, START_TAG: 3, STOP_TAG: 4}
        ix_to_tag = {0:"O", 1: "B-KP", 2: "I-KP", 3: "O", 4: "O"}

        biLSTM_CRF_model = BiLSTM_CRF(
            vocab_size = len(word_to_ix),
            tag_to_ix = tag_to_ix,
            embedding_dim = EMBEDDING_DIM,
            dropout = DROPOUT,
            use_pretrained_embd=word_embeddings
            )
        
        hierAttnNtwk_trainer = hierAttnNtwkTrainer(
            model = biLSTM_CRF_model,
            train_data = trainData,
            test_data = testData,
            biLM_path = os.path.join(config.INTERIM_DATA,BI_LM_MODEL_FILE),
            word_to_ix = word_to_ix,
            tag_to_ix = tag_to_ix
        )
        hierAttnNtwk_trainer.train()
        hierAttnNtwk_trainer.saveModel(os.path.join(config.INTERIM_DATA, BILSTMCRF_MODEL_NAME))
        pass

    elif args.mode == "test":
        testData = utils.read_json_array(os.path.join(config.JSON_DATA, "test.json"))
        pass
    elif args.mode == "testGS":
        pass
    else:
        print("Invalid option selected!!!\n Mode of opertion: train/test/predict/createData")