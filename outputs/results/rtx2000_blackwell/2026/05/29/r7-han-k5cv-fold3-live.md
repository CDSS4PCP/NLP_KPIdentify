# R7 HAN-CRF (k=5 fold=3, freeze embeddings, fixed+block defaults)
Run started: 2026-05-29T18:11:05-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,test,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --earlyStopPatience 3 --hanUseBlockDiagonal --hanBatchMode fixed --hanFreezeEmbeddings --kFolds 5 --kFoldIndex 3 --kFoldSeed 42
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
Using k-fold split: k=5, fold=3, seed=42 (train_docs=1969, val_docs=492).
Step 1: Loaded training data JSON in 0.3151 seconds (train_docs=1969, val_docs=492).
Step 2: Loaded vocabularies in 0.0495 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.5331 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.6255 seconds (BiLM weights: True).
Label diagnostics [train] | docs=1969 tokens=450039 kp_tokens=117691 kp_ratio=0.2615 kw_nonempty=74271/74272 kw_matched=57315 kw_unmatched=16956 match_ratio=0.7717
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, treatment
Label diagnostics [train] unmatched reasons: overlap_conflict=16952, no_span_match=4
Label diagnostics [val] | docs=492 tokens=115446 kp_tokens=29913 kp_ratio=0.2591 kw_nonempty=18798/18799 kw_matched=14346 kw_unmatched=4452 match_ratio=0.7632
Label diagnostics [val] top unmatched keywords: patients, implementation, CDSS, management, monitoring
Label diagnostics [val] unmatched reasons: overlap_conflict=4450, no_span_match=2
Step 5a: Prepared 322 train and 84 val CPU batches in 39.04s (cached for all epochs).
Epoch  1/20 | Train Loss: 10.7897 | Val Loss: 7.0400 | Time: 33.78s | Checkpoint Saved
Epoch  2/20 | Train Loss: 6.0813 | Val Loss: 5.9373 | Time: 33.36s | Checkpoint Saved
Epoch  3/20 | Train Loss: 4.7750 | Val Loss: 5.4616 | Time: 30.78s | Checkpoint Saved
Epoch  4/20 | Train Loss: 4.0020 | Val Loss: 5.3806 | Time: 29.76s | Checkpoint Saved
Epoch  5/20 | Train Loss: 3.4863 | Val Loss: 5.3294 | Time: 33.02s | Checkpoint Saved
Epoch  6/20 | Train Loss: 3.1072 | Val Loss: 5.3789 | Time: 34.55s | No Save
Epoch  7/20 | Train Loss: 2.7967 | Val Loss: 5.4642 | Time: 31.41s | No Save
Epoch  8/20 | Train Loss: 2.5015 | Val Loss: 5.4686 | Time: 31.94s | No Save
Early stopping at epoch 8 after 3 non-improving validation epochs (best epoch=5, best val loss=5.3294).
Best checkpoint selected from epoch 5 with val loss 5.3294.
Step 5: Completed 8 training epochs in 321.74 seconds (Avg per epoch: 32.33s; prep: 39.04s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 324.26 seconds
  - Step 1: Loading Data:      0.3151s
  - Step 2: Loading Vocab:     0.0495s
  - Step 3: Embeddings Load:   0.5331s
  - Step 4: Model & Device:    1.6255s
  - Step 5: Epochs Train Loop: 321.74s (Avg: 32.33s/epoch)
==================================================

============================================================
Mode train completed in 324.35 seconds
============================================================
============================================================
Running mode: test
============================================================
Auto-selected device: cuda
Running in test mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0825 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5465 seconds.

Evaluating on Test dataset: test.json
Label diagnostics [test] | docs=820 tokens=187970 kp_tokens=49600 kp_ratio=0.2639 kw_nonempty=31441/31441 kw_matched=24017 kw_unmatched=7424 match_ratio=0.7639
Label diagnostics [test] top unmatched keywords: patients, implementation, monitoring, management, CDSS
Label diagnostics [test] unmatched reasons: overlap_conflict=7423, no_span_match=1
Step 3: Inference prediction loop completed in 20.83 seconds.
Metrics on Test DS:
Label counts (target): {'B-KP': 37737, 'I-KP': 11851, 'O': 138314}
Label counts (pred):   {'B-KP': 35446, 'I-KP': 13475, 'O': 138981}
Confusion Matrix:
[[ 29116    976   7645]
 [   489   9344   2018]
 [  5841   3155 129318]]
Row sums (target support by label order): [37737, 11851, 138314]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       | 29116.0 |  8621.0 |  6330.0 | 143835.0 |   0.9204 |   0.0796 |   0.8214 |   0.7716 |   0.9578 |   0.7957
I-KP       |  9344.0 |  2507.0 |  4131.0 | 171920.0 |   0.9647 |   0.0353 |   0.6934 |   0.7885 |   0.9765 |   0.7379
O          | 129318.0 |  8996.0 |  9663.0 |  39925.0 |   0.9007 |   0.0993 |   0.9305 |   0.9350 |   0.8051 |   0.9327
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9286 |   0.0714 |   0.8151 |   0.8317 |   0.9132 |   0.8221
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.77      0.73      0.75     37737

   micro avg       0.77      0.73      0.75     37737
   macro avg       0.77      0.73      0.75     37737
weighted avg       0.77      0.73      0.75     37737

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    77.23% |    72.54% |    74.82% |    89.29%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 2.7889 seconds.

==================================================
EVALUATION SUMMARY ON TEST (HAN_CRF on device: cuda)
Total Dataset Eval Time: 31.77 seconds
  - Step 1: Loading Vocabs:    0.0825s
  - Step 2: Model Loading:     0.5465s
  - Step 3: Batch Inference:   20.83s
  - Step 4: Metric Report:     2.7889s
==================================================

============================================================
Mode test completed in 31.79 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0566 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.6115 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.23 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1481, 'I-KP': 593, 'O': 6852}
Confusion Matrix:
[[ 607   44  371]
 [  51  235  149]
 [ 823  314 6332]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   607.0 |   415.0 |   874.0 |   7030.0 |   0.8556 |   0.1444 |   0.4099 |   0.5939 |   0.8894 |   0.4850
I-KP       |   235.0 |   200.0 |   358.0 |   8133.0 |   0.9375 |   0.0625 |   0.3963 |   0.5402 |   0.9578 |   0.4572
O          |  6332.0 |  1137.0 |   520.0 |    937.0 |   0.8144 |   0.1856 |   0.9241 |   0.8478 |   0.6431 |   0.8843
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8691 |   0.1309 |   0.5768 |   0.6606 |   0.8301 |   0.6088
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.35      0.51      0.41      1022

   micro avg       0.35      0.51      0.41      1022
   macro avg       0.35      0.51      0.41      1022
weighted avg       0.35      0.51      0.41      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    35.04% |    50.78% |    41.47% |    80.37%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1070 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 2.82 seconds
  - Step 1: Loading Vocabs:    0.0566s
  - Step 2: Model Loading:     0.6115s
  - Step 3: Batch Inference:   1.23s
  - Step 4: Metric Report:     0.1070s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.38 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2579, 'I-KP': 1000, 'O': 13658}
