import argparse
import psycopg2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.utils.database_params import database_params
from src.nlp.classes.insert_gs import insert_gs

def run(args):
    database_conn_obj = database_params()
    params = database_conn_obj.config()
    conn = psycopg2.connect(**params)
    
    if args.type == "gs":
        insert_gs_obj = insert_gs(conn)
        insert_gs_obj.insert_data()
    else:
        print(f"Data insertion for {args.type} is not implemented.")
        
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Insertion Pipeline")
    parser.add_argument("--type", type=str, choices=["gs", "raw"], default="gs", help="Data type to insert")
    args = parser.parse_args()
    run(args)
