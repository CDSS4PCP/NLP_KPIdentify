import argparse
import os
import shutil
import time
from modules import createDataset as data
from modules import preProcessData as ppd
from modules import model as model
from modules import utils
import config
import logging

# Get the absolute path under the current working directory
WORKING_PATH = os.getcwd()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Keyphrase extraction using BiLSTM-CRF and AL")
    
    parser.add_argument('--mode','-m', default='train', type=str, help='Mode of opertion: train/test/testgs/predict/createData')
    parser.add_argument('--sections','-s', default=['title','abstract'], type=str, nargs='+', help='Sections in research paper to include: title/abstract/methods/results')
    parser.add_argument('--features','-f', default=['CEM','WFOF','POS','LEN','TI','TR'], type=str, nargs='+',
                        help=("Features to include:",
                        "CEM - Char Embeddings",
                        "DEM - Document Embeddings",
                        "PEM - Phrase Embeddings",
                        "TFIDF - (Term Frequency Inverse Document Frequency)",
                        "TextR - Text Rank",
                        "TopR - Topic Rank",
                        "PosR - Position Rank "
                        "MR - Multi-partite Rank",
                        "WFOT - Word First Occurence in Text",
                        "LEN - Length of word",
                        ))
    parser.add_argument("--log", "-log",default="warn",
                        help=("Provide logging level. "
                              "Example --log debug', default='warning'"))
    parser.add_argument("--stem", "-stem",default="no",help="Vocabulary Stemming - yes/no")
    
    args = parser.parse_args()
    
    levels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
    }
    
    level = levels.get(args.log.lower())
    if level is None:
        raise ValueError(
            f"log level given: {args.log}"
            f" -- must be one of: {' | '.join(levels.keys())}")
    logging.basicConfig(level=level)
    logger = logging.getLogger(__name__)
    
    print("="*100)
    print("Mode: {}".format(args.mode))
    print("Sections Included: {}".format(args.sections))
    print("Features: {}".format(args.features))
    print("Vocab Stemming: {}".format(args.stem))
    print("Logging Level: {}".format(args.log))
    print("="*100)
    
    
    json_data_folder = os.path.join(WORKING_PATH, config.JSON_DATA)
    if not os.path.exists(json_data_folder): os.mkdir(json_data_folder)
    interim_data_folder = os.path.join(WORKING_PATH, config.INTERIM_DATA)
    if not os.path.exists(interim_data_folder): os.mkdir(interim_data_folder)
        
    # Fields contained in the dataset
    corpus_type = "".join([i[0] for i in args.sections]).upper()

    if args.mode=="testgs":
        s_time = time.time()
        ## Inteference Mode
        ## Take JSON document as input - 44 Abstracts
        pubmed_data_folder = os.path.join(WORKING_PATH, config.PUBMED_PROCESSED_DATA_GS)
        test44Abstracts = data.load_pubmed_data(pubmed_data_folder)
        data.gen_gs_dataset(test44Abstracts, json_data_folder)
        
        ## Pre-Process JSON with Data Features
        ppd.build_testgs_data_set(json_data_folder, args.sections, interim_data_folder, args.stem)
        
        ## Load pre-trained model
        ## Infer/Predict on Test Gold Standard
        model.testgs(interim_data_folder,corpus_type, args.mode, args.features)
        print("\033[031mINFO: Total time of model training:%sS\033[0m"%round(time.time() - s_time, 3))
        pass
    elif args.mode == "predict":
        
        total_data = utils.read_json_array(os.path.join(WORKING_PATH,"dummy.json"))
        for article in total_data:
            ppd.build_infer_data_set(article, args.sections, interim_data_folder, args.stem)
            kps = model.predict_kws(interim_data_folder, corpus_type, args.mode, args.features)
            act_kps = article['actual_keywords']
            act_kps.sort(reverse=True, key=len)
            
            print("GoldStandard Keywords:\n{}\nPredicted Keywords:\n{}\n\n".format(act_kps,kps))

    elif args.mode=='al':
        ## Activate Active Learning
        ## Pick test sample from Test Data Pool
        ## Incremental Train with Active Learning
        pass
    elif args.mode == "test":
        ## Metrics Calculation
        s_time = time.time()
        p, r, f1 = model.test(interim_data_folder, corpus_type, args.mode, args.features)
        print("\033[031mINFO: Total time of model test:%sS\033[0m"%round(time.time() - s_time, 3))
        pass
    elif args.mode == "createData":
        ## Read PubMed XML processed Data
        pubmed_data_folder = os.path.join(WORKING_PATH, config.PUBMED_PROCESSED_DATA)
        fullData = data.load_pubmed_data(pubmed_data_folder)
        ## Generate JSON Files from XML
        data.generate_dataset(fullData, json_data_folder)
    elif args.mode == "train":
        ## Build Data Features with JSON Data
        ppd.build_data_sets(json_data_folder, args.sections, interim_data_folder, args.stem)
        
        # start time
        s_time = time.time()
        model.train(interim_data_folder, corpus_type, args.features)
        
        print("\033[031mINFO: Total time of model training:%sS\033[0m"%round(time.time() - s_time, 3))
    else:
        print("Invalid option selected!!!\n Mode of opertion: train/test/predict/createData")