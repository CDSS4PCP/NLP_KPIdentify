# R7 HAN-CRF (k=5 fold=1, freeze embeddings, fixed+block defaults)
Run started: 2026-05-29T17:59:12-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,test,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --earlyStopPatience 3 --hanUseBlockDiagonal --hanBatchMode fixed --hanFreezeEmbeddings --kFolds 5 --kFoldIndex 1 --kFoldSeed 42
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
Using k-fold split: k=5, fold=1, seed=42 (train_docs=1969, val_docs=492).
Step 1: Loaded training data JSON in 0.4712 seconds (train_docs=1969, val_docs=492).
Step 2: Loaded vocabularies in 0.0705 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.6521 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.6579 seconds (BiLM weights: True).
Label diagnostics [train] | docs=1969 tokens=451708 kp_tokens=117769 kp_ratio=0.2607 kw_nonempty=74317/74319 kw_matched=57231 kw_unmatched=17086 match_ratio=0.7701
Label diagnostics [train] top unmatched keywords: patients, implementation, CDSS, management, treatment
Label diagnostics [train] unmatched reasons: overlap_conflict=17082, no_span_match=4
Label diagnostics [val] | docs=492 tokens=113777 kp_tokens=29835 kp_ratio=0.2622 kw_nonempty=18752/18752 kw_matched=14430 kw_unmatched=4322 match_ratio=0.7695
Label diagnostics [val] top unmatched keywords: patients, management, monitoring, implementation, treatment
Label diagnostics [val] unmatched reasons: overlap_conflict=4320, no_span_match=2
Step 5a: Prepared 324 train and 82 val CPU batches in 38.97s (cached for all epochs).
Epoch  1/20 | Train Loss: 10.7000 | Val Loss: 6.8088 | Time: 32.68s | Checkpoint Saved
Epoch  2/20 | Train Loss: 5.7969 | Val Loss: 5.7152 | Time: 30.76s | Checkpoint Saved
Epoch  3/20 | Train Loss: 4.5390 | Val Loss: 5.2985 | Time: 29.88s | Checkpoint Saved
Epoch  4/20 | Train Loss: 3.8187 | Val Loss: 5.2717 | Time: 30.95s | Checkpoint Saved
Epoch  5/20 | Train Loss: 3.3506 | Val Loss: 5.2590 | Time: 33.14s | Checkpoint Saved
Epoch  6/20 | Train Loss: 2.9870 | Val Loss: 5.3442 | Time: 29.61s | No Save
Epoch  7/20 | Train Loss: 2.6857 | Val Loss: 5.2703 | Time: 28.72s | No Save
Epoch  8/20 | Train Loss: 2.4044 | Val Loss: 5.7908 | Time: 31.85s | No Save
Early stopping at epoch 8 after 3 non-improving validation epochs (best epoch=5, best val loss=5.2590).
Best checkpoint selected from epoch 5 with val loss 5.2590.
Step 5: Completed 8 training epochs in 310.13 seconds (Avg per epoch: 30.95s; prep: 38.97s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 312.98 seconds
  - Step 1: Loading Data:      0.4712s
  - Step 2: Loading Vocab:     0.0705s
  - Step 3: Embeddings Load:   0.6521s
  - Step 4: Model & Device:    1.6579s
  - Step 5: Epochs Train Loop: 310.13s (Avg: 30.95s/epoch)
==================================================

============================================================
Mode train completed in 313.07 seconds
============================================================
============================================================
Running mode: test
============================================================
Auto-selected device: cuda
Running in test mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0715 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5378 seconds.

Evaluating on Test dataset: test.json
Label diagnostics [test] | docs=820 tokens=187970 kp_tokens=49600 kp_ratio=0.2639 kw_nonempty=31441/31441 kw_matched=24017 kw_unmatched=7424 match_ratio=0.7639
Label diagnostics [test] top unmatched keywords: patients, implementation, monitoring, management, CDSS
Label diagnostics [test] unmatched reasons: overlap_conflict=7423, no_span_match=1
Step 3: Inference prediction loop completed in 21.77 seconds.
Metrics on Test DS:
Label counts (target): {'B-KP': 37737, 'I-KP': 11851, 'O': 138314}
Label counts (pred):   {'B-KP': 33625, 'I-KP': 10508, 'O': 143769}
Confusion Matrix:
[[ 28224    720   8793]
 [   515   8140   3196]
 [  4886   1648 131780]]
Row sums (target support by label order): [37737, 11851, 138314]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       | 28224.0 |  9513.0 |  5401.0 | 144764.0 |   0.9206 |   0.0794 |   0.8394 |   0.7479 |   0.9640 |   0.7910
I-KP       |  8140.0 |  3711.0 |  2368.0 | 173683.0 |   0.9676 |   0.0324 |   0.7746 |   0.6869 |   0.9865 |   0.7281
O          | 131780.0 |  6534.0 | 11989.0 |  37599.0 |   0.9014 |   0.0986 |   0.9166 |   0.9528 |   0.7582 |   0.9343
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9299 |   0.0701 |   0.8435 |   0.7958 |   0.9029 |   0.8178
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.80      0.71      0.75     37737

   micro avg       0.80      0.71      0.75     37737
   macro avg       0.80      0.71      0.75     37737
weighted avg       0.80      0.71      0.75     37737

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    79.84% |    71.14% |    75.24% |    89.48%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 2.6397 seconds.

==================================================
EVALUATION SUMMARY ON TEST (HAN_CRF on device: cuda)
Total Dataset Eval Time: 31.55 seconds
  - Step 1: Loading Vocabs:    0.0715s
  - Step 2: Model Loading:     0.5378s
  - Step 3: Batch Inference:   21.77s
  - Step 4: Metric Report:     2.6397s
==================================================

============================================================
Mode test completed in 31.57 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0528 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.6192 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 0.97 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1277, 'I-KP': 506, 'O': 7143}
Confusion Matrix:
[[ 550   36  436]
 [  43  209  183]
 [ 684  261 6524]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   550.0 |   472.0 |   727.0 |   7177.0 |   0.8657 |   0.1343 |   0.4307 |   0.5382 |   0.9080 |   0.4785
I-KP       |   209.0 |   226.0 |   297.0 |   8194.0 |   0.9414 |   0.0586 |   0.4130 |   0.4805 |   0.9650 |   0.4442
O          |  6524.0 |   945.0 |   619.0 |    838.0 |   0.8248 |   0.1752 |   0.9133 |   0.8735 |   0.5752 |   0.8930
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8773 |   0.1227 |   0.5857 |   0.6307 |   0.8161 |   0.6052
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.38      0.47      0.42      1022

   micro avg       0.38      0.47      0.42      1022
   macro avg       0.38      0.47      0.42      1022
weighted avg       0.38      0.47      0.42      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    37.51% |    46.87% |    41.67% |    81.59%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0714 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 2.65 seconds
  - Step 1: Loading Vocabs:    0.0528s
  - Step 2: Model Loading:     0.6192s
  - Step 3: Batch Inference:   0.97s
  - Step 4: Metric Report:     0.0714s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.04 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2334, 'I-KP': 845, 'O': 14058}
