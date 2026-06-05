# R2 HAN-CRF (mask-fix baseline, fixed-batch+block-diagonal defaults)
Run started: 2026-05-29T16:49:59-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,test,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --validationSplit 0.0 --earlyStopPatience 0 --hanUseBlockDiagonal --hanBatchMode fixed
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
Step 1: Loaded training data JSON in 0.4481 seconds (train_docs=2461, val_docs=0).
Step 2: Loaded vocabularies in 0.0714 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.5924 seconds.
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.7298 seconds (BiLM weights: True).
Label diagnostics [train] | docs=2461 tokens=565485 kp_tokens=147604 kp_ratio=0.2610 kw_nonempty=93069/93071 kw_matched=71661 kw_unmatched=21408 match_ratio=0.7700
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=21402, no_span_match=6
Step 5a: Prepared 405 train and 0 val CPU batches in 41.96s (cached for all epochs).
Epoch  1/20 | Train Loss: 9.7301 | Val Loss: n/a | Time: 37.98s | Checkpoint Saved
Epoch  2/20 | Train Loss: 5.7048 | Val Loss: n/a | Time: 33.67s | Checkpoint Saved
Epoch  3/20 | Train Loss: 4.4498 | Val Loss: n/a | Time: 31.85s | Checkpoint Saved
Epoch  4/20 | Train Loss: 3.7490 | Val Loss: n/a | Time: 35.21s | Checkpoint Saved
Epoch  5/20 | Train Loss: 3.2762 | Val Loss: n/a | Time: 33.81s | Checkpoint Saved
Epoch  6/20 | Train Loss: 2.9220 | Val Loss: n/a | Time: 32.90s | Checkpoint Saved
Epoch  7/20 | Train Loss: 2.6214 | Val Loss: n/a | Time: 32.79s | Checkpoint Saved
Epoch  8/20 | Train Loss: 2.3561 | Val Loss: n/a | Time: 32.68s | Checkpoint Saved
Epoch  9/20 | Train Loss: 2.1091 | Val Loss: n/a | Time: 34.55s | Checkpoint Saved
Epoch 10/20 | Train Loss: 1.8748 | Val Loss: n/a | Time: 37.35s | Checkpoint Saved
Epoch 11/20 | Train Loss: 1.6704 | Val Loss: n/a | Time: 33.01s | Checkpoint Saved
Epoch 12/20 | Train Loss: 1.5059 | Val Loss: n/a | Time: 33.89s | Checkpoint Saved
Epoch 13/20 | Train Loss: 1.3296 | Val Loss: n/a | Time: 33.32s | Checkpoint Saved
Epoch 14/20 | Train Loss: 1.1706 | Val Loss: n/a | Time: 33.45s | Checkpoint Saved
Epoch 15/20 | Train Loss: 1.0549 | Val Loss: n/a | Time: 32.50s | Checkpoint Saved
Epoch 16/20 | Train Loss: 0.9473 | Val Loss: n/a | Time: 34.35s | Checkpoint Saved
Epoch 17/20 | Train Loss: 0.8423 | Val Loss: n/a | Time: 33.58s | Checkpoint Saved
Epoch 18/20 | Train Loss: 0.7709 | Val Loss: n/a | Time: 34.22s | Checkpoint Saved
Epoch 19/20 | Train Loss: 0.7005 | Val Loss: n/a | Time: 33.35s | Checkpoint Saved
Epoch 20/20 | Train Loss: 0.6296 | Val Loss: n/a | Time: 32.66s | Checkpoint Saved
Step 5: Completed 20 training epochs in 752.67 seconds (Avg per epoch: 33.85s; prep: 41.96s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 755.51 seconds
  - Step 1: Loading Data:      0.4481s
  - Step 2: Loading Vocab:     0.0714s
  - Step 3: Embeddings Load:   0.5924s
  - Step 4: Model & Device:    1.7298s
  - Step 5: Epochs Train Loop: 752.67s (Avg: 33.85s/epoch)
==================================================

============================================================
Mode train completed in 755.64 seconds
============================================================
============================================================
Running mode: test
============================================================
Auto-selected device: cuda
Running in test mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0618 seconds.
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5384 seconds.

Evaluating on Test dataset: test.json
Label diagnostics [test] | docs=820 tokens=187970 kp_tokens=49600 kp_ratio=0.2639 kw_nonempty=31441/31441 kw_matched=24017 kw_unmatched=7424 match_ratio=0.7639
Label diagnostics [test] top unmatched keywords: patients, implementation, monitoring, management, CDSS
Label diagnostics [test] unmatched reasons: overlap_conflict=7423, no_span_match=1
Step 3: Inference prediction loop completed in 17.76 seconds.
Metrics on Test DS:
Label counts (target): {'B-KP': 37737, 'I-KP': 11851, 'O': 138314}
Label counts (pred):   {'B-KP': 36537, 'I-KP': 11822, 'O': 139543}
Confusion Matrix:
[[ 29448    820   7469]
 [   591   8745   2515]
 [  6498   2257 129559]]
Row sums (target support by label order): [37737, 11851, 138314]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       | 29448.0 |  8289.0 |  7089.0 | 143076.0 |   0.9182 |   0.0818 |   0.8060 |   0.7803 |   0.9528 |   0.7930
I-KP       |  8745.0 |  3106.0 |  3077.0 | 172974.0 |   0.9671 |   0.0329 |   0.7397 |   0.7379 |   0.9825 |   0.7388
O          | 129559.0 |  8755.0 |  9984.0 |  39604.0 |   0.9003 |   0.0997 |   0.9285 |   0.9367 |   0.7987 |   0.9326
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9285 |   0.0715 |   0.8247 |   0.8183 |   0.9113 |   0.8214
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.77      0.74      0.75     37737

   micro avg       0.77      0.74      0.75     37737
   macro avg       0.77      0.74      0.75     37737
weighted avg       0.77      0.74      0.75     37737

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    76.63% |    74.19% |    75.39% |    89.28%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 2.5157 seconds.

==================================================
EVALUATION SUMMARY ON TEST (HAN_CRF on device: cuda)
Total Dataset Eval Time: 26.77 seconds
  - Step 1: Loading Vocabs:    0.0618s
  - Step 2: Model Loading:     0.5384s
  - Step 3: Batch Inference:   17.76s
  - Step 4: Metric Report:     2.5157s
==================================================

============================================================
Mode test completed in 26.80 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0525 seconds.
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5988 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 0.98 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1391, 'I-KP': 523, 'O': 7012}
Confusion Matrix:
[[ 598   45  379]
 [  46  205  184]
 [ 747  273 6449]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   598.0 |   424.0 |   793.0 |   7111.0 |   0.8637 |   0.1363 |   0.4299 |   0.5851 |   0.8997 |   0.4956
I-KP       |   205.0 |   230.0 |   318.0 |   8173.0 |   0.9386 |   0.0614 |   0.3920 |   0.4713 |   0.9625 |   0.4280
O          |  6449.0 |  1020.0 |   563.0 |    894.0 |   0.8227 |   0.1773 |   0.9197 |   0.8634 |   0.6136 |   0.8907
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8750 |   0.1250 |   0.5805 |   0.6399 |   0.8253 |   0.6048
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
Score (%)         |    36.88% |    50.20% |    42.52% |    81.25%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0698 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 2.65 seconds
  - Step 1: Loading Vocabs:    0.0525s
  - Step 2: Model Loading:     0.5988s
  - Step 3: Batch Inference:   0.98s
  - Step 4: Metric Report:     0.0698s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.21 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2460, 'I-KP': 872, 'O': 13905}
