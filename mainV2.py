#################################
## Author: Rohan Goli
## Usage: Experiment with model training/testing and prediction using Document-level attention by Hierarchical Attention BiLSTM-CRF
## Date: 09/21/22
#################################

import argparse
import config
import os
import shutil
import time
import sys
from modules import utils
from modules import createDataset as data
from modules import preProcessData as ppd

# Get the absolute path under the current working directory
WORKING_PATH = os.getcwd()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keyphrase extraction using hierAttn-BiLSTM-CRF")

    parser.add_argument('--mode','-m', default='train', type=str, help='Mode of opertion: train/test/testgs/predict/createData')

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

        with open(os.path.join(WORKING_PATH, config.DATA_FOLDER, "4Rohan_FirstAnnotationResults_GS_CleanedAfter.txt"),'r') as f:
            test42Abs = f.read().split('\n\n')
        print(len(test42Abs))

        with open(os.path.join(WORKING_PATH, config.DATA_FOLDER,"4Rohan_SecondTimeGS.txt"),'r') as f:
            test80Abs = f.read().split('\n\n')
        print(len(test80Abs))

        with open(os.path.join(WORKING_PATH, config.DATA_FOLDER,"4Rohan_ACM_GS.txt"),'r') as f:
            testACM = f.read().split('\n\n')
        print(len(testACM))

        sys.exit(0)
        ## Remove HoldOut Data from Fulltext
        pmids_HO = utils.read_text(config.HOLDOUT_DATA)
        
        ## Remove GS Data from Fulltext
        # pmids_HO =  set([paper['pmid'] for paper in testGSAbstracts])
        # pmids_fulltext = set([paper['pmid'] for paper in fullData])
        # # print(len(pmids_fulltext))
        # removeGS_pmids_fulltext = pmids_fulltext - pmids_HO
        # # print(len(removeGS_pmids_fulltext))
        
        N=len(fullData)
        i=0
        j=0
        while i<N:
            if fullData[i]['pmid'] not in pmids_HO:
                fullData[j]=fullData[i]
                j+=1
            i+=1
        fullData[j:]=[]
        
        ## Generate JSON Files from XML
        data.generate_synthetic_dataset(fullData, json_data_folder, min_sentences=args.minSentences, filter_kp=args.filterKP)

        pass
    elif args.mode == "train":
        pass
    elif args.mode == "test":
        pass
    elif args.mode == "testGS":
        pass
    else:
        print("Invalid option selected!!!\n Mode of opertion: train/test/predict/createData")