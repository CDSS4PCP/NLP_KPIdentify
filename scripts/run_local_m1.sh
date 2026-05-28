#!/bin/bash
set -e

# Define ANSI color escape codes for professional output
BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BOLD}${BLUE}====================================================${NC}"
echo -e "${BOLD}${BLUE}       NLP_KPIdentify macOS M1 Pro GPU Launcher     ${NC}"
echo -e "${BOLD}${BLUE}====================================================${NC}"

# 1. Check if Conda is active
if [[ -z "$CONDA_DEFAULT_ENV" || "$CONDA_DEFAULT_ENV" != "cdss" ]]; then
    echo -e "${YELLOW}Warning: Conda environment 'cdss' is not currently active.${NC}"
    echo -e "${BLUE}Attempting to automatically activate 'cdss' conda environment...${NC}"
    
    # Try standard conda loading mechanisms
    if [ -n "$CONDA_EXE" ]; then
        CONDA_DIR=$(dirname $(dirname "$CONDA_EXE"))
        if [ -f "$CONDA_DIR/etc/profile.d/conda.sh" ]; then
            source "$CONDA_DIR/etc/profile.d/conda.sh"
            conda activate cdss 2>/dev/null || conda activate base
        fi
    fi
    
    if [[ "$CONDA_DEFAULT_ENV" != "cdss" ]]; then
        echo -e "${RED}Error: Could not activate 'cdss' environment automatically.${NC}"
        echo -e "${YELLOW}Please run the following commands manually:${NC}"
        echo -e "  conda activate cdss"
        echo -e "  ./scripts/run_local_m1.sh"
        exit 1
    fi
fi

echo -e "${GREEN}✔ Active Conda environment detected: ${BOLD}$CONDA_DEFAULT_ENV${NC}"

# 2. Check PyTorch MPS Acceleration availability
echo -e "${BLUE}Verifying PyTorch MPS capability...${NC}"
python -c "
import torch
if torch.backends.mps.is_available():
    print('✔ PyTorch Metal Performance Shaders (MPS) are available and working.')
else:
    print('❌ PyTorch MPS is NOT available. Training will default to CPU.')
"

# 3. Check and download spaCy & NLTK dependencies
echo -e "${BLUE}Verifying models and dictionaries...${NC}"
python -c "
import sys
import nltk
import spacy

# NLTK Stopwords and Punkt
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
    print('✔ NLTK stopword/punkt datasets are loaded.')
except LookupError:
    print('Downloading NLTK stopwords and punkt tokenizer...')
    nltk.download('stopwords')
    nltk.download('punkt')

# spaCy & SciSpacy models
models = ['en_core_web_sm', 'en_ner_bc5cdr_md', 'en_core_sci_lg']
for model in models:
    try:
        spacy.load(model)
        print(f'✔ spaCy model {model} is installed.')
    except OSError:
        print(f'Warning: spaCy model {model} is missing. Installing...')
        import subprocess
        if model == 'en_core_web_sm':
            subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
        elif model == 'en_ner_bc5cdr_md':
            subprocess.run(['pip', 'install', 'https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_bc5cdr_md-0.5.4.tar.gz'])
        elif model == 'en_core_sci_lg':
            subprocess.run(['pip', 'install', 'https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_lg-0.5.4.tar.gz'])
"

# 4. Trigger the job using PyTorch MPS device
echo -e "${BOLD}${GREEN}✔ Verification completed! Initializing run with PyTorch MPS...${NC}"
echo -e "${BLUE}Running command:${NC} python src/nlp/jobs/gna_pipeline.py --device mps $@"
echo -e "${BOLD}${BLUE}====================================================${NC}"

python src/nlp/jobs/gna_pipeline.py --device mps "$@"
