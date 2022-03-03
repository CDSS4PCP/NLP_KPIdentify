import argparse
import os
from modules import createDataset as data
from modules import preProcessData as ppd
import config
import logging

# Get the absolute path under the current working directory
WORKING_PATH = os.getcwd()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Keyphrase extraction using BiLSTM-CRF and AL")
    
    parser.add_argument('--mode','-m', default='train', type=str, help='Mode of opertion: train/test/predict')
    parser.add_argument('--sections','-s', default=['title','abstract'], type=str, nargs='+', help='Sections in research paper to include: title/abstract/methods/results')
    parser.add_argument('--features','-f', default=['CEM','WFOF','POS','LEN'], type=str, nargs='+', help='Features to include: Char Embeddings (CEM), Document Embeddings (DEM), Phrase Embeddings (PEM), TFIDF (Term Frequency - Inverse Document Frequency), Text Rank (TextR), Topic Rank (TopR), Position Rank (PosR), Multi-partite Rank (MR), Word First Occurence in Text (WFOT), Length of word (LEN)')
    parser.add_argument("--log", "-log",default="warn",
                        help=("Provide logging level. "
                              "Example --log debug', default='warning'"))
    
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
    print("Logging Level: {}".format(args.log))
    print("="*100)
    
    pubmed_data_folder = os.path.join(WORKING_PATH, config.PUBMED_PROCESSED_DATA)
    json_data_folder = os.path.join(WORKING_PATH, config.JSON_DATA)
    if not os.path.exists(json_data_folder): os.mkdir(json_data_folder)
    interim_data_folder = os.path.join(WORKING_PATH, config.INTERIM_DATA)
    if not os.path.exists(interim_data_folder): os.mkdir(interim_data_folder)

    if args.mode=="predict":
        ## Inteference Mode
        ## Take JSON document as input
        ## Pre-Process JSON with Data Features
        ## Load pre-trained model
        ## Infer/Predict
        pass
    elif args.mode=='al':
        ## Activate Active Learning
        ## Pick test sample from Test Data Pool
        ## Incremental Train with Active Learning
        pass
    elif args.mode == "test":
        ## Metrics Calculation
        pass
    elif args.mode == "createData":
        ## Read PubMed XML processed Data
        fullData = data.load_pubmed_data(pubmed_data_folder)
        ## Generate JSON Files from XML
        data.generate_dataset(fullData, json_data_folder)
    else:
        ## Build Data Features with JSON Data
        ppd.build_data_sets(json_data_folder, args.sections, interim_data_folder)