# R3 HAN-CRF (freeze embeddings, fixed-batch+block-diagonal defaults)
Run started: 2026-05-29T17:05:39-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,test,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --validationSplit 0.0 --earlyStopPatience 0 --hanUseBlockDiagonal --hanBatchMode fixed --hanFreezeEmbeddings
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
Step 1: Loaded training data JSON in 0.4065 seconds (train_docs=2461, val_docs=0).
Step 2: Loaded vocabularies in 0.0534 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.7188 seconds.
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.7000 seconds (BiLM weights: True).
Label diagnostics [train] | docs=2461 tokens=565485 kp_tokens=147604 kp_ratio=0.2610 kw_nonempty=93069/93071 kw_matched=71661 kw_unmatched=21408 match_ratio=0.7700
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=21402, no_span_match=6
Step 5a: Prepared 405 train and 0 val CPU batches in 39.23s (cached for all epochs).
Epoch  1/20 | Train Loss: 12.7879 | Val Loss: n/a | Time: 35.11s | Checkpoint Saved
Epoch  2/20 | Train Loss: 7.0786 | Val Loss: n/a | Time: 32.90s | Checkpoint Saved
Epoch  3/20 | Train Loss: 5.4663 | Val Loss: n/a | Time: 32.99s | Checkpoint Saved
Epoch  4/20 | Train Loss: 4.4710 | Val Loss: n/a | Time: 34.59s | Checkpoint Saved
Epoch  5/20 | Train Loss: 3.7894 | Val Loss: n/a | Time: 33.57s | Checkpoint Saved
Epoch  6/20 | Train Loss: 3.3011 | Val Loss: n/a | Time: 36.83s | Checkpoint Saved
Epoch  7/20 | Train Loss: 2.8992 | Val Loss: n/a | Time: 35.26s | Checkpoint Saved
Epoch  8/20 | Train Loss: 2.5740 | Val Loss: n/a | Time: 33.98s | Checkpoint Saved
Epoch  9/20 | Train Loss: 2.2988 | Val Loss: n/a | Time: 34.59s | Checkpoint Saved
Epoch 10/20 | Train Loss: 2.0431 | Val Loss: n/a | Time: 41.44s | Checkpoint Saved
Epoch 11/20 | Train Loss: 1.8209 | Val Loss: n/a | Time: 37.44s | Checkpoint Saved
Epoch 12/20 | Train Loss: 1.6423 | Val Loss: n/a | Time: 34.17s | Checkpoint Saved
Epoch 13/20 | Train Loss: 1.4594 | Val Loss: n/a | Time: 34.66s | Checkpoint Saved
Epoch 14/20 | Train Loss: 1.3096 | Val Loss: n/a | Time: 36.36s | Checkpoint Saved
Epoch 15/20 | Train Loss: 1.1637 | Val Loss: n/a | Time: 35.43s | Checkpoint Saved
Epoch 16/20 | Train Loss: 1.0362 | Val Loss: n/a | Time: 36.61s | Checkpoint Saved
Epoch 17/20 | Train Loss: 0.9444 | Val Loss: n/a | Time: 34.89s | Checkpoint Saved
Epoch 18/20 | Train Loss: 0.8474 | Val Loss: n/a | Time: 35.56s | Checkpoint Saved
Epoch 19/20 | Train Loss: 0.7538 | Val Loss: n/a | Time: 35.28s | Checkpoint Saved
Epoch 20/20 | Train Loss: 0.6901 | Val Loss: n/a | Time: 33.98s | Checkpoint Saved
Step 5: Completed 20 training epochs in 776.04 seconds (Avg per epoch: 35.28s; prep: 39.23s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 778.92 seconds
  - Step 1: Loading Data:      0.4065s
  - Step 2: Loading Vocab:     0.0534s
  - Step 3: Embeddings Load:   0.7188s
  - Step 4: Model & Device:    1.7000s
  - Step 5: Epochs Train Loop: 776.04s (Avg: 35.28s/epoch)
==================================================

============================================================
Mode train completed in 779.04 seconds
============================================================
============================================================
Running mode: test
============================================================
Auto-selected device: cuda
Running in test mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0540 seconds.
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5142 seconds.

Evaluating on Test dataset: test.json
Label diagnostics [test] | docs=820 tokens=187970 kp_tokens=49600 kp_ratio=0.2639 kw_nonempty=31441/31441 kw_matched=24017 kw_unmatched=7424 match_ratio=0.7639
Label diagnostics [test] top unmatched keywords: patients, implementation, monitoring, management, CDSS
Label diagnostics [test] unmatched reasons: overlap_conflict=7423, no_span_match=1
Step 3: Inference prediction loop completed in 18.82 seconds.
Metrics on Test DS:
Label counts (target): {'B-KP': 37737, 'I-KP': 11851, 'O': 138314}
Label counts (pred):   {'B-KP': 38582, 'I-KP': 12364, 'O': 136956}
Confusion Matrix:
[[ 30468    725   6544]
 [   669   9009   2173]
 [  7445   2630 128239]]
Row sums (target support by label order): [37737, 11851, 138314]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       | 30468.0 |  7269.0 |  8114.0 | 142051.0 |   0.9181 |   0.0819 |   0.7897 |   0.8074 |   0.9460 |   0.7984
I-KP       |  9009.0 |  2842.0 |  3355.0 | 172696.0 |   0.9670 |   0.0330 |   0.7286 |   0.7602 |   0.9809 |   0.7441
O          | 128239.0 | 10075.0 |  8717.0 |  40871.0 |   0.9000 |   0.1000 |   0.9364 |   0.9272 |   0.8242 |   0.9317
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9284 |   0.0716 |   0.8182 |   0.8316 |   0.9170 |   0.8248
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.75      0.77      0.76     37737

   micro avg       0.75      0.77      0.76     37737
   macro avg       0.75      0.77      0.76     37737
weighted avg       0.75      0.77      0.76     37737

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    74.94% |    76.62% |    75.77% |    89.26%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 2.6147 seconds.

==================================================
EVALUATION SUMMARY ON TEST (HAN_CRF on device: cuda)
Total Dataset Eval Time: 28.52 seconds
  - Step 1: Loading Vocabs:    0.0540s
  - Step 2: Model Loading:     0.5142s
  - Step 3: Batch Inference:   18.82s
  - Step 4: Metric Report:     2.6147s
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
Step 1: Loaded vocabulary mappings in 0.0600 seconds.
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.6264 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.18 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1415, 'I-KP': 474, 'O': 7037}
Confusion Matrix:
[[ 593   34  395]
 [  46  191  198]
 [ 776  249 6444]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   593.0 |   429.0 |   822.0 |   7082.0 |   0.8598 |   0.1402 |   0.4191 |   0.5802 |   0.8960 |   0.4867
I-KP       |   191.0 |   244.0 |   283.0 |   8208.0 |   0.9410 |   0.0590 |   0.4030 |   0.4391 |   0.9667 |   0.4202
O          |  6444.0 |  1025.0 |   593.0 |    864.0 |   0.8187 |   0.1813 |   0.9157 |   0.8628 |   0.5930 |   0.8885
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8732 |   0.1268 |   0.5793 |   0.6274 |   0.8186 |   0.5985
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.36      0.50      0.42      1022

   micro avg       0.36      0.50      0.42      1022
   macro avg       0.36      0.50      0.42      1022
weighted avg       0.36      0.50      0.42      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    35.97% |    49.80% |    41.77% |    80.98%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1310 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 2.99 seconds
  - Step 1: Loading Vocabs:    0.0600s
  - Step 2: Model Loading:     0.6264s
  - Step 3: Batch Inference:   1.18s
  - Step 4: Metric Report:     0.1310s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.46 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2510, 'I-KP': 829, 'O': 13898}
Confusion Matrix:
[[ 1449    92   781]
 [   72   380   345]
 [  989   357 12772]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1449.0 |   873.0 |  1061.0 |  13854.0 |   0.8878 |   0.1122 |   0.5773 |   0.6240 |   0.9289 |   0.5998
I-KP       |   380.0 |   417.0 |   449.0 |  15991.0 |   0.9498 |   0.0502 |   0.4584 |   0.4768 |   0.9727 |   0.4674
O          | 12772.0 |  1346.0 |  1126.0 |   1993.0 |   0.8566 |   0.1434 |   0.9190 |   0.9047 |   0.6390 |   0.9118
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8980 |   0.1020 |   0.6516 |   0.6685 |   0.8468 |   0.6596
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
Score (%)         |    52.23% |    56.46% |    54.26% |    84.71%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1431 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 6.56 seconds
  - Step 1: Loading Vocabs:    0.0600s
  - Step 2: Model Loading:     0.6264s
  - Step 3: Batch Inference:   2.46s
  - Step 4: Metric Report:     0.1431s
==================================================

============================================================
Mode testGS completed in 6.57 seconds
============================================================
