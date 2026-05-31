# R7 HAN-CRF KFold (k=5, fold=0, freeze embeddings, fixed+block defaults)
Run started: 2026-05-29T17:46:14-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,test,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --earlyStopPatience 3 --hanUseBlockDiagonal --hanBatchMode fixed --hanFreezeEmbeddings --kFolds 5 --kFoldIndex 0 --kFoldSeed 42
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
Using k-fold split: k=5, fold=0, seed=42 (train_docs=1968, val_docs=493).
Step 1: Loaded training data JSON in 0.3445 seconds (train_docs=1968, val_docs=493).
Step 2: Loaded vocabularies in 0.0494 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.5937 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.6757 seconds (BiLM weights: True).
Label diagnostics [train] | docs=1968 tokens=453270 kp_tokens=118483 kp_ratio=0.2614 kw_nonempty=74577/74579 kw_matched=57385 kw_unmatched=17192 match_ratio=0.7695
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=17186, no_span_match=6
Label diagnostics [val] | docs=493 tokens=112215 kp_tokens=29121 kp_ratio=0.2595 kw_nonempty=18492/18492 kw_matched=14276 kw_unmatched=4216 match_ratio=0.7720
Label diagnostics [val] top unmatched keywords: patients, CDSS, implementation, management, CDS
Label diagnostics [val] unmatched reasons: overlap_conflict=4216
Step 5a: Prepared 325 train and 81 val CPU batches in 39.37s (cached for all epochs).
Epoch  1/20 | Train Loss: 8.6651 | Val Loss: 6.1360 | Time: 33.72s | Checkpoint Saved
Epoch  2/20 | Train Loss: 5.2110 | Val Loss: 5.2837 | Time: 34.43s | Checkpoint Saved
Epoch  3/20 | Train Loss: 4.1676 | Val Loss: 4.8600 | Time: 31.34s | Checkpoint Saved
Epoch  4/20 | Train Loss: 3.5755 | Val Loss: 4.8463 | Time: 31.48s | Checkpoint Saved
