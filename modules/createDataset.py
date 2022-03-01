import json 
import os
import spacy
import scispacy
from scispacy.linking import EntityLinker
import pubmed_parser as pp
import tqdm

def load_pubmed_data(path):
    '''
    Load PubMed XML parsed Data with PMIDS
    '''
    data = pp.parse_medline_xml(path,
                                 year_info_only=False,
                                 nlm_category=False,
                                 author_list=False,
                                 reference_list=False)

    return data

def generate_dataset(fullData, json_data_path):
    '''
    Create Train & Test Datasets as JSON with Synthetic Keywords
    '''
    nlp = spacy.load("en_core_sci_lg")
    nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})

    comb_arr=[]
    pmid_arr =[]
    dataset = []
    p_id=0
    with tqdm(enumerate(fullData)) as pbar1:
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
            pbar1.set_description("The %s-th JSON pre-processing is completed! %s"%(p_id,index))
        
    idx=0
    with tqdm(enumerate(nlp.pipe(comb_arr))) as pbar1:
        # for doc in nlp.pipe(comb_arr):
        for index, doc in pbar1:
            # text = [token.orth_ for token in doc if not token.is_punct | token.is_space] 

            kws = [str(x) for x in doc.ents]
            kws.sort(reverse=True, key=len)
            
            dataset[idx]["keywords"]=kws
            idx+=1
            pbar1.set_description("Synthetic Keywrods generated for %s! %s %s"%(dataset["id"],p_id,index))

    dataset_length = len(dataset)
    with open(os.path.join(json_data_path, "train.json"), "w") as outfile:
        json.dump(dataset[:dataset_length//3], outfile)

    with open(os.path.join(json_data_path, "test.json"), "w") as outfile:
        json.dump(dataset[dataset_length//3:], outfile)  

# if __name__ == "__main__":
#     fullData = load_data()
#     generate_dataset(fullData)
#     return True