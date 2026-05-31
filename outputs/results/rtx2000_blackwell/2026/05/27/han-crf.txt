(cdss-gpu) rohangoli@TD-6L0NCJ4:~/remote_mount$ python src/nlp/jobs/gna_pipeline.py --mode train,test,testGS --taggingSchema BIO --model han_crf
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
Step 1: Loaded training data JSON in 0.5099 seconds (train_docs=2461, val_docs=0).
Step 2: Loaded vocabularies in 0.0710 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.7863 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.8830 seconds (BiLM weights: True).
Label diagnostics [train] | docs=2461 tokens=565485 kp_tokens=147604 kp_ratio=0.2610 kw_nonempty=93069/93071 kw_matched=71661 kw_unmatched=21408 match_ratio=0.7700
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=21402, no_span_match=6
Step 5a: Prepared 2461 train and 0 val CPU batches in 41.12s (cached for all epochs).
Epoch  1/20 | Train Loss: 6.8629 | Val Loss: n/a | Time: 204.47s | Checkpoint Saved
Epoch  2/20 | Train Loss: 4.1596 | Val Loss: n/a | Time: 208.04s | Checkpoint Saved
Epoch  3/20 | Train Loss: 3.3905 | Val Loss: n/a | Time: 204.38s | Checkpoint Saved
Epoch  4/20 | Train Loss: 2.9465 | Val Loss: n/a | Time: 220.09s | Checkpoint Saved
Epoch  5/20 | Train Loss: 2.5923 | Val Loss: n/a | Time: 225.67s | Checkpoint Saved
Epoch  6/20 | Train Loss: 2.2718 | Val Loss: n/a | Time: 219.09s | Checkpoint Saved
Epoch  7/20 | Train Loss: 1.9725 | Val Loss: n/a | Time: 208.70s | Checkpoint Saved
Epoch  8/20 | Train Loss: 1.7088 | Val Loss: n/a | Time: 204.86s | Checkpoint Saved
Epoch  9/20 | Train Loss: 1.4900 | Val Loss: n/a | Time: 201.41s | Checkpoint Saved
Epoch 10/20 | Train Loss: 1.2930 | Val Loss: n/a | Time: 198.79s | Checkpoint Saved
Epoch 11/20 | Train Loss: 1.1503 | Val Loss: n/a | Time: 200.36s | Checkpoint Saved
Epoch 12/20 | Train Loss: 1.0170 | Val Loss: n/a | Time: 211.79s | Checkpoint Saved
Epoch 13/20 | Train Loss: 0.9177 | Val Loss: n/a | Time: 200.89s | Checkpoint Saved
Epoch 14/20 | Train Loss: 0.8198 | Val Loss: n/a | Time: 202.32s | Checkpoint Saved
Epoch 15/20 | Train Loss: 0.7487 | Val Loss: n/a | Time: 202.44s | Checkpoint Saved
Epoch 16/20 | Train Loss: 0.6958 | Val Loss: n/a | Time: 203.67s | Checkpoint Saved
Epoch 17/20 | Train Loss: 0.6482 | Val Loss: n/a | Time: 204.86s | Checkpoint Saved
Epoch 18/20 | Train Loss: 0.5927 | Val Loss: n/a | Time: 204.89s | Checkpoint Saved
Epoch 19/20 | Train Loss: 0.5718 | Val Loss: n/a | Time: 204.96s | Checkpoint Saved
Epoch 20/20 | Train Loss: 0.5466 | Val Loss: n/a | Time: 204.35s | Checkpoint Saved
Step 5: Completed 20 training epochs in 4211.34 seconds (Avg per epoch: 206.80s; prep: 41.12s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 4214.60 seconds
  - Step 1: Loading Data:      0.5099s
  - Step 2: Loading Vocab:     0.0710s
  - Step 3: Embeddings Load:   0.7863s
  - Step 4: Model & Device:    1.8830s
  - Step 5: Epochs Train Loop: 4211.34s (Avg: 206.80s/epoch)
==================================================

============================================================
Mode train completed in 4215.56 seconds
============================================================
============================================================
Running mode: test
============================================================
Auto-selected device: cuda
Running in test mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.1500 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.7643 seconds.

Evaluating on Test dataset: test.json
Label diagnostics [test] | docs=820 tokens=187970 kp_tokens=49600 kp_ratio=0.2639 kw_nonempty=31441/31441 kw_matched=24017 kw_unmatched=7424 match_ratio=0.7639
Label diagnostics [test] top unmatched keywords: patients, implementation, monitoring, management, CDSS
Label diagnostics [test] unmatched reasons: overlap_conflict=7423, no_span_match=1
Step 3: Inference prediction loop completed in 38.02 seconds.
Metrics on Test DS:
Label counts (target): {'B-KP': 37737, 'I-KP': 11851, 'O': 138314}
Label counts (pred):   {'B-KP': 39416, 'I-KP': 12565, 'O': 135921}
Confusion Matrix:
[[ 30775    779   6183]
 [   733   9115   2003]
 [  7908   2671 127735]]
Row sums (target support by label order): [37737, 11851, 138314]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       | 30775.0 |  6962.0 |  8641.0 | 141524.0 |   0.9170 |   0.0830 |   0.7808 |   0.8155 |   0.9425 |   0.7978
I-KP       |  9115.0 |  2736.0 |  3450.0 | 172601.0 |   0.9671 |   0.0329 |   0.7254 |   0.7691 |   0.9804 |   0.7466
O          | 127735.0 | 10579.0 |  8186.0 |  41402.0 |   0.9001 |   0.0999 |   0.9398 |   0.9235 |   0.8349 |   0.9316
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9281 |   0.0719 |   0.8153 |   0.8361 |   0.9193 |   0.8253
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.74      0.78      0.76     37737

   micro avg       0.74      0.78      0.76     37737
   macro avg       0.74      0.78      0.76     37737
weighted avg       0.74      0.78      0.76     37737

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    74.28% |    77.59% |    75.90% |    89.21%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 5.1573 seconds.

==================================================
EVALUATION SUMMARY ON TEST (HAN_CRF on device: cuda)
Total Dataset Eval Time: 52.05 seconds
  - Step 1: Loading Vocabs:    0.1500s
  - Step 2: Model Loading:     0.7643s
  - Step 3: Batch Inference:   38.02s
  - Step 4: Metric Report:     5.1573s
==================================================

============================================================
Mode test completed in 52.10 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0630 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.8055 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.98 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1535, 'I-KP': 550, 'O': 6841}
Confusion Matrix:
[[ 593   46  383]
 [  54  209  172]
 [ 888  295 6286]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   593.0 |   429.0 |   942.0 |   6962.0 |   0.8464 |   0.1536 |   0.3863 |   0.5802 |   0.8808 |   0.4638
I-KP       |   209.0 |   226.0 |   341.0 |   8150.0 |   0.9365 |   0.0635 |   0.3800 |   0.4805 |   0.9598 |   0.4244
O          |  6286.0 |  1183.0 |   555.0 |    902.0 |   0.8053 |   0.1947 |   0.9189 |   0.8416 |   0.6191 |   0.8785
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8627 |   0.1373 |   0.5617 |   0.6341 |   0.8199 |   0.5889
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.33      0.49      0.39      1022

   micro avg       0.33      0.49      0.39      1022
   macro avg       0.33      0.49      0.39      1022
weighted avg       0.33      0.49      0.39      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    32.90% |    49.41% |    39.50% |    79.41%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0831 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 4.46 seconds
  - Step 1: Loading Vocabs:    0.0630s
  - Step 2: Model Loading:     0.8055s
  - Step 3: Batch Inference:   1.98s
  - Step 4: Metric Report:     0.0831s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 3.33 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2785, 'I-KP': 950, 'O': 13502}
