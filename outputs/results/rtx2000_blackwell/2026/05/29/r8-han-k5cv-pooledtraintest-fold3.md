# R8 HAN-CRF (k=5 pooled train+test for CV, fold=3, freeze embeddings, fixed+block defaults, final eval GS only)
Run started: 2026-05-29T18:47:46-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --earlyStopPatience 3 --hanUseBlockDiagonal --hanBatchMode fixed --hanFreezeEmbeddings --kFolds 5 --kFoldIndex 3 --kFoldSeed 42 --cvPoolTrainAndTest
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
CV pooling enabled: using train.json + test.json (train_docs=2461, test_docs=820, pooled_docs=3281).
Using k-fold split: k=5, fold=3, seed=42 (train_docs=2625, val_docs=656).
Step 1: Loaded training data JSON in 0.5504 seconds (train_docs=2625, val_docs=656).
Step 2: Loaded vocabularies in 0.0455 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.6787 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.6273 seconds (BiLM weights: True).
Label diagnostics [train] | docs=2625 tokens=600370 kp_tokens=157188 kp_ratio=0.2618 kw_nonempty=99339/99341 kw_matched=76366 kw_unmatched=22973 match_ratio=0.7687
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=22966, no_span_match=7
Label diagnostics [val] | docs=656 tokens=153085 kp_tokens=40016 kp_ratio=0.2614 kw_nonempty=25171/25171 kw_matched=19312 kw_unmatched=5859 match_ratio=0.7672
Label diagnostics [val] top unmatched keywords: patients, management, CDSS, implementation, CDS
Label diagnostics [val] unmatched reasons: overlap_conflict=5859
Step 5a: Prepared 432 train and 108 val CPU batches in 49.60s (cached for all epochs).
Epoch  1/20 | Train Loss: 7.5906 | Val Loss: 5.3407 | Time: 47.37s | Checkpoint Saved
Epoch  2/20 | Train Loss: 4.5420 | Val Loss: 4.7005 | Time: 45.21s | Checkpoint Saved
Epoch  3/20 | Train Loss: 3.7236 | Val Loss: 4.6225 | Time: 43.92s | Checkpoint Saved
Epoch  4/20 | Train Loss: 3.2803 | Val Loss: 4.6106 | Time: 45.11s | Checkpoint Saved
Epoch  5/20 | Train Loss: 2.9345 | Val Loss: 4.5952 | Time: 45.25s | Checkpoint Saved
Epoch  6/20 | Train Loss: 2.6484 | Val Loss: 4.8269 | Time: 44.88s | No Save
Epoch  7/20 | Train Loss: 2.4175 | Val Loss: 5.0542 | Time: 45.50s | No Save
Epoch  8/20 | Train Loss: 2.1587 | Val Loss: 5.1927 | Time: 45.98s | No Save
Early stopping at epoch 8 after 3 non-improving validation epochs (best epoch=5, best val loss=4.5952).
Best checkpoint selected from epoch 5 with val loss 4.5952.
Step 5: Completed 8 training epochs in 441.96 seconds (Avg per epoch: 45.40s; prep: 49.60s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 444.86 seconds
  - Step 1: Loading Data:      0.5504s
  - Step 2: Loading Vocab:     0.0455s
  - Step 3: Embeddings Load:   0.6787s
  - Step 4: Model & Device:    1.6273s
  - Step 5: Epochs Train Loop: 441.96s (Avg: 45.40s/epoch)
==================================================

============================================================
Mode train completed in 444.97 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0639 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5219 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.23 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1380, 'I-KP': 469, 'O': 7077}
Confusion Matrix:
[[ 592   41  389]
 [  42  199  194]
 [ 746  229 6494]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   592.0 |   430.0 |   788.0 |   7116.0 |   0.8635 |   0.1365 |   0.4290 |   0.5793 |   0.9003 |   0.4929
I-KP       |   199.0 |   236.0 |   270.0 |   8221.0 |   0.9433 |   0.0567 |   0.4243 |   0.4575 |   0.9682 |   0.4403
O          |  6494.0 |   975.0 |   583.0 |    874.0 |   0.8255 |   0.1745 |   0.9176 |   0.8695 |   0.5999 |   0.8929
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8774 |   0.1226 |   0.5903 |   0.6354 |   0.8228 |   0.6087
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.37      0.50      0.43      1022

   micro avg       0.37      0.50      0.43      1022
   macro avg       0.37      0.50      0.43      1022
weighted avg       0.37      0.50      0.43      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    37.25% |    50.29% |    42.80% |    81.62%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0713 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 2.68 seconds
  - Step 1: Loading Vocabs:    0.0639s
  - Step 2: Model Loading:     0.5219s
  - Step 3: Batch Inference:   1.23s
  - Step 4: Metric Report:     0.0713s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.12 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2523, 'I-KP': 828, 'O': 13886}
Confusion Matrix:
[[ 1429    84   809]
 [   77   389   331]
 [ 1017   355 12746]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1429.0 |   893.0 |  1094.0 |  13821.0 |   0.8847 |   0.1153 |   0.5664 |   0.6154 |   0.9267 |   0.5899
I-KP       |   389.0 |   408.0 |   439.0 |  16001.0 |   0.9509 |   0.0491 |   0.4698 |   0.4881 |   0.9733 |   0.4788
O          | 12746.0 |  1372.0 |  1140.0 |   1979.0 |   0.8543 |   0.1457 |   0.9179 |   0.9028 |   0.6345 |   0.9103
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8966 |   0.1034 |   0.6514 |   0.6688 |   0.8448 |   0.6597
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.52      0.56      0.54      2322

   micro avg       0.52      0.56      0.54      2322
   macro avg       0.52      0.56      0.54      2322
weighted avg       0.52      0.56      0.54      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    51.80% |    56.29% |    53.95% |    84.49%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.5632 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 6.26 seconds
  - Step 1: Loading Vocabs:    0.0639s
  - Step 2: Model Loading:     0.5219s
  - Step 3: Batch Inference:   2.12s
  - Step 4: Metric Report:     0.5632s
==================================================

============================================================
Mode testGS completed in 6.27 seconds
============================================================
