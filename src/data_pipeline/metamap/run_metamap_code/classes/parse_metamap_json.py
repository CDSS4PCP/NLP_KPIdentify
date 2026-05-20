import json

class parse_metamap_json:
    def __init__(self):
        pass

    '''
    This function returns the list of preferred name for the candidates for the input file.
    The input file should be in json format wiz is output of metamap.

    nested levels:

    -AllDocuments
    --Document
    ---Utterances
    ----Phrases
    -----Mappings
    ------MappingCandidates
    -------CandidatePreferred

    '''
    def get_CandidatePreferred(self,file):

        with open(file) as f:
            data = json.load(f)

        final_CandidateMatched_dict={}

        for document in data['AllDocuments']:
            pmid=0
            inner_CandidateMatched={}
 
            for utterance in document['Document']['Utterances']:
                pmid=utterance['PMID']
                for phrase in utterance['Phrases']:
                    for mapping in phrase['Mappings']:
                        for candidate in mapping['MappingCandidates']:
                            inner_CandidateMatched[candidate['CandidateMatched']]=[candidate['CandidatePreferred'], candidate['CandidateCUI'], candidate['CandidateScore']]

            final_CandidateMatched_dict[pmid]=inner_CandidateMatched
        return final_CandidateMatched_dict
