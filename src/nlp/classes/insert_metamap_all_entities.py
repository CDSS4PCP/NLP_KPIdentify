from datetime import datetime
import psycopg2
import psycopg2.extras as extras

class insert_metamap_all_entities:
    
    def __init__(self, conn, page_size=200):
        self.conn=conn
        self.page_size = page_size
        
    
    def generate_insert_values_list(self, answer_dict, dict_out):
        final_val_list=[]
        for pmid, entity_to_gold in answer_dict.items():
            metamap_entities = dict_out[pmid]

            for candidate_matched, scores in entity_to_gold.items():    
                for candidate_preferred, concept in metamap_entities[candidate_matched].items():

                    final_val_list.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'cdssadmin',
                                         concept[0], candidate_matched, candidate_preferred, int(concept[1]), scores[0][0], scores[0][1],
                                         scores[0][2], None, None, scores[1][0], scores[1][1], scores[1][2], None, None,
                                         'Abstract',pmid))
        
        return final_val_list
    
    def get_sequence_list(self, final_val_list, cursor):   
        get_sequences='''select nextval('metamap_all_entites_id') from generate_series(1,'''+str(len(final_val_list))+''')'''
        cursor.execute(get_sequences)
        sequences = cursor.fetchall()
        new_values_list=[]
        for value_tuple in final_val_list:
            value_tuple = sequences.pop(0) + value_tuple
            new_values_list.append(value_tuple)
            
        #cursor.close()
        return new_values_list
    
    def run_insert(self, answer_dict, dict_out):
        cursor = self.conn.cursor()
        final_val_list = self.generate_insert_values_list(answer_dict, dict_out)
        new_final_list = self.get_sequence_list(final_val_list, cursor)
        
        sql = """Insert into metamap_all_entites (id, sys_creation_date, sys_update_date, app_id, concept_id, candidate_matched,
        candidate_preferred, candidate_score, score_1, score_2, score_3, score_4, score_5, matched_gs_term_1_id, matched_gs_term_2_id, 
        matched_gs_term_3_id, matched_gs_term_4_id, matched_gs_term_5_id, text_type, other_id) values %s"""
        
        try:
            extras.execute_values(cursor, sql, new_final_list, page_size = self.page_size)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn.rollback()
            cursor.close()
            return 1
        print("execute_values() done")
        cursor.close()
