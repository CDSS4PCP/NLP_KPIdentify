# R7 HAN-CRF (k=5 fold=4, freeze embeddings, fixed+block defaults)
Run started: 2026-05-29T18:17:12-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,test,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --earlyStopPatience 3 --hanUseBlockDiagonal --hanBatchMode fixed --hanFreezeEmbeddings --kFolds 5 --kFoldIndex 4 --kFoldSeed 42
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
Using k-fold split: k=5, fold=4, seed=42 (train_docs=1969, val_docs=492).
Step 1: Loaded training data JSON in 0.3213 seconds (train_docs=1969, val_docs=492).
Step 2: Loaded vocabularies in 0.0493 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.5016 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.5067 seconds (BiLM weights: True).
Label diagnostics [train] | docs=1969 tokens=452660 kp_tokens=118184 kp_ratio=0.2611 kw_nonempty=74483/74484 kw_matched=57355 kw_unmatched=17128 match_ratio=0.7700
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=17124, no_span_match=4
Label diagnostics [val] | docs=492 tokens=112825 kp_tokens=29420 kp_ratio=0.2608 kw_nonempty=18586/18587 kw_matched=14306 kw_unmatched=4280 match_ratio=0.7697
Label diagnostics [val] top unmatched keywords: patients, implementation, management, CDSS, alerts
Label diagnostics [val] unmatched reasons: overlap_conflict=4278, no_span_match=2
Step 5a: Prepared 325 train and 81 val CPU batches in 40.21s (cached for all epochs).
Epoch  1/20 | Train Loss: 11.8941 | Val Loss: 7.2299 | Time: 33.99s | Checkpoint Saved
Epoch  2/20 | Train Loss: 6.0449 | Val Loss: 6.1498 | Time: 33.94s | Checkpoint Saved
Epoch  3/20 | Train Loss: 4.7625 | Val Loss: 5.8322 | Time: 33.36s | Checkpoint Saved
Epoch  4/20 | Train Loss: 3.9966 | Val Loss: 5.5569 | Time: 31.89s | Checkpoint Saved
Epoch  5/20 | Train Loss: 3.5036 | Val Loss: 5.6584 | Time: 31.14s | No Save
Epoch  6/20 | Train Loss: 3.1051 | Val Loss: 5.7630 | Time: 30.84s | No Save
Epoch  7/20 | Train Loss: 2.7757 | Val Loss: 5.8049 | Time: 33.46s | No Save
Early stopping at epoch 7 after 3 non-improving validation epochs (best epoch=4, best val loss=5.5569).
Best checkpoint selected from epoch 4 with val loss 5.5569.
Step 5: Completed 7 training epochs in 291.87 seconds (Avg per epoch: 32.66s; prep: 40.21s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 294.25 seconds
  - Step 1: Loading Data:      0.3213s
  - Step 2: Loading Vocab:     0.0493s
  - Step 3: Embeddings Load:   0.5016s
  - Step 4: Model & Device:    1.5067s
  - Step 5: Epochs Train Loop: 291.87s (Avg: 32.66s/epoch)
==================================================

============================================================
Mode train completed in 294.32 seconds
============================================================
============================================================
Running mode: test
============================================================
Auto-selected device: cuda
Running in test mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0708 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.4957 seconds.

Evaluating on Test dataset: test.json
Label diagnostics [test] | docs=820 tokens=187970 kp_tokens=49600 kp_ratio=0.2639 kw_nonempty=31441/31441 kw_matched=24017 kw_unmatched=7424 match_ratio=0.7639
Label diagnostics [test] top unmatched keywords: patients, implementation, monitoring, management, CDSS
Label diagnostics [test] unmatched reasons: overlap_conflict=7423, no_span_match=1
Step 3: Inference prediction loop completed in 20.40 seconds.
Metrics on Test DS:
Label counts (target): {'B-KP': 37737, 'I-KP': 11851, 'O': 138314}
Label counts (pred):   {'B-KP': 37364, 'I-KP': 11030, 'O': 139508}
Confusion Matrix:
[[ 29986    539   7212]
 [   837   8448   2566]
 [  6541   2043 129730]]
Row sums (target support by label order): [37737, 11851, 138314]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       | 29986.0 |  7751.0 |  7378.0 | 142787.0 |   0.9195 |   0.0805 |   0.8025 |   0.7946 |   0.9509 |   0.7986
I-KP       |  8448.0 |  3403.0 |  2582.0 | 173469.0 |   0.9681 |   0.0319 |   0.7659 |   0.7129 |   0.9853 |   0.7384
O          | 129730.0 |  8584.0 |  9778.0 |  39810.0 |   0.9023 |   0.0977 |   0.9299 |   0.9379 |   0.8028 |   0.9339
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9300 |   0.0700 |   0.8328 |   0.8151 |   0.9130 |   0.8236
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.76      0.75      0.75     37737

   micro avg       0.76      0.75      0.75     37737
   macro avg       0.76      0.75      0.75     37737
weighted avg       0.76      0.75      0.75     37737

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    75.59% |    74.84% |    75.22% |    89.50%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 2.6812 seconds.

==================================================
EVALUATION SUMMARY ON TEST (HAN_CRF on device: cuda)
Total Dataset Eval Time: 30.18 seconds
  - Step 1: Loading Vocabs:    0.0708s
  - Step 2: Model Loading:     0.4957s
  - Step 3: Batch Inference:   20.40s
  - Step 4: Metric Report:     2.6812s
==================================================

============================================================
Mode test completed in 30.21 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0508 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.6222 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.18 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1401, 'I-KP': 444, 'O': 7081}
Confusion Matrix:
[[ 596   37  389]
 [  55  183  197]
 [ 750  224 6495]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   596.0 |   426.0 |   805.0 |   7099.0 |   0.8621 |   0.1379 |   0.4254 |   0.5832 |   0.8982 |   0.4920
I-KP       |   183.0 |   252.0 |   261.0 |   8230.0 |   0.9425 |   0.0575 |   0.4122 |   0.4207 |   0.9693 |   0.4164
O          |  6495.0 |   974.0 |   586.0 |    871.0 |   0.8252 |   0.1748 |   0.9172 |   0.8696 |   0.5978 |   0.8928
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8766 |   0.1234 |   0.5849 |   0.6245 |   0.8217 |   0.6004
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.37      0.51      0.43      1022

   micro avg       0.37      0.51      0.43      1022
   macro avg       0.37      0.51      0.43      1022
weighted avg       0.37      0.51      0.43      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    37.04% |    50.78% |    42.84% |    81.49%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0764 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 2.76 seconds
  - Step 1: Loading Vocabs:    0.0508s
  - Step 2: Model Loading:     0.6222s
  - Step 3: Batch Inference:   1.18s
  - Step 4: Metric Report:     0.0764s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.19 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2454, 'I-KP': 758, 'O': 14025}
