"""CLI entry point for transformer token-classification baselines (reviewer concern #1).

Examples:
    # Fine-tune PubMedBERT on the synthetic train split and evaluate on GS42/GS91
    python src/nlp/jobs/transformer_pipeline.py \
        --hfModel pubmedbert --mode train,testGS --device cuda \
        --epochs 3 --batchSize 16 --lr 3e-5 --seed 42 \
        --dumpPredictions outputs/results/rtx2000_blackwell/2026/06/12/preds_pubmedbert

    # Short names: pubmedbert | biobert | scibert  (or any HF hub id / local path)
"""
import argparse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from src.nlp.experiments.transformer_experiment import TransformerExperiment


def main():
    parser = argparse.ArgumentParser(description="Biomedical transformer token-classification baseline")
    parser.add_argument("--hfModel", type=str, default="pubmedbert",
                        help="Preset (pubmedbert/biobert/scibert) or HF hub id / local path")
    parser.add_argument("--mode", "-m", type=str, default="train,testGS",
                        help="Comma-separated: train, testGS, inferGS (zero-shot random head), transferGS (zero-shot pretrained-NER transfer)")
    parser.add_argument("--transferModel", type=str, default="d4data/biomedical-ner-all",
                        help="HF token-classification checkpoint used for transferGS (pretrained NER head)")
    parser.add_argument("--device", type=str, default=None, choices=["cpu", "cuda", "mps"])
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batchSize", type=int, default=16)
    parser.add_argument("--lr", type=float, default=3e-5)
    parser.add_argument("--maxLength", type=int, default=256)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--dumpPredictions", type=str, default=None,
                        help="Directory to dump per-document gold/pred BIO tags for error analysis & bootstrap CI")
    parser.add_argument("--dataSource", type=str, default="synthetic", choices=["synthetic", "kpbiomed", "pubmedake"],
                        help="Training-data source: synthetic labels (default) or a public dataset (KPBioMed/PubMedAKE)")
    parser.add_argument("--jsonDataDir", type=str, default=None,
                        help="Override JSON_DATA directory (read train.json/test.json/testgs*.json). Defaults per --dataSource.")
    parser.add_argument("--trainSampleSize", type=int, default=None,
                        help="Cap the number of train.json documents used during train mode (None=use all)")
    args = parser.parse_args()

    config = {
        "hfModel": args.hfModel,
        "mode": args.mode,
        "device": args.device,
        "epochs": args.epochs,
        "batchSize": args.batchSize,
        "lr": args.lr,
        "maxLength": args.maxLength,
        "seed": args.seed,
        "dumpPredictions": args.dumpPredictions,
        "transferModel": args.transferModel,
        "dataSource": args.dataSource,
        "jsonDataDir": args.jsonDataDir,
        "trainSampleSize": args.trainSampleSize,
    }
    experiment = TransformerExperiment(config)
    experiment.run()


if __name__ == "__main__":
    main()