Confusion Matrix:
[[ 1487    98   737]
 [   81   415   301]
 [ 1217   437 12464]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1487.0 |   835.0 |  1298.0 |  13617.0 |   0.8763 |   0.1237 |   0.5339 |   0.6404 |   0.9130 |   0.5823
I-KP       |   415.0 |   382.0 |   535.0 |  15905.0 |   0.9468 |   0.0532 |   0.4368 |   0.5207 |   0.9675 |   0.4751
O          | 12464.0 |  1654.0 |  1038.0 |   2081.0 |   0.8438 |   0.1562 |   0.9231 |   0.8828 |   0.6672 |   0.9025
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8890 |   0.1110 |   0.6313 |   0.6813 |   0.8492 |   0.6533
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.49      0.58      0.53      2322

   micro avg       0.49      0.58      0.53      2322
   macro avg       0.49      0.58      0.53      2322
weighted avg       0.49      0.58      0.53      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    48.58% |    58.27% |    52.99% |    83.34%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1924 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 8.91 seconds
  - Step 1: Loading Vocabs:    0.0630s
  - Step 2: Model Loading:     0.8055s
  - Step 3: Batch Inference:   3.33s
  - Step 4: Metric Report:     0.1924s
==================================================

============================================================
Mode testGS completed in 8.93 seconds
============================================================
(cdss-gpu) rohangoli@TD-6L0NCJ4:~/remote_mount$