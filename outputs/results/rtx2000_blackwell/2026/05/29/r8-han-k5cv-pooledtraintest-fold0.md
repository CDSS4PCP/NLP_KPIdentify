# R8 HAN-CRF (k=5 pooled train+test for CV, fold=0, freeze embeddings, fixed+block defaults, final eval GS only)
Run started: 2026-05-29T18:26:15-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --earlyStopPatience 3 --hanUseBlockDiagonal --hanBatchMode fixed --hanFreezeEmbeddings --kFolds 5 --kFoldIndex 0 --kFoldSeed 42 --cvPoolTrainAndTest
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
CV pooling enabled: using train.json + test.json (train_docs=2461, test_docs=820, pooled_docs=3281).
Using k-fold split: k=5, fold=0, seed=42 (train_docs=2624, val_docs=657).
Step 1: Loaded training data JSON in 0.6611 seconds (train_docs=2624, val_docs=657).
Step 2: Loaded vocabularies in 0.0509 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.5784 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.5810 seconds (BiLM weights: True).
Label diagnostics [train] | docs=2624 tokens=601035 kp_tokens=157152 kp_ratio=0.2615 kw_nonempty=99163/99164 kw_matched=76362 kw_unmatched=22801 match_ratio=0.7701
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=22795, no_span_match=6
Label diagnostics [val] | docs=657 tokens=152420 kp_tokens=40052 kp_ratio=0.2628 kw_nonempty=25347/25348 kw_matched=19316 kw_unmatched=6031 match_ratio=0.7621
Label diagnostics [val] top unmatched keywords: patients, implementation, CDSS, monitoring, management
Label diagnostics [val] unmatched reasons: overlap_conflict=6030, no_span_match=1
Step 5a: Prepared 430 train and 110 val CPU batches in 56.52s (cached for all epochs).
Epoch  1/20 | Train Loss: 7.9268 | Val Loss: 5.3459 | Time: 46.06s | Checkpoint Saved
Epoch  2/20 | Train Loss: 4.6199 | Val Loss: 4.6794 | Time: 41.95s | Checkpoint Saved
Epoch  3/20 | Train Loss: 3.7821 | Val Loss: 4.6288 | Time: 43.44s | Checkpoint Saved
Epoch  4/20 | Train Loss: 3.3089 | Val Loss: 4.4851 | Time: 47.23s | Checkpoint Saved
Epoch  5/20 | Train Loss: 2.9661 | Val Loss: 4.5354 | Time: 44.60s | No Save
Epoch  6/20 | Train Loss: 2.6749 | Val Loss: 4.7125 | Time: 45.16s | No Save
Epoch  7/20 | Train Loss: 2.4131 | Val Loss: 4.9594 | Time: 42.28s | No Save
Early stopping at epoch 7 after 3 non-improving validation epochs (best epoch=4, best val loss=4.4851).
Best checkpoint selected from epoch 4 with val loss 4.4851.
Step 5: Completed 7 training epochs in 397.28 seconds (Avg per epoch: 44.39s; prep: 56.52s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 400.15 seconds
  - Step 1: Loading Data:      0.6611s
  - Step 2: Loading Vocab:     0.0509s
  - Step 3: Embeddings Load:   0.5784s
  - Step 4: Model & Device:    1.5810s
  - Step 5: Epochs Train Loop: 397.28s (Avg: 44.39s/epoch)
==================================================

============================================================
Mode train completed in 400.25 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0594 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5048 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.25 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1395, 'I-KP': 532, 'O': 6999}
Confusion Matrix:
[[ 602   39  381]
 [  47  217  171]
 [ 746  276 6447]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   602.0 |   420.0 |   793.0 |   7111.0 |   0.8641 |   0.1359 |   0.4315 |   0.5890 |   0.8997 |   0.4981
I-KP       |   217.0 |   218.0 |   315.0 |   8176.0 |   0.9403 |   0.0597 |   0.4079 |   0.4989 |   0.9629 |   0.4488
O          |  6447.0 |  1022.0 |   552.0 |    905.0 |   0.8237 |   0.1763 |   0.9211 |   0.8632 |   0.6211 |   0.8912
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8760 |   0.1240 |   0.5869 |   0.6504 |   0.8279 |   0.6127
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.37      0.50      0.42      1022

   micro avg       0.37      0.50      0.42      1022
   macro avg       0.37      0.50      0.42      1022
weighted avg       0.37      0.50      0.42      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    36.77% |    50.20% |    42.45% |    81.40%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0846 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 2.68 seconds
  - Step 1: Loading Vocabs:    0.0594s
  - Step 2: Model Loading:     0.5048s
  - Step 3: Batch Inference:   1.25s
  - Step 4: Metric Report:     0.0846s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.18 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2541, 'I-KP': 925, 'O': 13771}
Confusion Matrix:
[[ 1424    99   799]
 [   78   411   308]
 [ 1039   415 12664]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1424.0 |   898.0 |  1117.0 |  13798.0 |   0.8831 |   0.1169 |   0.5604 |   0.6133 |   0.9251 |   0.5856
I-KP       |   411.0 |   386.0 |   514.0 |  15926.0 |   0.9478 |   0.0522 |   0.4443 |   0.5157 |   0.9687 |   0.4774
O          | 12664.0 |  1454.0 |  1107.0 |   2012.0 |   0.8514 |   0.1486 |   0.9196 |   0.8970 |   0.6451 |   0.9082
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8941 |   0.1059 |   0.6414 |   0.6753 |   0.8463 |   0.6571
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.51      0.56      0.53      2322

   micro avg       0.51      0.56      0.53      2322
   macro avg       0.51      0.56      0.53      2322
weighted avg       0.51      0.56      0.53      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    50.77% |    55.56% |    53.05% |    84.12%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.4236 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 6.28 seconds
  - Step 1: Loading Vocabs:    0.0594s
  - Step 2: Model Loading:     0.5048s
  - Step 3: Batch Inference:   2.18s
  - Step 4: Metric Report:     0.4236s
==================================================

============================================================
Mode testGS completed in 6.29 seconds
============================================================
