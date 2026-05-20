from src.utils.database_params import database_params
from src.data_pipeline.pubmed.classes.parse_pubmed_xml_and_insert_raw_data import parse_pubmed_xml_and_insert_raw_data
import psycopg2

database_conn_obj = database_params()
# Obtain the configuration parameters
params = database_conn_obj.config()
# Connect to the PostgreSQL database
conn = psycopg2.connect(**params)

parse_pubmed_xml_and_insert_raw_data_obj= parse_pubmed_xml_and_insert_raw_data(conn)

parse_pubmed_xml_and_insert_raw_data_obj.parse_and_insert_raw_data()

conn.close()