Confusion Matrix:
[[ 1459   100   763]
 [   70   394   333]
 [  931   378 12809]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1459.0 |   863.0 |  1001.0 |  13914.0 |   0.8919 |   0.1081 |   0.5931 |   0.6283 |   0.9329 |   0.6102
I-KP       |   394.0 |   403.0 |   478.0 |  15962.0 |   0.9489 |   0.0511 |   0.4518 |   0.4944 |   0.9709 |   0.4721
O          | 12809.0 |  1309.0 |  1096.0 |   2023.0 |   0.8605 |   0.1395 |   0.9212 |   0.9073 |   0.6486 |   0.9142
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9004 |   0.0996 |   0.6554 |   0.6767 |   0.8508 |   0.6655
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.54      0.57      0.56      2322

   micro avg       0.54      0.57      0.56      2322
   macro avg       0.54      0.57      0.56      2322
weighted avg       0.54      0.57      0.56      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    54.11% |    57.32% |    55.67% |    85.06%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1418 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 5.92 seconds
  - Step 1: Loading Vocabs:    0.0525s
  - Step 2: Model Loading:     0.5988s
  - Step 3: Batch Inference:   2.21s
  - Step 4: Metric Report:     0.1418s
==================================================

============================================================
Mode testGS completed in 5.94 seconds
============================================================
