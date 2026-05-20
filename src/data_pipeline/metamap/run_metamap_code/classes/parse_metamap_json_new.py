import json

class parse_metamap_json_new:
    def __init__(self, text_preprocessing_obj):
        self.text_preprocessing_obj = text_preprocessing_obj

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

        for document in data['AllDocuments'][:10]:
            pmid=0
            inner_CandidateMatched={}
            for utterance in document['Document']['Utterances']:
                pmid=utterance['PMID']
                for phrase in utterance['Phrases']:
                    for mapping in phrase['Mappings']:
                        for candidate in mapping['MappingCandidates']:
                            CandidateMatched = ' '.join(self.text_preprocessing_obj.call_preprocessing(candidate['CandidateMatched']))
                            if CandidateMatched == '':
                                continue
                            CandidatePreferred = candidate['CandidatePreferred']
                            if CandidateMatched in inner_CandidateMatched:
                                cur_dict=inner_CandidateMatched[CandidateMatched]
                                if CandidatePreferred not in cur_dict:
                                    cur_dict[CandidatePreferred] = [candidate['CandidateCUI'], candidate['CandidateScore']]
                            else:
                                inner_CandidateMatched[CandidateMatched]={CandidatePreferred : [candidate['CandidateCUI'], candidate['CandidateScore']]}
                            
            final_CandidateMatched_dict[pmid]=inner_CandidateMatched
        return final_CandidateMatched_dict
