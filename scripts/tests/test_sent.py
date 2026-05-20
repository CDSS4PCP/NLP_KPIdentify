
import json
import numpy as np
import os
import configV2 as config

def analyze_sentence_length():
    """
    Analyzes the training input sentences to find the min, max, median, and average length.
    """
    try:
        # Construct the path to the training data file
        train_data_path = os.path.join(config.JSON_DATA, "train.json")    
        # Get the absolute path of the project root
        project_root = os.path.abspath(os.path.dirname(__file__))
        # Construct the absolute path to the training data file
        absolute_train_data_path = os.path.join(project_root, train_data_path)
        print(f"Attempting to read training data from: {absolute_train_data_path}")
        with open(absolute_train_data_path, 'r') as f:
            train_data = json.load(f)
        sentence_lengths = []
        for item in train_data:
            if 'sentences' in item and isinstance(item['sentences'], list):
                for sentence in item['sentences']:
                    # Assuming each sentence is a list of words
                    sentence_lengths.append(len(sentence))
        if not sentence_lengths:
            print("No sentences found in the training data.")
            return
        min_length = np.min(sentence_lengths)
        max_length = np.max(sentence_lengths)
        median_length = np.median(sentence_lengths)
        avg_length = np.mean(sentence_lengths)
        print(f"Sentence Length Analysis:")
        print(f"  Min: {min_length}")
        print(f"  Max: {max_length}")
        print(f"  Median: {median_length}")
        print(f"  Average: {avg_length}")
    except FileNotFoundError:
        print(f"Error: The file was not found at the specified path.")
        print("Please ensure that the `data` directory is structured as expected and accessible.")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from the training data file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    analyze_sentence_length()
