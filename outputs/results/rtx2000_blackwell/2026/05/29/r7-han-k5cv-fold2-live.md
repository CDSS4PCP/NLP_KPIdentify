# R7 HAN-CRF (k=5 fold=2, freeze embeddings, fixed+block defaults)
Run started: 2026-05-29T18:05:10-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,test,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --earlyStopPatience 3 --hanUseBlockDiagonal --hanBatchMode fixed --hanFreezeEmbeddings --kFolds 5 --kFoldIndex 2 --kFoldSeed 42
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
Using k-fold split: k=5, fold=2, seed=42 (train_docs=1969, val_docs=492).
Step 1: Loaded training data JSON in 0.3691 seconds (train_docs=1969, val_docs=492).
Step 2: Loaded vocabularies in 0.0643 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.5921 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.7020 seconds (BiLM weights: True).
Label diagnostics [train] | docs=1969 tokens=454263 kp_tokens=118289 kp_ratio=0.2604 kw_nonempty=74628/74630 kw_matched=57358 kw_unmatched=17270 match_ratio=0.7686
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=17264, no_span_match=6
Label diagnostics [val] | docs=492 tokens=111222 kp_tokens=29315 kp_ratio=0.2636 kw_nonempty=18441/18441 kw_matched=14303 kw_unmatched=4138 match_ratio=0.7756
Label diagnostics [val] top unmatched keywords: patients, implementation, CDSS, management, treatment
Label diagnostics [val] unmatched reasons: overlap_conflict=4138
Step 5a: Prepared 326 train and 80 val CPU batches in 40.01s (cached for all epochs).
Epoch  1/20 | Train Loss: 10.2972 | Val Loss: 6.8715 | Time: 33.11s | Checkpoint Saved
Epoch  2/20 | Train Loss: 5.8116 | Val Loss: 5.7088 | Time: 30.37s | Checkpoint Saved
Epoch  3/20 | Train Loss: 4.5727 | Val Loss: 5.4570 | Time: 29.00s | Checkpoint Saved
Epoch  4/20 | Train Loss: 3.8676 | Val Loss: 5.4151 | Time: 30.88s | Checkpoint Saved
Epoch  5/20 | Train Loss: 3.3882 | Val Loss: 5.0964 | Time: 30.38s | Checkpoint Saved
Epoch  6/20 | Train Loss: 3.0269 | Val Loss: 5.4619 | Time: 30.30s | No Save
Epoch  7/20 | Train Loss: 2.7092 | Val Loss: 5.3380 | Time: 31.20s | No Save
Epoch  8/20 | Train Loss: 2.4374 | Val Loss: 5.5577 | Time: 30.95s | No Save
Early stopping at epoch 8 after 3 non-improving validation epochs (best epoch=5, best val loss=5.0964).
Best checkpoint selected from epoch 5 with val loss 5.0964.
Step 5: Completed 8 training epochs in 311.19 seconds (Avg per epoch: 30.77s; prep: 40.01s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 313.92 seconds
  - Step 1: Loading Data:      0.3691s
  - Step 2: Loading Vocab:     0.0643s
  - Step 3: Embeddings Load:   0.5921s
  - Step 4: Model & Device:    1.7020s
  - Step 5: Epochs Train Loop: 311.19s (Avg: 30.77s/epoch)
==================================================

============================================================
Mode train completed in 314.01 seconds
============================================================
============================================================
Running mode: test
============================================================
Auto-selected device: cuda
Running in test mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0717 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5159 seconds.

Evaluating on Test dataset: test.json
Label diagnostics [test] | docs=820 tokens=187970 kp_tokens=49600 kp_ratio=0.2639 kw_nonempty=31441/31441 kw_matched=24017 kw_unmatched=7424 match_ratio=0.7639
Label diagnostics [test] top unmatched keywords: patients, implementation, monitoring, management, CDSS
Label diagnostics [test] unmatched reasons: overlap_conflict=7423, no_span_match=1
Step 3: Inference prediction loop completed in 19.70 seconds.
Metrics on Test DS:
Label counts (target): {'B-KP': 37737, 'I-KP': 11851, 'O': 138314}
Label counts (pred):   {'B-KP': 36969, 'I-KP': 13093, 'O': 137840}
Confusion Matrix:
[[ 29828    940   6969]
 [   481   9256   2114]
 [  6660   2897 128757]]
Row sums (target support by label order): [37737, 11851, 138314]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       | 29828.0 |  7909.0 |  7141.0 | 143024.0 |   0.9199 |   0.0801 |   0.8068 |   0.7904 |   0.9524 |   0.7985
I-KP       |  9256.0 |  2595.0 |  3837.0 | 172214.0 |   0.9658 |   0.0342 |   0.7069 |   0.7810 |   0.9782 |   0.7421
O          | 128757.0 |  9557.0 |  9083.0 |  40505.0 |   0.9008 |   0.0992 |   0.9341 |   0.9309 |   0.8168 |   0.9325
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9288 |   0.0712 |   0.8160 |   0.8341 |   0.9158 |   0.8244
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.76      0.75      0.76     37737

   micro avg       0.76      0.75      0.76     37737
   macro avg       0.76      0.75      0.76     37737
weighted avg       0.76      0.75      0.76     37737

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    76.40% |    74.84% |    75.61% |    89.32%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 2.5951 seconds.

==================================================
EVALUATION SUMMARY ON TEST (HAN_CRF on device: cuda)
Total Dataset Eval Time: 29.04 seconds
  - Step 1: Loading Vocabs:    0.0717s
  - Step 2: Model Loading:     0.5159s
  - Step 3: Batch Inference:   19.70s
  - Step 4: Metric Report:     2.5951s
==================================================

============================================================
Mode test completed in 29.07 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0534 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5878 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.10 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1464, 'I-KP': 615, 'O': 6847}
Confusion Matrix:
[[ 592   44  386]
 [  50  235  150]
 [ 822  336 6311]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   592.0 |   430.0 |   872.0 |   7032.0 |   0.8541 |   0.1459 |   0.4044 |   0.5793 |   0.8897 |   0.4763
I-KP       |   235.0 |   200.0 |   380.0 |   8111.0 |   0.9350 |   0.0650 |   0.3821 |   0.5402 |   0.9552 |   0.4476
O          |  6311.0 |  1158.0 |   536.0 |    921.0 |   0.8102 |   0.1898 |   0.9217 |   0.8450 |   0.6321 |   0.8817
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8665 |   0.1335 |   0.5694 |   0.6548 |   0.8257 |   0.6019
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
Score (%)         |    34.70% |    49.71% |    40.87% |    79.97%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1018 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 2.52 seconds
  - Step 1: Loading Vocabs:    0.0534s
  - Step 2: Model Loading:     0.5878s
  - Step 3: Batch Inference:   1.10s
  - Step 4: Metric Report:     0.1018s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.06 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2604, 'I-KP': 1055, 'O': 13578}
