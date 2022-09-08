from metamap.run_metamap_code.classes.parse_metamap_json import parse_metamap_json
from nlp.classes.get_current_gs_dump import get_current_gs_dump
from nlp.classes.text_preprocessing import text_preprocessing
from utils.database_params import database_params
import psycopg2

database_conn_obj = database_params()
# Obtain the configuration parameters
params = database_conn_obj.config()
# Connect to the PostgreSQL database
conn = psycopg2.connect(**params)

#0. get gold standard dump
get_current_gs_dump_obj = get_current_gs_dump(conn)
gs_terms=get_current_gs_dump_obj.get_dump()
print(gs_terms[:10])

#1. preprocess gold standard
text_preprocessing_obj = text_preprocessing()
preprocessed_gs_terms = []

for term in gs_terms[:10]:
    pre_term = ' '.join(text_preprocessing_obj.call_preprocessing(term[0]))
    preprocessed_gs_terms.append((pre_term,term[1]))

print(preprocessed_gs_terms)


#2. Preprocess metamap entities
parse_metamap_json_obj=parse_metamap_json()

dict_out=parse_metamap_json_obj.get_CandidatePreferred('/home/rgoli/MetaMap-src/data/metamap_data/metamap_results/metamap_processed_full_data.json')
print(len(dict_out))

preprocessed_dict_out={}
for k,v in dict_out['33787612'].items():
    pre_k=' '.join(text_preprocessing_obj.call_preprocessing(k))
    preprocessed_dict_out[pre_k]=v

print(preprocessed_dict_out)





conn.close()
