import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import csv
import subprocess
import spacy
import torch
import numpy as np
from tqdm import tqdm
from nltk import sent_tokenize
from seqeval.metrics import classification_report, accuracy_score, f1_score, recall_score, precision_score
from seqeval.scheme import BILOU, IOBES
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from src.nlp.experiments.base import BaseExperiment
from src.nlp.utils.io import read_json_array
from src.nlp.data.preprocessor import TextPreprocessor
from src.core import configV2 as config

class ScispacyExperiment(BaseExperiment):
    def __init__(self, config_dict):
        super().__init__("ScispacyExperiment", config_dict)
        self.preprocessor = TextPreprocessor()
        self.nlp = None

    def create_bert_tsv(self, data, filename):
        with open(filename, 'w', encoding="utf-8") as f:
            pass
        for article in data:
            textData = []
            for sent in sent_tokenize(article['title'] + ' ' + article['abstract']):
                words, _, _, _ = self.preprocessor.sent2words(sent)
                textData.append(' '.join(words))
            _, mapper, tokens = self.preprocessor.mark_keyword_all_sentences(article['keywords'], textData)
            with open(filename, 'a', encoding="utf-8") as f:
                print("-DOCSTART- -X- O O", file=f)
                for sentM, sentT in zip(mapper, tokens):
                    for wordM, wordT in zip(sentM, sentT):
                        print(f"{wordT}\t{wordM}", file=f)

    def prepare_data(self):
        print("Preparing data for ScispacyExperiment...")
        WORKING_PATH = os.getcwd()
        
        # Determine dataset paths from config
        json_dir = os.path.join(WORKING_PATH, config.JSON_DATA)
        gs42_path = os.path.join(json_dir, "testgs42.json")
        gs91_path = os.path.join(json_dir, "testgs91.json")
        
        if not os.path.exists(gs42_path) or not os.path.exists(gs91_path):
            # Fallback to alternative directory if needed
            json_dir = os.path.join(WORKING_PATH, "data/pubmed_data/json_data_synthetic_labels")
            gs42_path = os.path.join(json_dir, "v2_testgs42.json")
            gs91_path = os.path.join(json_dir, "v2_testgs91.json")
            
        print(f"Loading datasets:\n  - GS42: {gs42_path}\n  - GS91: {gs91_path}")
        gs42_data = read_json_array(gs42_path)
        gs91_data = read_json_array(gs91_path)
        gs_comb_data = gs42_data + gs91_data
        
        experiment_type = self.config.get("experiment_type", "gs42")
        seed = self.config.get("seed", 42)
        
        data_dir = os.path.join(WORKING_PATH, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        if experiment_type == "gs42":
            print(f"Using GS42 experimental setup (Seed: {seed})")
            # 52 Train/Val + 91 Test (test_size = 91/133 = 0.684)
            gs_train_val, gs_test = train_test_split(gs_comb_data, test_size=0.684, random_state=seed)
            gs_train, gs_val = train_test_split(gs_train_val, test_size=0.20, random_state=seed)
            
            self.train_tsv = os.path.join(data_dir, "gs42Spacy_T.tsv")
            self.val_tsv = os.path.join(data_dir, "gs42Spacy_V.tsv")
            self.train_spacy = os.path.join(data_dir, "gs42Spacy_T.spacy")
            self.val_spacy = os.path.join(data_dir, "gs42Spacy_V.spacy")
            self.train_json = os.path.join(data_dir, "gs42Spacy_T.json")
            self.val_json = os.path.join(data_dir, "gs42Spacy_V.json")
        else:
            print(f"Using GS66/CDSS experimental setup (Seed: {seed})")
            # 66 Train/Val + 67 Test (test_size = 0.50)
            gs_train_val, gs_test = train_test_split(gs_comb_data, test_size=0.50, random_state=seed)
            gs_train, gs_val = train_test_split(gs_train_val, test_size=0.20, random_state=seed)
            
            self.train_tsv = os.path.join(data_dir, "gs66Spacy_T.tsv")
            self.val_tsv = os.path.join(data_dir, "gs66Spacy_V.tsv")
            self.train_spacy = os.path.join(data_dir, "gs66Spacy_T.spacy")
            self.val_spacy = os.path.join(data_dir, "gs66Spacy_V.spacy")
            self.train_json = os.path.join(data_dir, "gs66Spacy_T.json")
            self.val_json = os.path.join(data_dir, "gs66Spacy_V.json")

        self.gs_test = gs_test
        print(f"Dataset split count:\n  - Train: {len(gs_train)}\n  - Validation: {len(gs_val)}\n  - Test: {len(gs_test)}")
        
        # Save splits as TSVs
        print("Generating training/validation TSV files...")
        self.create_bert_tsv(gs_train, self.train_tsv)
        self.create_bert_tsv(gs_val, self.val_tsv)
        
        # Convert TSV -> JSON -> Spacy binary formats
        print("Converting TSV files to JSON and .spacy formats...")
        try:
            # Convert train
            subprocess.run([
                sys.executable, "-m", "spacy", "convert",
                self.train_tsv, data_dir, "-t", "json", "-n", "1", "-c", "iob"
            ], check=True)
            subprocess.run([
                sys.executable, "-m", "spacy", "convert",
                self.train_json, data_dir, "-t", "spacy"
            ], check=True)
            
            # Convert val
            subprocess.run([
                sys.executable, "-m", "spacy", "convert",
                self.val_tsv, data_dir, "-t", "json", "-n", "1", "-c", "iob"
            ], check=True)
            subprocess.run([
                sys.executable, "-m", "spacy", "convert",
                self.val_json, data_dir, "-t", "spacy"
            ], check=True)
            print("Data conversion successfully completed.")
        except Exception as e:
            print(f"Error converting data formats: {e}")
            raise e

    def build_model(self):
        print("Filling spaCy configurations...")
        WORKING_PATH = os.getcwd()
        experiment_type = self.config.get("experiment_type", "gs42")
        
        temp_cfg = "tempSpacy42GS.cfg" if experiment_type == "gs42" else "tempSpacy66GS.cfg"
        temp_path = os.path.join(WORKING_PATH, "src/nlp/configs", temp_cfg)
        self.cfg_path = os.path.join(WORKING_PATH, "src/nlp/configs", "config.cfg")
        
        try:
            subprocess.run([
                sys.executable, "-m", "spacy", "init", "fill-config",
                temp_path, self.cfg_path
            ], check=True)
            print(f"Generated spaCy configuration file at {self.cfg_path}")
        except Exception as e:
            print(f"Error building model configurations: {e}")
            raise e

    def train(self):
        print("Training spaCy model...")
        WORKING_PATH = os.getcwd()
        experiment_type = self.config.get("experiment_type", "gs42")
        output_name = "sciSpacyGS42" if experiment_type == "gs42" else "cdssSciSpacyGS66"
        self.output_dir = os.path.join(WORKING_PATH, "outputs", "models", output_name)
        
        # Detect device configuration
        gpu_id = -1
        device_str = self.config.get("device")
        if device_str == "cuda" or (device_str is None and torch.cuda.is_available()):
            gpu_id = 0
            print("GPU detected. Training will run on GPU (ID 0).")
        else:
            print("Training will run on CPU.")
            
        try:
            subprocess.run([
                sys.executable, "-m", "spacy", "train", self.cfg_path,
                "--output", self.output_dir,
                "--paths.train", self.train_spacy,
                "--paths.dev", self.val_spacy,
                "--gpu-id", str(gpu_id)
            ], check=True)
            print(f"Training completed. Model saved to {self.output_dir}")
        except Exception as e:
            print(f"Error during training: {e}")
            raise e

    def get_target_preds(self, test_data):
        comb_arr = []
        for article in test_data:
            comb_arr.append(article['title'] + ' ' + article['abstract'])

        y_preds, y_targets = [], []
        print("Running batch inference over test dataset...")
        for idx, doc in tqdm(enumerate(self.nlp.pipe(comb_arr)), total=len(comb_arr)):
            kws = [str(x) for x in doc.ents]
            textData = []
            for sent in sent_tokenize(test_data[idx]['title'] + ' ' + test_data[idx]['abstract']):
                words, _, _, _ = self.preprocessor.sent2words(sent)
                textData.append(' '.join(words))

            _, target, _ = self.preprocessor.mark_keyword_all_sentences(test_data[idx]['keywords'], textData)
            _, predict, _ = self.preprocessor.mark_keyword_all_sentences(kws, textData)
            
            y_preds.extend(predict)
            y_targets.extend(target)
            
        return y_preds, y_targets

    def print_metrics(self, y_targets, y_preds, custom='', experiment=0):
        print(f"\nSeqEval Metrics on sciSpacy {custom}:\n")
        print(classification_report(y_targets, y_preds, mode='strict', scheme=BILOU))
        
        precision = precision_score(y_targets, y_preds) * 100
        recall = recall_score(y_targets, y_preds) * 100
        f1score = f1_score(y_targets, y_preds) * 100
        accuracy = accuracy_score(y_targets, y_preds) * 100
        
        csv_filename = f"{self.config.get('experiment_type', 'gs42')}_results.csv"
        with open(csv_filename, 'a', newline='', encoding="utf-8") as csvfile:
            logwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            logwriter.writerow([experiment, precision, recall, f1score, accuracy])
            
        print(f"Precision given by SeqEval: {precision:.2f}%")
        print(f"Recall given by SeqEval: {recall:.2f}%")
        print(f"F1-Score given by SeqEval: {f1score:.2f}%")
        print(f"Accuracy given by SeqEval: {accuracy:.2f}%")
        print("-" * 60)

    def print_gna_equivalent_metrics(self, y_targets, y_preds):
        """
        Prints and formats metric output matching the exact format of GNAExperiment (IOBES tags).
        Allows apple-to-apple comparison between SciSpacy and neural models on identical tagging schemes.
        """
        # Map BILOU (from TextPreprocessor) to IOBES
        bilou_to_iobes = {
            'U-KP': 'S-KP',
            'L-KP': 'E-KP',
            'B-KP': 'B-KP',
            'I-KP': 'I-KP',
            'O': 'O'
        }
        y_targets_iobes = [[bilou_to_iobes.get(t, t) for t in seq] for seq in y_targets]
        y_preds_iobes = [[bilou_to_iobes.get(t, t) for t in seq] for seq in y_preds]
        
        flat_targets = [tag for seq in y_targets_iobes for tag in seq]
        flat_preds = [tag for seq in y_preds_iobes for tag in seq]
        
        labels_list = ["B-KP", "I-KP", "E-KP", "S-KP", "O"]
        
        cm = confusion_matrix(flat_targets, flat_preds, labels=labels_list)
        print("\n" + "="*50)
        print("GNA-EQUIVALENT DETAILED METRICS (IOBES Tagging)")
        print("="*50)
        print("Confusion Matrix:")
        print(cm)
        
        precisions, recalls, f1s, accuracies, specificities = [], [], [], [], []
        
        for idx, label_name in enumerate(labels_list):
            tp = cm[idx, idx]
            fn = cm[idx, :].sum() - tp
            fp = cm[:, idx].sum() - tp
            tn = cm.sum() - tp - fn - fp
            
            accuracy = (tp + tn) / (tp + fn + fp + tn) if (tp + fn + fp + tn) > 0 else 0.0
            misclassification = (fp + fn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0.0
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
            f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            
            precisions.append(precision)
            recalls.append(recall)
            specificities.append(specificity)
            accuracies.append(accuracy)
            f1s.append(f1)
            
            print("-" * 50)
            print(f"Label: {label_name}")
            print(f"TP:{tp:.1f} FN:{fn:.1f} FP:{fp:.1f} TN:{tn:.1f}")
            print("-" * 50)
            print(f"    Accuracy:\t{accuracy:.6f}")
            print(f"    Misclassification:\t{misclassification:.6f}")
            print(f"    Precision:\t{precision:.6f}")
            print(f"    Sensitivity/Recall:\t{recall:.6f}")
            print(f"    Specificity:\t{specificity:.6f}")
            print(f"    F1 Score:\t{f1:.6f}")
            
        print("=-" * 25)
        print(f"Avg. Accuracy: {np.mean(accuracies):.5f}")
        print(f"Avg. Precision: {np.mean(precisions):.5f}")
        print(f"Avg. F1-Score: {np.mean(f1s):.5f}")
        print(f"Avg. Sensitivity: {np.mean(recalls):.5f}")
        print(f"Avg. Specificity: {np.mean(specificities):.5f}")
        print("=-" * 25)
        
        print("\nSeqEval IOBES Metrics:")
        print(classification_report(y_targets_iobes, y_preds_iobes, mode='strict', scheme=IOBES))
        print(f"Precision (SeqEval): {precision_score(y_targets_iobes, y_preds_iobes)*100:.2f}%")
        print(f"Recall (SeqEval): {recall_score(y_targets_iobes, y_preds_iobes)*100:.2f}%")
        print(f"F1-Score (SeqEval): {f1_score(y_targets_iobes, y_preds_iobes)*100:.2f}%")
        print(f"Accuracy (SeqEval): {accuracy_score(y_targets_iobes, y_preds_iobes)*100:.2f}%")
        print("="*50 + "\n")

    def evaluate(self):
        print("Evaluating ScispacyExperiment...")
        model_best_path = os.path.join(self.output_dir, "model-best")
        if not os.path.exists(model_best_path):
            print(f"Error: Trained model not found at {model_best_path}")
            return
            
        print(f"Loading best model from {model_best_path}...")
        self.nlp = spacy.load(model_best_path)
        
        y_preds, y_targets = self.get_target_preds(self.gs_test)
        
        # Standard BILOU Logging & Logging to CSV
        seed = self.config.get("seed", 42)
        experiment_type = self.config.get("experiment_type", "gs42")
        custom_label = f"GS42 34 Train + 8 Val + 91 Test (Seed: {seed})" if experiment_type == "gs42" else f"GS66 52 Train + 14 Val + 67 Test (Seed: {seed})"
        self.print_metrics(y_targets, y_preds, custom_label, seed)
        
        # High-Fidelity GNA-Equivalent IOBES evaluation
        self.print_gna_equivalent_metrics(y_targets, y_preds)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run ScispacyExperiment Pipeline")
    parser.add_argument("--type", default="gs42", choices=["gs42", "gs66"], help="Experiment configuration: gs42/gs66")
    parser.add_argument("--seed", default=42, type=int, help="Random seed for splitting")
    parser.add_argument("--device", default=None, choices=["cpu", "cuda"], help="Force CPU or CUDA")
    args = parser.parse_args()
    
    config_dict = {
        "experiment_type": args.type,
        "seed": args.seed,
        "device": args.device
    }
    
    experiment = ScispacyExperiment(config_dict)
    experiment.run()
