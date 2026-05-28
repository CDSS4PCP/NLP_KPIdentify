import argparse
import psycopg2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.utils.database_params import database_params
from src.nlp.classes.nlp_ops import nlp_ops

def run(args):
    database_conn_obj = database_params()
    params = database_conn_obj.config()
    conn = psycopg2.connect(**params)
    
    nlp_ops_obj = nlp_ops(conn)
    if args.op == "process":
        nlp_ops_obj.process_data()
    elif args.op == "train":
        nlp_ops_obj.train_models()
    else:
        print(f"Operation {args.op} is not implemented.")
        
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NLP Operations Pipeline")
    parser.add_argument("--op", type=str, choices=["process", "train"], default="process", help="NLP operation to perform")
    args = parser.parse_args()
    run(args)
