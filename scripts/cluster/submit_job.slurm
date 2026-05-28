#!/bin/bash
# ==============================================================================
# Slurm Job Submission Script for HPC Clusters (Palmetto / general clusters)
# ==============================================================================
#SBATCH --job-name=cdss_gna_pipeline
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH --time=06:00:00
#SBATCH --output=cdss_gna_pipeline_%j.out
#SBATCH --error=cdss_gna_pipeline_%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=rgoli@clemson.edu

# Move into the working directory
cd $SLURM_SUBMIT_DIR

echo "======================================================================"
echo "HPC Slurm Job Triggered"
echo "======================================================================"
echo "Job Name:           $SLURM_JOB_NAME"
echo "Job ID:             $SLURM_JOB_ID"
echo "Execution Node:     $(hostname)"
echo "Current Directory:  $(pwd)"
echo "Submit Directory:   $SLURM_SUBMIT_DIR"
echo "Start Time:         $(date)"
echo "======================================================================"

# 1. Load Cluster Environment Modules
echo "Loading required environment modules..."
module purge
module load anaconda3/2022.10-gcc/11.3.0
module load cuda/11.8.0-gcc/11.3.0

# 2. Activate Conda Environment
echo "Activating Conda Environment..."
if [ -f /software/anaconda3/2022.10/etc/profile.d/conda.sh ]; then
    source /software/anaconda3/2022.10/etc/profile.d/conda.sh
else
    eval "$(conda shell.bash hook)"
fi

conda activate cdss

# 3. Load Project Environment Variables (API Keys, Paths, etc.)
if [ -f scripts/cluster/load_env.sh ]; then
    echo "Loading cluster execution environment variables (load_env.sh)..."
    source scripts/cluster/load_env.sh
else
    echo "Warning: scripts/cluster/load_env.sh not found. Proceeding with system defaults."
fi

# 4. Verify GPU Configuration via PyTorch/CUDA
echo "Verifying CUDA capability..."
python -c "
import torch
print('PyTorch Version:', torch.__file__)
if torch.cuda.is_available():
    print('✔ CUDA is available!')
    print('Active Device Count:', torch.cuda.device_count())
    print('Device Name:', torch.cuda.get_device_name(0))
else:
    print('❌ CUDA is NOT available. Script will fall back to CPU.')
"

# 5. Launch the Modular pipeline via python or torchrun
# Run all modes of the pipeline sequentially: clean -> createData -> preTrain -> train -> testGS
echo "Launching global attention pipeline (gna_pipeline.py)..."
python src/nlp/jobs/gna_pipeline.py --device cuda --mode clean,createData,preTrain,train,testGS --epochs 20 --batchSize 64

echo "======================================================================"
echo "HPC Slurm Job Completed at: $(date)"
echo "======================================================================"
