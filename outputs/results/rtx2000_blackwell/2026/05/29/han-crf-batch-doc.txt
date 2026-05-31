(cdss-gpu) rohangoli@TD-6L0NCJ4:~/remote_mount$ python src/nlp/jobs/gna_pipeline.py --mode train,test,testGS --taggingSchema BIO --model han_crf --epochs 20 --batchSize 64 --validationSplit 0.0 --earlyStopPatience 0
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
Step 1: Loaded training data JSON in 0.4402 seconds (train_docs=2461, val_docs=0).
Step 2: Loaded vocabularies in 0.0692 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.6833 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.6302 seconds (BiLM weights: True).
Label diagnostics [train] | docs=2461 tokens=565485 kp_tokens=147604 kp_ratio=0.2610 kw_nonempty=93069/93071 kw_matched=71661 kw_unmatched=21408 match_ratio=0.7700
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=21402, no_span_match=6
Step 5a: Prepared 2461 train and 0 val CPU batches in 33.00s (cached for all epochs).
Epoch  1/20 | Train Loss: 6.5535 | Val Loss: n/a | Time: 209.33s | Checkpoint Saved
Epoch  2/20 | Train Loss: 4.0911 | Val Loss: n/a | Time: 211.68s | Checkpoint Saved
Epoch  3/20 | Train Loss: 3.3729 | Val Loss: n/a | Time: 218.93s | Checkpoint Saved
Epoch  4/20 | Train Loss: 2.9302 | Val Loss: n/a | Time: 221.17s | Checkpoint Saved
Epoch  5/20 | Train Loss: 2.5917 | Val Loss: n/a | Time: 211.89s | Checkpoint Saved
Epoch  6/20 | Train Loss: 2.2551 | Val Loss: n/a | Time: 216.19s | Checkpoint Saved
Epoch  7/20 | Train Loss: 1.9706 | Val Loss: n/a | Time: 208.14s | Checkpoint Saved
Epoch  8/20 | Train Loss: 1.7199 | Val Loss: n/a | Time: 198.38s | Checkpoint Saved
Epoch  9/20 | Train Loss: 1.5110 | Val Loss: n/a | Time: 204.06s | Checkpoint Saved
Epoch 10/20 | Train Loss: 1.3101 | Val Loss: n/a | Time: 208.88s | Checkpoint Saved
Epoch 11/20 | Train Loss: 1.1472 | Val Loss: n/a | Time: 212.92s | Checkpoint Saved
Epoch 12/20 | Train Loss: 1.0241 | Val Loss: n/a | Time: 203.96s | Checkpoint Saved
Epoch 13/20 | Train Loss: 0.9225 | Val Loss: n/a | Time: 203.83s | Checkpoint Saved
Epoch 14/20 | Train Loss: 0.8247 | Val Loss: n/a | Time: 197.99s | Checkpoint Saved
Epoch 15/20 | Train Loss: 0.7515 | Val Loss: n/a | Time: 200.97s | Checkpoint Saved
Epoch 16/20 | Train Loss: 0.6946 | Val Loss: n/a | Time: 210.84s | Checkpoint Saved
Epoch 17/20 | Train Loss: 0.6417 | Val Loss: n/a | Time: 215.80s | Checkpoint Saved
Epoch 18/20 | Train Loss: 0.5971 | Val Loss: n/a | Time: 221.46s | Checkpoint Saved
Epoch 19/20 | Train Loss: 0.5632 | Val Loss: n/a | Time: 206.89s | Checkpoint Saved
Epoch 20/20 | Train Loss: 0.5354 | Val Loss: n/a | Time: 205.66s | Checkpoint Saved
Step 5: Completed 20 training epochs in 4252.93 seconds (Avg per epoch: 209.45s; prep: 33.00s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 4255.76 seconds
  - Step 1: Loading Data:      0.4402s
  - Step 2: Loading Vocab:     0.0692s
  - Step 3: Embeddings Load:   0.6833s
  - Step 4: Model & Device:    1.6302s
  - Step 5: Epochs Train Loop: 4252.93s (Avg: 209.45s/epoch)
==================================================

============================================================
Mode train completed in 4256.68 seconds
============================================================
============================================================
Running mode: test
============================================================
Auto-selected device: cuda
Running in test mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.1768 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.6139 seconds.

Evaluating on Test dataset: test.json
Label diagnostics [test] | docs=820 tokens=187970 kp_tokens=49600 kp_ratio=0.2639 kw_nonempty=31441/31441 kw_matched=24017 kw_unmatched=7424 match_ratio=0.7639
Label diagnostics [test] top unmatched keywords: patients, implementation, monitoring, management, CDSS
Label diagnostics [test] unmatched reasons: overlap_conflict=7423, no_span_match=1
Step 3: Inference prediction loop completed in 34.57 seconds.
Metrics on Test DS:
Label counts (target): {'B-KP': 37737, 'I-KP': 11851, 'O': 138314}
Label counts (pred):   {'B-KP': 37649, 'I-KP': 11904, 'O': 138349}
Confusion Matrix:
[[ 30142    758   6837]
 [   662   8833   2356]
 [  6845   2313 129156]]
Row sums (target support by label order): [37737, 11851, 138314]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       | 30142.0 |  7595.0 |  7507.0 | 142658.0 |   0.9196 |   0.0804 |   0.8006 |   0.7987 |   0.9500 |   0.7997
I-KP       |  8833.0 |  3018.0 |  3071.0 | 172980.0 |   0.9676 |   0.0324 |   0.7420 |   0.7453 |   0.9826 |   0.7437
O          | 129156.0 |  9158.0 |  9193.0 |  40395.0 |   0.9023 |   0.0977 |   0.9336 |   0.9338 |   0.8146 |   0.9337
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9299 |   0.0701 |   0.8254 |   0.8260 |   0.9157 |   0.8257
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.76      0.76      0.76     37737

   micro avg       0.76      0.76      0.76     37737
   macro avg       0.76      0.76      0.76     37737
weighted avg       0.76      0.76      0.76     37737

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    76.09% |    75.92% |    76.01% |    89.48%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 4.1266 seconds.

==================================================
EVALUATION SUMMARY ON TEST (HAN_CRF on device: cuda)
Total Dataset Eval Time: 46.35 seconds
  - Step 1: Loading Vocabs:    0.1768s
  - Step 2: Model Loading:     0.6139s
  - Step 3: Batch Inference:   34.57s
  - Step 4: Metric Report:     4.1266s
==================================================

============================================================
Mode test completed in 46.43 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0718 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.6344 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.87 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1468, 'I-KP': 535, 'O': 6923}
Confusion Matrix:
[[ 594   38  390]
 [  47  213  175]
 [ 827  284 6358]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   594.0 |   428.0 |   874.0 |   7030.0 |   0.8541 |   0.1459 |   0.4046 |   0.5812 |   0.8894 |   0.4771
I-KP       |   213.0 |   222.0 |   322.0 |   8169.0 |   0.9391 |   0.0609 |   0.3981 |   0.4897 |   0.9621 |   0.4392
O          |  6358.0 |  1111.0 |   565.0 |    892.0 |   0.8122 |   0.1878 |   0.9184 |   0.8513 |   0.6122 |   0.8835
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8685 |   0.1315 |   0.5737 |   0.6407 |   0.8212 |   0.5999
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.35      0.50      0.41      1022

   micro avg       0.35      0.50      0.41      1022
   macro avg       0.35      0.50      0.41      1022
weighted avg       0.35      0.50      0.41      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    35.01% |    50.29% |    41.29% |    80.27%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0829 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 3.89 seconds
  - Step 1: Loading Vocabs:    0.0718s
  - Step 2: Model Loading:     0.6344s
  - Step 3: Batch Inference:   1.87s
  - Step 4: Metric Report:     0.0829s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 3.66 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2581, 'I-KP': 874, 'O': 13782}
