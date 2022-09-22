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
from modules import utils
from modules import createDataset as data
from modules import preProcessData as ppd

# Get the absolute path under the current working directory
WORKING_PATH = os.getcwd()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keyphrase extraction using hierAttn-BiLSTM-CRF")

    parser.add_argument('--mode','-m', default='train', type=str, help='Mode of opertion: train/test/testgs/predict/createData')
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
    parser.add_argument("--minSentences", "-minSentences", default=3, help="Minimum Sentences in Each Text")
    parser.add_argument("--filterKP","-filterKP", default=False, help="Filter KP generation for DISEASE/GPE/HEALTH/MEDICATION")
    
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
        with open(os.path.join(config.JSON_DATA,"testgs91.json"), "w") as outfile:
            json.dump(gs91Data, outfile)

        print("Saving GS42: ", len(gs42Data))
        with open(os.path.join(config.JSON_DATA,"testgs42.json"), "w") as outfile:
            json.dump(gs42Data, outfile)

        dataset_length = len(totalData)
        print("Saving Train: ", dataset_length//3)
        with open(os.path.join(config.JSON_DATA,"train.json"), "w") as outfile:
            json.dump(totalData[:dataset_length//3], outfile)
        print("Saving Test: ", dataset_length-dataset_length//3)
        with open(os.path.join(config.JSON_DATA,"test.json"), "w") as outfile:
            json.dump(totalData[dataset_length//3:], outfile)  

        pass
    elif args.mode == "train":
        pass
    elif args.mode == "test":
        pass
    elif args.mode == "testGS":
        pass
    else:
        print("Invalid option selected!!!\n Mode of opertion: train/test/predict/createData")