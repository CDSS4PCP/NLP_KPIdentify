import bisect
from src.nlp.classes.get_mean_vector_class import get_mean_vector_class
from src.nlp.classes.calc_cosine_similarity_class import calc_cosine_similarity_class

class calc_cosine_top_n_class:
    def __init__(self):
        self.get_mean_vector_class_obj= get_mean_vector_class()
        self.calc_cosine_similarity_class_obj = calc_cosine_similarity_class()

    def calc_cosine_top_n(self, input_metamap_dict, gs_list_preprocessed, w2v_model, phrase_model, top_n=3):
        answer_dict={}
        for pmid, all_entities in input_metamap_dict.items():
            print("\nPMID: ", pmid, "\n=====================")
            terms_cosine_score_dict={}
            for candidate_matched,parameters in all_entities.items():
                candidate_phrase=phrase_model[candidate_matched.split(' ')]
                print("Candidate Phrase: ", candidate_phrase)
                term_vector = self.get_mean_vector_class_obj.get_mean_vector(w2v_model, candidate_phrase)
                #print("Term Vector", term_vector)
                if str(term_vector) == 'vocab not present' or str(term_vector) =='nothing':
                    continue

                for gold in gs_list_preprocessed:
                    gold_phrase = phrase_model[gold[0]]
                    GS_mean_vector = self.get_mean_vector_class_obj.get_mean_vector(w2v_model, gold_phrase)
                    if str(GS_mean_vector) == 'vocab not present' or str(GS_mean_vector) =='nothing':
                        continue

                    #print(GS_mean_vector)
                    cos_sim_score = self.calc_cosine_similarity_class_obj.calc_cosine_similarity(term_vector,GS_mean_vector)
                    print(gold_phrase, candidate_phrase, cos_sim_score)

                    if candidate_matched in terms_cosine_score_dict:
                        #print(terms_cosine_score_dict[' '.join(candidate)])

                        if len(terms_cosine_score_dict[candidate_matched][0]) < top_n:
                            cur_list_of_scores = terms_cosine_score_dict[candidate_matched][0]
                            insertion_point = bisect.bisect(cur_list_of_scores, cos_sim_score)
                            bisect.insort(cur_list_of_scores, cos_sim_score)
                            terms_cosine_score_dict[candidate_matched][0] = cur_list_of_scores
                            #updating gold standard
                            cur_list_of_gold_standard = terms_cosine_score_dict[candidate_matched][1]
                            cur_list_of_gold_standard.insert(insertion_point, ' '.join(gold_phrase))                  
                            terms_cosine_score_dict[candidate_matched][1] = cur_list_of_gold_standard

                            #print(cur_list_of_gold_standard,updated_gold_standard)

                        else:
                            cur_list_of_scores = terms_cosine_score_dict[candidate_matched][0]
                            if cos_sim_score > cur_list_of_scores[0]:
                                insertion_point = bisect.bisect(cur_list_of_scores, cos_sim_score)
                                bisect.insort(cur_list_of_scores, cos_sim_score)
                                terms_cosine_score_dict[candidate_matched][0] = cur_list_of_scores[-top_n:]
                                #updating gold_standard
                                cur_list_of_gold_standard = terms_cosine_score_dict[candidate_matched][1]
                                cur_list_of_gold_standard.insert(insertion_point, ' '.join(gold_phrase))
                                terms_cosine_score_dict[candidate_matched][1] = cur_list_of_gold_standard[-top_n:]
                            else:
                                continue

                    else:
                        terms_cosine_score_dict[candidate_matched] = [[cos_sim_score], [ ' '.join(gold_phrase)]]

                '''
                for candidate_preferred, inside_parameters in parameters.items():
                    print(candidate_preferred, inside_parameters)
                    #phrase_model[candidate_preferred]
                '''
                answer_dict[pmid] = terms_cosine_score_dict
        return answer_dict
