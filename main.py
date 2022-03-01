import argparse
import os
from modules import createDataset as data
from modules import preProcessData as ppd
import config

# Get the absolute path under the current working directory
WORKING_PATH = os.path.dirname(os.getcwd())

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Keyphrase extraction using BiLSTM-CRF and AL")
    
    parser.add_argument('--mode','-m', default='train', type=str, help='Mode of opertion: train/test/predict')
    parser.add_argument('--sections','-s', default=['title','abstract'], type=str, nargs='+', help='Sections in research paper to include: title/abstract/methods/results')
    parser.add_argument('--features','-f', default=['CEM','TFIDF','TextR','WFOT','LEN'], type=str, nargs='+', help='Features to include: Char Embeddings (CEM), Document Embeddings (DEM), Phrase Embeddings (PEM), TFIDF (Term Frequency - Inverse Document Frequency), Text Rank (TextR), Topic Rank (TopR), Position Rank (PosR), Multi-partite Rank (MR), Word First Occurence in Text (WFOT), Length of word (LEN)')
    
    args = parser.parse_args()
    
    print("+"*50)
    print("Mode: {}".format(args.mode))
    print("Sections Included: {}".format(args.sections))
    print("Features: {}".format(args.features))
    print("+"*50)
    
    pubmed_data_folder = os.path.join(WORKING_PATH, config.PUBMED_PROCESSED_DATA)
    json_data_folder = os.path.join(WORKING_PATH, config.JSON_DATA)
    if not os.path.exists(json_data_folder): os.mkdir(json_data_folder)
    interim_data_folder = os.path.join(WORKING_PATH, config.INTERIM_DATA)
    if not os.path.exists(interim_data_folder): os.mkdir(interim_data_folder)

    if args.mode=="predict":
        pass
    elif args.mode == "test":
        pass
    elif args.mode == "createData":
        fullData = data.load_pubmed_data(pubmed_data_folder)
        data.generate_dataset(fullData, json_data_folder)
    else:
        ppd.build_data_sets(json_data_folder, args.sections, interim_data_folder)