Confusion Matrix:
[[ 1371    94   857]
 [   59   382   356]
 [  904   369 12845]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1371.0 |   951.0 |   963.0 |  13952.0 |   0.8890 |   0.1110 |   0.5874 |   0.5904 |   0.9354 |   0.5889
I-KP       |   382.0 |   415.0 |   463.0 |  15977.0 |   0.9491 |   0.0509 |   0.4521 |   0.4793 |   0.9718 |   0.4653
O          | 12845.0 |  1273.0 |  1213.0 |   1906.0 |   0.8558 |   0.1442 |   0.9137 |   0.9098 |   0.6111 |   0.9118
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8979 |   0.1021 |   0.6511 |   0.6599 |   0.8395 |   0.6553
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.53      0.53      0.53      2322

   micro avg       0.53      0.53      0.53      2322
   macro avg       0.53      0.53      0.53      2322
weighted avg       0.53      0.53      0.53      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    52.78% |    53.06% |    52.92% |    84.69%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1390 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 5.82 seconds
  - Step 1: Loading Vocabs:    0.0528s
  - Step 2: Model Loading:     0.6192s
  - Step 3: Batch Inference:   2.04s
  - Step 4: Metric Report:     0.1390s
==================================================

============================================================
Mode testGS completed in 5.83 seconds
============================================================
