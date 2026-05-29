(cdss-gpu) rohangoli@TD-6L0NCJ4:~/remote_mount$ python src/nlp/jobs/gna_pipeline.py --mode train,test,testGS --taggingSchema BIO --model han_crf --epochs 20 --batchSize 64 --validationSplit 0.0 --earlyStopPatience 0 --hanBatchMode fixed --hanUseBlockDiagonal
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
Step 1: Loaded training data JSON in 0.5325 seconds (train_docs=2461, val_docs=0).
Step 2: Loaded vocabularies in 0.0608 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.8211 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 2.0651 seconds (BiLM weights: True).
Label diagnostics [train] | docs=2461 tokens=565485 kp_tokens=147604 kp_ratio=0.2610 kw_nonempty=93069/93071 kw_matched=71661 kw_unmatched=21408 match_ratio=0.7700
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=21402, no_span_match=6
Step 5a: Prepared 405 train and 0 val CPU batches in 35.22s (cached for all epochs).
Epoch  1/20 | Train Loss: 9.9963 | Val Loss: n/a | Time: 36.40s | Checkpoint Saved
Epoch  2/20 | Train Loss: 5.3126 | Val Loss: n/a | Time: 32.14s | Checkpoint Saved
Epoch  3/20 | Train Loss: 4.1550 | Val Loss: n/a | Time: 32.95s | Checkpoint Saved
Epoch  4/20 | Train Loss: 3.5330 | Val Loss: n/a | Time: 32.83s | Checkpoint Saved
Epoch  5/20 | Train Loss: 3.1310 | Val Loss: n/a | Time: 32.60s | Checkpoint Saved
Epoch  6/20 | Train Loss: 2.8088 | Val Loss: n/a | Time: 36.40s | Checkpoint Saved
Epoch  7/20 | Train Loss: 2.5350 | Val Loss: n/a | Time: 34.52s | Checkpoint Saved
Epoch  8/20 | Train Loss: 2.2797 | Val Loss: n/a | Time: 33.60s | Checkpoint Saved
Epoch  9/20 | Train Loss: 2.0351 | Val Loss: n/a | Time: 32.84s | Checkpoint Saved
Epoch 10/20 | Train Loss: 1.8105 | Val Loss: n/a | Time: 32.66s | Checkpoint Saved
Epoch 11/20 | Train Loss: 1.6176 | Val Loss: n/a | Time: 33.39s | Checkpoint Saved
Epoch 12/20 | Train Loss: 1.4349 | Val Loss: n/a | Time: 33.79s | Checkpoint Saved
Epoch 13/20 | Train Loss: 1.2753 | Val Loss: n/a | Time: 33.72s | Checkpoint Saved
Epoch 14/20 | Train Loss: 1.1370 | Val Loss: n/a | Time: 33.54s | Checkpoint Saved
Epoch 15/20 | Train Loss: 1.0052 | Val Loss: n/a | Time: 33.18s | Checkpoint Saved
Epoch 16/20 | Train Loss: 0.9004 | Val Loss: n/a | Time: 33.15s | Checkpoint Saved
Epoch 17/20 | Train Loss: 0.8172 | Val Loss: n/a | Time: 33.17s | Checkpoint Saved
Epoch 18/20 | Train Loss: 0.7334 | Val Loss: n/a | Time: 30.46s | Checkpoint Saved
Epoch 19/20 | Train Loss: 0.6749 | Val Loss: n/a | Time: 32.66s | Checkpoint Saved
Epoch 20/20 | Train Loss: 0.5953 | Val Loss: n/a | Time: 34.02s | Checkpoint Saved
Step 5: Completed 20 training epochs in 733.97 seconds (Avg per epoch: 33.40s; prep: 35.22s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 737.45 seconds
  - Step 1: Loading Data:      0.5325s
  - Step 2: Loading Vocab:     0.0608s
  - Step 3: Embeddings Load:   0.8211s
  - Step 4: Model & Device:    2.0651s
  - Step 5: Epochs Train Loop: 733.97s (Avg: 33.40s/epoch)
==================================================

============================================================
Mode train completed in 737.62 seconds
============================================================
============================================================
Running mode: test
============================================================
Auto-selected device: cuda
Running in test mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0731 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5325 seconds.

Evaluating on Test dataset: test.json
Label diagnostics [test] | docs=820 tokens=187970 kp_tokens=49600 kp_ratio=0.2639 kw_nonempty=31441/31441 kw_matched=24017 kw_unmatched=7424 match_ratio=0.7639
Label diagnostics [test] top unmatched keywords: patients, implementation, monitoring, management, CDSS
Label diagnostics [test] unmatched reasons: overlap_conflict=7423, no_span_match=1
Step 3: Inference prediction loop completed in 18.62 seconds.
Metrics on Test DS:
Label counts (target): {'B-KP': 37737, 'I-KP': 11851, 'O': 138314}
Label counts (pred):   {'B-KP': 36433, 'I-KP': 11524, 'O': 139945}
Confusion Matrix:
[[ 29389    732   7616]
 [   649   8655   2547]
 [  6395   2137 129782]]
Row sums (target support by label order): [37737, 11851, 138314]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       | 29389.0 |  8348.0 |  7044.0 | 143121.0 |   0.9181 |   0.0819 |   0.8067 |   0.7788 |   0.9531 |   0.7925
I-KP       |  8655.0 |  3196.0 |  2869.0 | 173182.0 |   0.9677 |   0.0323 |   0.7510 |   0.7303 |   0.9837 |   0.7405
O          | 129782.0 |  8532.0 | 10163.0 |  39425.0 |   0.9005 |   0.0995 |   0.9274 |   0.9383 |   0.7951 |   0.9328
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9288 |   0.0712 |   0.8284 |   0.8158 |   0.9106 |   0.8219
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.77      0.74      0.76     37737

   micro avg       0.77      0.74      0.76     37737
   macro avg       0.77      0.74      0.76     37737
weighted avg       0.77      0.74      0.76     37737

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    76.89% |    74.24% |    75.54% |    89.32%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 2.6783 seconds.

==================================================
EVALUATION SUMMARY ON TEST (HAN_CRF on device: cuda)
Total Dataset Eval Time: 28.51 seconds
  - Step 1: Loading Vocabs:    0.0731s
  - Step 2: Model Loading:     0.5325s
  - Step 3: Batch Inference:   18.62s
  - Step 4: Metric Report:     2.6783s
==================================================

============================================================
Mode test completed in 28.54 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0545 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.6427 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.09 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1440, 'I-KP': 527, 'O': 6959}
Confusion Matrix:
[[ 571   47  404]
 [  45  194  196]
 [ 824  286 6359]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   571.0 |   451.0 |   869.0 |   7035.0 |   0.8521 |   0.1479 |   0.3965 |   0.5587 |   0.8901 |   0.4639
I-KP       |   194.0 |   241.0 |   333.0 |   8158.0 |   0.9357 |   0.0643 |   0.3681 |   0.4460 |   0.9608 |   0.4033
O          |  6359.0 |  1110.0 |   600.0 |    857.0 |   0.8084 |   0.1916 |   0.9138 |   0.8514 |   0.5882 |   0.8815
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8654 |   0.1346 |   0.5595 |   0.6187 |   0.8130 |   0.5829
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.35      0.49      0.41      1022

   micro avg       0.35      0.49      0.41      1022
   macro avg       0.35      0.49      0.41      1022
weighted avg       0.35      0.49      0.41      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    34.65% |    48.83% |    40.54% |    79.81%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0688 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 2.55 seconds
  - Step 1: Loading Vocabs:    0.0545s
  - Step 2: Model Loading:     0.6427s
  - Step 3: Batch Inference:   1.09s
  - Step 4: Metric Report:     0.0688s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.02 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2590, 'I-KP': 855, 'O': 13792}