Confusion Matrix:
[[ 1433   118   771]
 [   72   435   290]
 [ 1099   502 12517]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1433.0 |   889.0 |  1171.0 |  13744.0 |   0.8805 |   0.1195 |   0.5503 |   0.6171 |   0.9215 |   0.5818
I-KP       |   435.0 |   362.0 |   620.0 |  15820.0 |   0.9430 |   0.0570 |   0.4123 |   0.5458 |   0.9623 |   0.4698
O          | 12517.0 |  1601.0 |  1061.0 |   2058.0 |   0.8456 |   0.1544 |   0.9219 |   0.8866 |   0.6598 |   0.9039
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8897 |   0.1103 |   0.6282 |   0.6832 |   0.8479 |   0.6518
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.49      0.55      0.52      2322

   micro avg       0.49      0.55      0.52      2322
   macro avg       0.49      0.55      0.52      2322
weighted avg       0.49      0.55      0.52      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    49.39% |    55.38% |    52.21% |    83.45%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1584 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 5.58 seconds
  - Step 1: Loading Vocabs:    0.0534s
  - Step 2: Model Loading:     0.5878s
  - Step 3: Batch Inference:   2.06s
  - Step 4: Metric Report:     0.1584s
==================================================

============================================================
Mode testGS completed in 5.59 seconds
============================================================