Confusion Matrix:
[[ 1418    91   813]
 [   77   353   367]
 [  959   314 12845]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1418.0 |   904.0 |  1036.0 |  13879.0 |   0.8875 |   0.1125 |   0.5778 |   0.6107 |   0.9305 |   0.5938
I-KP       |   353.0 |   444.0 |   405.0 |  16035.0 |   0.9507 |   0.0493 |   0.4657 |   0.4429 |   0.9754 |   0.4540
O          | 12845.0 |  1273.0 |  1180.0 |   1939.0 |   0.8577 |   0.1423 |   0.9159 |   0.9098 |   0.6217 |   0.9128
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8986 |   0.1014 |   0.6531 |   0.6545 |   0.8425 |   0.6536
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.51      0.54      0.53      2322

   micro avg       0.51      0.54      0.53      2322
   macro avg       0.51      0.54      0.53      2322
weighted avg       0.51      0.54      0.53      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    51.47% |    54.39% |    52.89% |    84.79%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1437 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 6.21 seconds
  - Step 1: Loading Vocabs:    0.0508s
  - Step 2: Model Loading:     0.6222s
  - Step 3: Batch Inference:   2.19s
  - Step 4: Metric Report:     0.1437s
==================================================

============================================================
Mode testGS completed in 6.23 seconds
============================================================
