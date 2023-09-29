
from modules import utils
from modules.hierAttnNtwk import BiLSTM_CRF, hierAttnNtwkTrainer
import os
import configV2 as config
from modules.languageModel import LanguageModel, WordLSTM_v2, Trainer, EmbeddingsReader
import torch
from modules import createDataset as data
import random
import csv

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
NO_OF_ACTIVE_LEARNING_ITERATIONS = 4

random.seed(42)


def load_model():
    ## Read Vocabulary Mapping
    ix_to_word = utils.read_json_array(os.path.join(config.INTERIM_DATA,"int2token.json"))
    word_to_ix = utils.read_json_array(os.path.join(config.INTERIM_DATA,"token2int.json"))

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

    ## Initialize Model Architecture with Word Embeddings 
    biLSTM_CRF_model = BiLSTM_CRF(
        vocab_size = len(word_to_ix),
        tag_to_ix = tag_to_ix,
        embedding_dim = EMBEDDING_DIM,
        dropout = DROPOUT,
        use_pretrained_embd=word_embeddings
        )

    ## Initialize Model-Trainer with Model Architecture, Word Mappings
    hierAttnNtwk_trainer = hierAttnNtwkTrainer(
        model = biLSTM_CRF_model,
        train_data = None,
        test_data = None,
        biLM_path = os.path.join(config.INTERIM_DATA,BI_LM_MODEL_FILE),
        word_to_ix = word_to_ix,
        tag_to_ix = tag_to_ix,
        ix_to_tag = ix_to_tag
    )

    ## Load Best Model
    hierAttnNtwk_trainer.loadModel(os.path.join(config.INTERIM_DATA, BILSTMCRF_MODEL_NAME))

    return hierAttnNtwk_trainer


def get_doc_score(predict_data, hierAttnNtwk_trainer):        
    try:
        predict_data = data.generate_predict_dataset(
            predict_data,
            min_sentences=args.minSentences,
            filter_kp=args.filterKP,
            model_name=os.path.join(WORKING_PATH,"cdssSciSpacy/model-best")
            )
    except NameError:
        predict_data = data.generate_predict_dataset(
            predict_data,
            min_sentences=3,
            filter_kp=False,
            model_name=os.path.join(WORKING_PATH,"cdssSciSpacy/model-best")
            )

    predict_tags, sen_scores = hierAttnNtwk_trainer.getPredictionKP(predict_data, "Predict")
    
    predict_kps = utils.parse_tags(
        predict_data[0]['sentences'], predict_tags,
        infer=True
        )
    predict_kps.sort(reverse=True, key=len)
    
    predict_data[0]['actual_keywords'] = predict_kps

    return predict_data, sen_scores


def select_documents(gs91a_data, model):
    print("============ Started selecting Docs ====================")
    doc_per_iter = 4
    s = len(gs91a_data)
    doc_scores = []

    #hierAttnNtwk_trainer = load_model()
    
    for i in range(s):
        # score document
        doc_score_dic = {}
        _, doc_score = get_doc_score([gs91a_data[i]], model)
        doc_id = gs91a_data[i]['id']
        # doc_score_dic["score"] = doc_score.item()
        # doc_score_dic["id"] = doc_id
        doc_score_dic[doc_id] = doc_score.item()
        doc_scores.append(doc_score_dic)
    
    

    doc_scores = list(doc_scores)

    # sort the docs
    #sorted_doc_scores = dict(sorted(doc_scores, key = lambda item: item["id"]))
    sorted_doc_scores = sorted(doc_scores, key=lambda x: list(x.values())[0])

    print("sorted")
    # select first d documents, add the documents to Training data and remove them from gs91a_data
    docs_selected = []
    
    c = 0
    # for key, value in sorted_doc_scores.items():
    #     docs_selected.append(key)
    #     c = c+1
    #     if c == doc_per_iter:
    #         break

    for item in sorted_doc_scores:
        docs_selected.append(list(item.keys())[0])
        c = c+1
        if c == doc_per_iter:
            break
    
    print(len(docs_selected))
    print("============ End of selecting Docs ====================")
    return docs_selected
    

def get_updated_training_data(gs91a, model):
    docs_selected = select_documents(gs91a, model)
    additional_training_data = []
    s = len(gs91a)
    
    indices_to_pop = []

    for i in range(s):
        # remove them from gs91a
        
        if gs91a[i]['id'] in docs_selected:
            # add to gs91a[i] training data
            additional_training_data.append(gs91a[i])
            #pop from the gs91a
            #print(len(gs91a))
            #print(len(gs91a_new))
            #gs91a_new.pop(i)
            indices_to_pop.append(i)
        

    gs91a_new = [gs91a[i] for i in range(len(gs91a)) if i not in indices_to_pop]
    
    print('-------------')
    print(len(gs91a))
    print(len(gs91a_new))
    print(len(additional_training_data))
    print('-------------')

    return gs91a_new, additional_training_data


