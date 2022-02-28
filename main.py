import argparse
import os
from modules import preProcessData

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
    
    if mode=="predict":
        pass
    elif mode == "test":
        pass
    else:
        