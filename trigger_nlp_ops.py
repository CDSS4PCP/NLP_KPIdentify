from metamap.run_metamap_code.classes.parse_metamap_json_new import parse_metamap_json_new
from nlp.classes.text_preprocessing import text_preprocessing
from nlp.classes.get_current_gs_dump import get_current_gs_dump
from nlp.classes.load_models import load_models
from nlp.classes.calc_cosine_top_n_class import calc_cosine_top_n_class
from nlp.classes.insert_metamap_all_entities import insert_metamap_all_entities
from utils.database_params import database_params
import psycopg2

text_preprocessing_obj = text_preprocessing()
parse_metamap_json_new_obj = parse_metamap_json_new(text_preprocessing_obj)

parsed_metamap_out = parse_metamap_json_new_obj.get_CandidatePreferred('/home/rgoli/MetaMap-src/data/metamap_data/metamap_results/metamap_processed_test_out_medline.json')
print(len(parsed_metamap_out))
#print(parsed_metamap_out)

database_conn_obj = database_params()
# Obtain the configuration parameters
params = database_conn_obj.config()
# Connect to the PostgreSQL database
conn = psycopg2.connect(**params)

#get gs dump
get_current_gs_dump_obj=get_current_gs_dump(conn)
gs_list=get_current_gs_dump_obj.get_dump()

#preprocess gs
gs_list_preprocessed=[]
for item in gs_list:
    gs_list_preprocessed.append((text_preprocessing_obj.call_preprocessing(item[0]), item[1]))

print(len(gs_list_preprocessed))

#load w2v and phrase model
load_models_obj=load_models()
w2v_model, phrase_model = load_models_obj.load()

#compute top n
calc_cosine_top_n_class_obj=calc_cosine_top_n_class()
answer_dict = calc_cosine_top_n_class_obj.calc_cosine_top_n(parsed_metamap_out, gs_list_preprocessed, w2v_model, phrase_model)
print(len(answer_dict))
print("Final Answer:\n=============================\n")
print(answer_dict)

#Insert into metamap_all_entities
#insert_metamap_all_entities_obj = insert_metamap_all_entities(conn)
#insert_metamap_all_entities_obj.run_insert(answer_dict, parsed_metamap_out)
#print('Insertion complete')

conn.close()


