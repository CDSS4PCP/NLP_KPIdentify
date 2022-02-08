from utils.database_params import database_params
from nlp.classes.insert_gs import insert_gs
import psycopg2

database_conn_obj = database_params()
# Obtain the configuration parameters
params = database_conn_obj.config()
# Connect to the PostgreSQL database
conn = psycopg2.connect(**params)

insert_gs_obj= insert_gs(conn)

insert_gs_obj.insert_data()

conn.close()

