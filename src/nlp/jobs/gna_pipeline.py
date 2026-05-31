import argparse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.nlp.experiments.gna_experiment import GNAExperiment

def clean_pipeline():
    print("Cleaning pipeline interim data...")
    interim_dir = "interim_data"
    if os.path.exists(interim_dir):
        schemas = ["BIO", "BILOU", "IOBES"]
        model_names = ["BiLSTM-CRF", "HAN-CRF"]
        schema_files = [f"{m}_{s}.pt" for m in model_names for s in schemas]
        files_to_remove = ["BiLM.pt", "LM_word2vec.bin", "int2token.json", "token2int.json"] + schema_files
        for f in files_to_remove:
            path = os.path.join(interim_dir, f)
            if os.path.exists(path):
                print(f"Removing {path}")
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"Error removing {path}: {e}")
    print("Pipeline cleaning complete.")

def run(args):
    raw_mode = args.mode.strip()
    modes = [m.strip() for m in raw_mode.split(",")]
    
    # Expand 'all' keyword
    final_modes = []
    for mode in modes:
        if mode == "all":
            final_modes.extend(["createData", "preTrain", "train", "test", "testGS"])
        else:
            final_modes.append(mode)
            
    # Process clean first if present
    if "clean" in final_modes:
        print("="*60)
        print("Executing clean target...")
        print("="*60)
        clean_pipeline()
        final_modes = [m for m in final_modes if m != "clean"]
        
    for run_mode in final_modes:
        print("="*60)
        print(f"Running mode: {run_mode}")
        print("="*60)
        
        import time
        start_time = time.time()
        
        config = {
            "mode": run_mode,
            "model_type": args.model,
            "device": args.device,
            "sections": args.sections,
            "features": args.features,
            "stem": args.stem,
            "bidirection": args.bidirection,
            "wordEmbdType": args.wordEmbdType,
            "minSentences": args.minSentences,
            "filterKP": args.filterKP,
            "seqLength": args.seqLength,
            "batchSize": args.batchSize,
            "epochs": args.epochs,
            "optimizer": args.optimizer,
            "lr": args.lr,
            "positiveUpsample": args.positiveUpsample,
            "preGenSyntheticData": args.preGenSyntheticData,
            "traintestSplit": args.traintestSplit,
            "noLayers": args.noLayers,
            "taggingSchema": args.taggingSchema,
            "numWorkers": args.numWorkers,
            "validationSplit": args.validationSplit,
            "earlyStopPatience": args.earlyStopPatience,
            "kFolds": args.kFolds,
            "kFoldIndex": args.kFoldIndex,
            "kFoldSeed": args.kFoldSeed,
            "cvPoolTrainAndTest": args.cvPoolTrainAndTest,
            "gsFineTuneEpochs": args.gsFineTuneEpochs,
            "gsFineTuneLr": args.gsFineTuneLr,
            "gsFineTuneTrainFraction": args.gsFineTuneTrainFraction,
            "gsFineTuneSeed": args.gsFineTuneSeed,
            "synthModel": args.synthModel,
            "hanUseBlockDiagonal": args.hanUseBlockDiagonal,
            "hanBatchMode": args.hanBatchMode,
            "hanFreezeEmbeddings": args.hanFreezeEmbeddings,
        }
        
        experiment = GNAExperiment(config)
        experiment.run()
        
        elapsed_time = time.time() - start_time
        print("="*60)
        print(f"Mode {run_mode} completed in {elapsed_time:.2f} seconds")
        print("="*60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GNA Pipeline (Replacement for mainV2.py)")
    parser.add_argument('--mode','-m', default='train', type=str, help='Mode of opertion: train/test/testgs/predict/createData/preTrain')
    parser.add_argument('--model', default='bilstm_crf', type=str, choices=['bilstm_crf', 'han_crf'], help='Model architecture to use: bilstm_crf/han_crf')
    parser.add_argument('--taggingSchema', default='IOBES', type=str, choices=['BIO', 'BILOU', 'IOBES'], help='Sequence tagging schema to use')
    parser.add_argument('--device', default=None, type=str, choices=['cpu', 'cuda', 'mps'], help='Forcefully use device: cpu/cuda/mps')
    parser.add_argument('--sections','-s', default=['title','abstract'], type=str, nargs='+', help='Sections in research paper to include: title/abstract/methods/results')
    parser.add_argument('--features','-f', default=['CEM','WFOF','POS','LEN','TI','TR'], type=str, nargs='+', help="Features to include")
    parser.add_argument("--stem", "-stem",default="no",help="Vocabulary Stemming - yes/no")
    parser.add_argument('-bD','--bidirection', default=False, type=bool)
    parser.add_argument('-wET','--wordEmbdType', type=str, default="basic")
    parser.add_argument("-minSent","--minSentences", default=3, type=int)
    parser.add_argument("-fKP","--filterKP", default=False, type=bool)
    parser.add_argument("-seqLen","--seqLength", type=int, default=5)
    parser.add_argument("-bS","--batchSize", type=int, default=64)
    parser.add_argument("-epochs","--epochs", type=int, default=20)
    parser.add_argument("--optimizer", type=str, default="adamw", choices=["adamw", "sgd"], help="Optimizer for sequence tagger training")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate for sequence tagger training")
    parser.add_argument("--positiveUpsample", type=int, default=0, help="Repeat positive-label sentences in training batches to reduce all-O collapse")
    parser.add_argument("--numWorkers", type=int, default=None, help="DataLoader workers for preTrain BiLM (default auto; on WSL auto-falls back to 0)")
    parser.add_argument("--validationSplit", type=float, default=0.0, help="Fraction of train.json reserved for validation during train mode (0 disables)")
    parser.add_argument("--earlyStopPatience", type=int, default=0, help="Stop training after N non-improving validation epochs (<=0 disables)")
    parser.add_argument("--kFolds", type=int, default=1, help="Number of folds for k-fold CV-style train/val split in train mode (1 disables)")
    parser.add_argument("--kFoldIndex", type=int, default=None, help="Fold index to use as validation fold when kFolds>1")
    parser.add_argument("--kFoldSeed", type=int, default=42, help="Random seed for k-fold permutation")
    parser.add_argument("--cvPoolTrainAndTest", action=argparse.BooleanOptionalAction, default=False, help="When true, train mode pools train.json+test.json before CV splitting")
    parser.add_argument("--gsFineTuneEpochs", type=int, default=0, help="Optional post-train fine-tuning epochs on GS42+GS91 train fold (0 disables)")
    parser.add_argument("--gsFineTuneLr", type=float, default=3e-4, help="Learning rate for optional GS fine-tuning stage")
    parser.add_argument("--gsFineTuneTrainFraction", type=float, default=0.8, help="Train fraction for GS fine-tuning split")
    parser.add_argument("--gsFineTuneSeed", type=int, default=42, help="Seed used for GS fine-tuning split")
    parser.add_argument("--synthModel", type=str, default=None, help="spaCy model/path for synthetic keyword generation (defaults to outputs/models/cdssSciSpacy/model-best if present)")
    parser.add_argument("--hanUseBlockDiagonal", action=argparse.BooleanOptionalAction, default=None, help="Enable/disable document-isolated block masking in HAN sentence attention (default: config)" )
    parser.add_argument("--hanBatchMode", type=str, default=None, choices=["doc", "fixed"], help="HAN batching strategy: doc=one-doc batches, fixed=pack documents up to batchSize sentences (default: config)")
    parser.add_argument("--hanFreezeEmbeddings", action="store_true", help="Freeze pre-trained HAN word embeddings during training")
    parser.add_argument("-preGenSynthDS", "--preGenSyntheticData", default=False, type=bool)
    parser.add_argument('-ttSplit', "--traintestSplit", type=int, default=3)
    parser.add_argument('-nLayers','--noLayers', type=int, default=4)
    args = parser.parse_args()
    run(args)
