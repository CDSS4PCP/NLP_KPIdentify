(cdss) rohangoli@Rohans-MacBook-Pro NLP_KPIdentify % python src/nlp/jobs/gna_pipeline.py --mode createData --model bilstm_crf --epochs 20 --batchSize 128 --taggingSchema BIO
============================================================
Running mode: createData
============================================================
Auto-selected device: cpu
Running in createData mode...
Preparing data...
Loaded source docs: main=3326 gs=42 misc=12 combined=3380
/Users/rohangoli/miniforge3/envs/cdss/lib/python3.9/site-packages/spacy/util.py:910: UserWarning: [W095] Model 'en_pipeline' (0.0.0) was trained with spaCy v3.2.4 and may not be 100% compatible with the current version (3.7.5). If you see errors or degraded performance, download a newer compatible model or retrain your custom model with the current spaCy version. For more details and available updates, run: python -m spacy validate
  warnings.warn(warn_msg)
Synthetic keyword model: /Users/rohangoli/Data/NLP_KPIdentify/outputs/models/cdssSciSpacy/model-best
JSON pre-processing: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████| 3380/3380 [00:00<00:00, 398974.12it/s]
Synthetic Keywords: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████| 3380/3380 [03:50<00:00, 14.69it/s]
Pre-computing TF-IDF and TextRank features...
The 3281 document calculation TF-IDF completed: 100%|█████████████████████████████████████████████████████████████████████████| 3281/3281 [00:00<00:00, 12008.68it/s]
The 3281 document has been calculated TextRank completed: 100%|█████████████████████████████████████████████████████████████████| 3281/3281 [00:05<00:00, 575.22it/s]
Synthetic labels generation completed in 506.54 seconds.
Checking for existing Gold Standard testsets (testgs42, testgs91) to compute features...
The 42 document calculation TF-IDF completed: 100%|███████████████████████████████████████████████████████████████████████████████| 42/42 [00:00<00:00, 13609.45it/s]
The 42 document has been calculated TextRank completed: 100%|███████████████████████████████████████████████████████████████████████| 42/42 [00:00<00:00, 505.82it/s]
Computed TF-IDF and TextRank for testgs42.json
The 91 document calculation TF-IDF completed: 100%|███████████████████████████████████████████████████████████████████████████████| 91/91 [00:00<00:00, 14203.69it/s]
The 91 document has been calculated TextRank completed: 100%|███████████████████████████████████████████████████████████████████████| 91/91 [00:00<00:00, 547.03it/s]
Computed TF-IDF and TextRank for testgs91.json
Data preparation complete.
============================================================
Mode createData completed in 509.41 seconds
============================================================
(cdss) rohangoli@Rohans-MacBook-Pro NLP_KPIdentify % 