Confusion Matrix:
[[ 1441   112   769]
 [   77   422   298]
 [ 1061   466 12591]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1441.0 |   881.0 |  1138.0 |  13777.0 |   0.8829 |   0.1171 |   0.5587 |   0.6206 |   0.9237 |   0.5880
I-KP       |   422.0 |   375.0 |   578.0 |  15862.0 |   0.9447 |   0.0553 |   0.4220 |   0.5295 |   0.9648 |   0.4697
O          | 12591.0 |  1527.0 |  1067.0 |   2052.0 |   0.8495 |   0.1505 |   0.9219 |   0.8918 |   0.6579 |   0.9066
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8924 |   0.1076 |   0.6342 |   0.6806 |   0.8488 |   0.6548
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.50      0.55      0.52      2322

   micro avg       0.50      0.55      0.52      2322
   macro avg       0.50      0.55      0.52      2322
weighted avg       0.50      0.55      0.52      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    49.86% |    55.38% |    52.48% |    83.85%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1795 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 6.40 seconds
  - Step 1: Loading Vocabs:    0.0566s
  - Step 2: Model Loading:     0.6115s
  - Step 3: Batch Inference:   2.38s
  - Step 4: Metric Report:     0.1795s
==================================================

============================================================
Mode testGS completed in 6.41 seconds
============================================================
