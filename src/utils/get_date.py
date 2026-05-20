import psycopg2
import pandas as pd
from src.utils.database_params import database_params


class get_date:
    def __init__(self, date_type='B'):
        self.query_string="select cur_execution_date from dates where date_type='"+date_type+"';"
        
    def run_query(self):
        
        database_conn_obj = database_params()
        # Obtain the configuration parameters
        params = database_conn_obj.config()
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # Create a new cursor
        cur = conn.cursor()

        # A function that takes in a PostgreSQL query and outputs a pandas database 
        def create_pandas_table(sql_query, database = conn):
            table = pd.read_sql_query(sql_query, database)
            return table
        # Utilize the create_pandas_table function to create a Pandas data frame
        # Store the data as a variable
        tables = create_pandas_table(self.query_string)
        #print(tables)

        # Close the cursor and connection to so the server can allocate
        # bandwidth to other requests
        cur.close()
        conn.close()
        
        return tables
