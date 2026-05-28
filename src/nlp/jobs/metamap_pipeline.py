import argparse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.data_pipeline.metamap.run_metamap_code.classes.run_metamap import run_metamap

def run(args):
    run_metamap_obj = run_metamap()
    run_metamap_obj.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Metamap Pipeline")
    parser.add_argument("--mode", type=str, default="default", help="Metamap mode")
    args = parser.parse_args()
    run(args)