Confusion Matrix:
[[ 1470    95   757]
 [   77   401   319]
 [ 1034   378 12706]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1470.0 |   852.0 |  1111.0 |  13804.0 |   0.8861 |   0.1139 |   0.5695 |   0.6331 |   0.9255 |   0.5996
I-KP       |   401.0 |   396.0 |   473.0 |  15967.0 |   0.9496 |   0.0504 |   0.4588 |   0.5031 |   0.9712 |   0.4800
O          | 12706.0 |  1412.0 |  1076.0 |   2043.0 |   0.8557 |   0.1443 |   0.9219 |   0.9000 |   0.6550 |   0.9108
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8971 |   0.1029 |   0.6501 |   0.6787 |   0.8506 |   0.6635
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.52      0.57      0.54      2322

   micro avg       0.52      0.57      0.54      2322
   macro avg       0.52      0.57      0.54      2322
weighted avg       0.52      0.57      0.54      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    51.72% |    57.49% |    54.46% |    84.57%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.4470 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 8.98 seconds
  - Step 1: Loading Vocabs:    0.0718s
  - Step 2: Model Loading:     0.6344s
  - Step 3: Batch Inference:   3.66s
  - Step 4: Metric Report:     0.4470s
==================================================

============================================================
Mode testGS completed in 8.99 seconds
============================================================
(cdss-gpu) rohangoli@TD-6L0NCJ4:~/remote_mount$
