# R7 HAN-CRF (k=5 fold=0, freeze embeddings, fixed+block defaults)
Run started: 2026-05-29T17:49:54-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,test,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --earlyStopPatience 3 --hanUseBlockDiagonal --hanBatchMode fixed --hanFreezeEmbeddings --kFolds 5 --kFoldIndex 0 --kFoldSeed 42
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
Using k-fold split: k=5, fold=0, seed=42 (train_docs=1968, val_docs=493).
Step 1: Loaded training data JSON in 0.4041 seconds (train_docs=1968, val_docs=493).
Step 2: Loaded vocabularies in 0.0523 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.6764 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.7106 seconds (BiLM weights: True).
Label diagnostics [train] | docs=1968 tokens=453270 kp_tokens=118483 kp_ratio=0.2614 kw_nonempty=74577/74579 kw_matched=57385 kw_unmatched=17192 match_ratio=0.7695
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=17186, no_span_match=6
Label diagnostics [val] | docs=493 tokens=112215 kp_tokens=29121 kp_ratio=0.2595 kw_nonempty=18492/18492 kw_matched=14276 kw_unmatched=4216 match_ratio=0.7720
Label diagnostics [val] top unmatched keywords: patients, CDSS, implementation, management, CDS
Label diagnostics [val] unmatched reasons: overlap_conflict=4216
Step 5a: Prepared 325 train and 81 val CPU batches in 39.21s (cached for all epochs).
Epoch  1/20 | Train Loss: 10.5464 | Val Loss: 7.2785 | Time: 35.80s | Checkpoint Saved
Epoch  2/20 | Train Loss: 6.2759 | Val Loss: 5.9954 | Time: 31.31s | Checkpoint Saved
Epoch  3/20 | Train Loss: 4.8596 | Val Loss: 5.7843 | Time: 31.05s | Checkpoint Saved
Epoch  4/20 | Train Loss: 4.0702 | Val Loss: 5.3367 | Time: 33.11s | Checkpoint Saved
Epoch  5/20 | Train Loss: 3.5272 | Val Loss: 5.3161 | Time: 31.38s | Checkpoint Saved
Epoch  6/20 | Train Loss: 3.1174 | Val Loss: 5.3929 | Time: 30.83s | No Save
Epoch  7/20 | Train Loss: 2.7590 | Val Loss: 5.3800 | Time: 31.86s | No Save
Epoch  8/20 | Train Loss: 2.4577 | Val Loss: 5.6229 | Time: 32.03s | No Save
Early stopping at epoch 8 after 3 non-improving validation epochs (best epoch=5, best val loss=5.3161).
Best checkpoint selected from epoch 5 with val loss 5.3161.
Step 5: Completed 8 training epochs in 319.83 seconds (Avg per epoch: 32.17s; prep: 39.21s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 322.67 seconds
  - Step 1: Loading Data:      0.4041s
  - Step 2: Loading Vocab:     0.0523s
  - Step 3: Embeddings Load:   0.6764s
  - Step 4: Model & Device:    1.7106s
  - Step 5: Epochs Train Loop: 319.83s (Avg: 32.17s/epoch)
==================================================

============================================================
Mode train completed in 322.81 seconds
============================================================
============================================================
Running mode: test
============================================================
Auto-selected device: cuda
Running in test mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0740 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.4995 seconds.

Evaluating on Test dataset: test.json
Label diagnostics [test] | docs=820 tokens=187970 kp_tokens=49600 kp_ratio=0.2639 kw_nonempty=31441/31441 kw_matched=24017 kw_unmatched=7424 match_ratio=0.7639
Label diagnostics [test] top unmatched keywords: patients, implementation, monitoring, management, CDSS
Label diagnostics [test] unmatched reasons: overlap_conflict=7423, no_span_match=1
Step 3: Inference prediction loop completed in 20.57 seconds.
Metrics on Test DS:
Label counts (target): {'B-KP': 37737, 'I-KP': 11851, 'O': 138314}
Label counts (pred):   {'B-KP': 39156, 'I-KP': 12392, 'O': 136354}
Confusion Matrix:
[[ 30835    817   6085]
 [   721   9036   2094]
 [  7600   2539 128175]]
Row sums (target support by label order): [37737, 11851, 138314]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       | 30835.0 |  6902.0 |  8321.0 | 141844.0 |   0.9190 |   0.0810 |   0.7875 |   0.8171 |   0.9446 |   0.8020
I-KP       |  9036.0 |  2815.0 |  3356.0 | 172695.0 |   0.9672 |   0.0328 |   0.7292 |   0.7625 |   0.9809 |   0.7455
O          | 128175.0 | 10139.0 |  8179.0 |  41409.0 |   0.9025 |   0.0975 |   0.9400 |   0.9267 |   0.8351 |   0.9333
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9296 |   0.0704 |   0.8189 |   0.8354 |   0.9202 |   0.8269
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.74      0.77      0.76     37737

   micro avg       0.74      0.77      0.76     37737
   macro avg       0.74      0.77      0.76     37737
weighted avg       0.74      0.77      0.76     37737

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    74.49% |    77.29% |    75.87% |    89.43%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 2.7559 seconds.

==================================================
EVALUATION SUMMARY ON TEST (HAN_CRF on device: cuda)
Total Dataset Eval Time: 30.54 seconds
  - Step 1: Loading Vocabs:    0.0740s
  - Step 2: Model Loading:     0.4995s
  - Step 3: Batch Inference:   20.57s
  - Step 4: Metric Report:     2.7559s
==================================================

============================================================
Mode test completed in 30.57 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0623 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5953 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.25 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1531, 'I-KP': 558, 'O': 6837}
Confusion Matrix:
[[ 615   45  362]
 [  57  224  154]
 [ 859  289 6321]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   615.0 |   407.0 |   916.0 |   6988.0 |   0.8518 |   0.1482 |   0.4017 |   0.6018 |   0.8841 |   0.4818
I-KP       |   224.0 |   211.0 |   334.0 |   8157.0 |   0.9389 |   0.0611 |   0.4014 |   0.5149 |   0.9607 |   0.4512
O          |  6321.0 |  1148.0 |   516.0 |    941.0 |   0.8136 |   0.1864 |   0.9245 |   0.8463 |   0.6458 |   0.8837
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8681 |   0.1319 |   0.5759 |   0.6543 |   0.8302 |   0.6055
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.35      0.52      0.42      1022

   micro avg       0.35      0.52      0.42      1022
   macro avg       0.35      0.52      0.42      1022
weighted avg       0.35      0.52      0.42      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    34.94% |    52.35% |    41.91% |    80.22%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0896 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 2.93 seconds
  - Step 1: Loading Vocabs:    0.0623s
  - Step 2: Model Loading:     0.5953s
  - Step 3: Batch Inference:   1.25s
  - Step 4: Metric Report:     0.0896s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.62 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2724, 'I-KP': 947, 'O': 13566}