Confusion Matrix:
[[ 1442   104   776]
 [   71   386   340]
 [ 1077   365 12676]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1442.0 |   880.0 |  1148.0 |  13767.0 |   0.8823 |   0.1177 |   0.5568 |   0.6210 |   0.9230 |   0.5871
I-KP       |   386.0 |   411.0 |   469.0 |  15971.0 |   0.9489 |   0.0511 |   0.4515 |   0.4843 |   0.9715 |   0.4673
O          | 12676.0 |  1442.0 |  1116.0 |   2003.0 |   0.8516 |   0.1484 |   0.9191 |   0.8979 |   0.6422 |   0.9083
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8943 |   0.1057 |   0.6424 |   0.6677 |   0.8456 |   0.6543
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.51      0.57      0.54      2322

   micro avg       0.51      0.57      0.54      2322
   macro avg       0.51      0.57      0.54      2322
weighted avg       0.51      0.57      0.54      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    50.93% |    56.80% |    53.71% |    84.14%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.4601 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 5.89 seconds
  - Step 1: Loading Vocabs:    0.0545s
  - Step 2: Model Loading:     0.6427s
  - Step 3: Batch Inference:   2.02s
  - Step 4: Metric Report:     0.4601s
==================================================

============================================================
Mode testGS completed in 5.90 seconds
============================================================
(cdss-gpu) rohangoli@TD-6L0NCJ4:~/remote_mount$