def retrain(trainData, gs91b, len_of_active_learning_data_pool, iter_number):
    print("========== Started retraining  ==============")
    
    testData = utils.read_json_array(os.path.join(config.JSON_DATA, "test.json"))

    ## Read Vocabulary Mapping
    ix_to_word = utils.read_json_array(os.path.join(config.INTERIM_DATA,"int2token.json"))
    word_to_ix = utils.read_json_array(os.path.join(config.INTERIM_DATA,"token2int.json"))
    
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

    ## Initialize Model Architecture with Word Embeddings 
    biLSTM_CRF_model = BiLSTM_CRF(
        vocab_size = len(word_to_ix),
        tag_to_ix = tag_to_ix,
        embedding_dim = EMBEDDING_DIM,
        dropout = DROPOUT,
        use_pretrained_embd=word_embeddings
        )
    
    ## Initialize Model-Trainer with Model Architecture, Word Mappings
    hierAttnNtwk_trainer = hierAttnNtwkTrainer(
        model = biLSTM_CRF_model,
        train_data = trainData,
        test_data = testData,
        biLM_path = os.path.join(config.INTERIM_DATA,BI_LM_MODEL_FILE),
        word_to_ix = word_to_ix,
        tag_to_ix = tag_to_ix,
        ix_to_tag = ix_to_tag
    )
    ## Start Training
    hierAttnNtwk_trainer.train()
    BILSTMCRF_MODEL_NAME = 'hierAttn-BiLSMT-CRF'

    ## Save Best Model
    hierAttnNtwk_trainer.saveModel(os.path.join(config.INTERIM_DATA, BILSTMCRF_MODEL_NAME+'_'+str(iter_number)))
    print("============== Saved the model ==================")    
    print("=============== Getting metrics on gs91b ================")

    ## Get Metrics on Test Data - GS91b
    test_p,test_r,test_f1,test_acc = hierAttnNtwk_trainer.getMetricsOnData(testData)
    gs91b_p,gs91b_r,gs91b_f1,gs91b_acc = hierAttnNtwk_trainer.getMetricsOnData(gs91b, "Test GS91b")

    with open('active_learning_results_1.csv', 'a', newline='') as csvfile:
        logwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        logwriter.writerow([iter_number, len_of_active_learning_data_pool, len(trainData), 'Test', len(testData), test_p, test_r, test_f1, test_acc])
        logwriter.writerow([iter_number, len_of_active_learning_data_pool, len(trainData), 'GS91b', len(gs91b), gs91b_p, gs91b_r, gs91b_f1, gs91b_acc])


    return hierAttnNtwk_trainer


def start_active_learning():
    gstest91 = utils.read_json_array(os.path.join(config.JSON_DATA, "testgs91.json"))
    data_points = list(range(1, 92))
    random.shuffle(data_points)
    gs91a = []
    
    for i in range(42):
        gs91a.append(gstest91[data_points[i] - 1])
    
    gs91b = []
    for i in range(42,91):
        gs91b.append(gstest91[data_points[i]-1])

    print("================ GS data divided ===================")
    print(len(gs91a))
    print(len(gs91b))

    trainData = utils.read_json_array(os.path.join(config.JSON_DATA, "train.json"))

    print("============== Loaded Intial training data ==========")
    print(len(trainData))

    with open('active_learning_results_1.csv', 'w', newline='') as csvfile:
            logwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([' Active learning Iteration','Active Learning Data pool Length','Train DS Length','Test DataSet','Test DS Length','Precision','Recall','F1Score','Accuracy',])

    
    prev_model = load_model()

    i = 1
    while i<=NO_OF_ACTIVE_LEARNING_ITERATIONS :
        print(f"======== started {i} active learning loop =================")
        
        len_of_active_learning_data_pool = len(gs91a)
        gs91a, additional_training_data = get_updated_training_data(gs91a, prev_model)
        
        del prev_model
        torch.cuda.empty_cache()
        
        print(f"============= len of gs91a and train set after {i} loop ================")
        print(len(gs91a))
        trainData.extend(additional_training_data)
        print(len(trainData))
        
        curr_model = retrain(trainData, gs91b , len_of_active_learning_data_pool, i)
        print(f"======== End of {i} active learning loop =================")
        i = i+1

        prev_model = curr_model
        print("updated prev_model")



if __name__ == "__main__":
    
    start_active_learning()