Confusion Matrix:
[[ 1469   100   753]
 [   85   417   295]
 [ 1170   430 12518]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1469.0 |   853.0 |  1255.0 |  13660.0 |   0.8777 |   0.1223 |   0.5393 |   0.6326 |   0.9159 |   0.5822
I-KP       |   417.0 |   380.0 |   530.0 |  15910.0 |   0.9472 |   0.0528 |   0.4403 |   0.5232 |   0.9678 |   0.4782
O          | 12518.0 |  1600.0 |  1048.0 |   2071.0 |   0.8464 |   0.1536 |   0.9227 |   0.8867 |   0.6640 |   0.9043
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8904 |   0.1096 |   0.6341 |   0.6808 |   0.8492 |   0.6549
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.48      0.56      0.52      2322

   micro avg       0.48      0.56      0.52      2322
   macro avg       0.48      0.56      0.52      2322
weighted avg       0.48      0.56      0.52      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    47.94% |    56.24% |    51.76% |    83.56%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1649 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 6.78 seconds
  - Step 1: Loading Vocabs:    0.0623s
  - Step 2: Model Loading:     0.5953s
  - Step 3: Batch Inference:   2.62s
  - Step 4: Metric Report:     0.1649s
==================================================

============================================================
Mode testGS completed in 6.79 seconds
============================================================
