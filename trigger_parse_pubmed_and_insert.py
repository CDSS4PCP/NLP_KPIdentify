from data_extraction.pubmed.classes.parse_pubmed_and_insert import parse_pubmed_and_insert
from utils.database_params import database_params
import psycopg2

database_conn_obj = database_params()
# Obtain the configuration parameters
params = database_conn_obj.config()
# Connect to the PostgreSQL database
conn = psycopg2.connect(**params)

parse_pubmed_and_insert_obj=parse_pubmed_and_insert(conn)
#values_list=parse_pubmed_and_insert_obj.parse_xml_csv('/home/rgoli/MetaMap-src/data/ubmed_data/processed_data/processed_test_out.xml')
#print(values_list)
parse_pubmed_and_insert_obj.insert_data('/home/rgoli/MetaMap-src/data/pubmed_data/processed_data/processed_test_out.xml')

conn.close()


