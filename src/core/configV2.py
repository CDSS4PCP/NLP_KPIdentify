DATA_FOLDER = 'data'
PUBMED_PROCESSED_DATA = 'data/pubmed_data/processed_data/processed_full_data.xml'
PUBMED_PROCESSED_DATA_GS = 'data/pubmed_data/processed_data/processed_44_abstracts_test.xml'
HOLDOUT_DATA = 'data/HoldOut_Total.txt'
JSON_DATA = 'data/pubmed_data/json_data_synthetic_labels_v2'
# Public-dataset JSON_DATA directories (replace synthetic labels with gold/extractive keyphrases).
PUBLIC_DATA_KPBIOMED = 'data/pubmed_data/json_data_kpbiomed'
PUBLIC_DATA_PUBMEDAKE = 'data/pubmed_data/json_data_pubmedake'
# Local download location for raw PubMedAKE (Zenodo 6330817) split files.
PUBMEDAKE_RAW_DIR = 'data/pubmed_data/raw_data/pubmedake'
PRE_PROCESSED_DATA = 'data/pubmed_data/preprocess_data'
INTERIM_DATA = 'interim_data/'
VOCAB = INTERIM_DATA+'vocab/'
MODEL_FOLDER = INTERIM_DATA+'models/'
RESULT_FOLDER = INTERIM_DATA+'results/'

# HAN defaults (used when not provided by CLI runtime config).
HAN_USE_BLOCK_DIAGONAL = True
HAN_BATCH_MODE = 'fixed'
HAN_CONTEXT_MODE = 'sentence_only'
HAN_CONTEXT_HEADS = 4
HAN_CONTEXT_DROPOUT = 0.1
HAN_USE_GATED_FUSION = False

# Phase 2: Context Horizon & Batching parameters
MIN_TOKENS_PER_SENTENCE_FOR_TRAINING = 4  # Sentence filter threshold (Phase 2 exploration: 1, 2, 4)
HAN_USE_CHUNK_MEMORY = False  # Enable document-chunk memory across batch boundaries (Phase 2)
HAN_CHUNK_MEMORY_SIZE = 128  # Size of compressed chunk memory representation
HAN_PACKING_MODE = 'mixed'  # 'mixed'=allow spillover, 'strict_doc'=keep doc boundaries

# Phase 3: Label Quality & Training Dynamics
WEAK_LABEL_CONFIDENCE_THRESHOLD = None  # Confidence threshold for weak label filtering (Phase 3, None=disabled)
WEAK_LABEL_CONFIDENCE_METRIC = 'source_agreement'  # How to compute confidence: 'source_agreement', 'combined'
CURRICULUM_LEARNING_ENABLED = False  # Enable curriculum learning (easy samples first) (Phase 3)
CURRICULUM_SCHEDULE = 'linear'  # Schedule for curriculum: 'linear', 'sqrt', 'exp'
CURRICULUM_WARMUP_PERCENT = 20  # Percentage of epochs to spend on easy samples only

# Symmetric model-training defaults.
BILSTM_FREEZE_EMBEDDINGS = True
REBALANCING_MODE = 'auto'