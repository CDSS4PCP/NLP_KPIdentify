# R8 HAN-CRF (k=5 pooled train+test for CV, fold=1, freeze embeddings, fixed+block defaults, final eval GS only)
Run started: 2026-05-29T18:33:09-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --earlyStopPatience 3 --hanUseBlockDiagonal --hanBatchMode fixed --hanFreezeEmbeddings --kFolds 5 --kFoldIndex 1 --kFoldSeed 42 --cvPoolTrainAndTest
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
CV pooling enabled: using train.json + test.json (train_docs=2461, test_docs=820, pooled_docs=3281).
Using k-fold split: k=5, fold=1, seed=42 (train_docs=2625, val_docs=656).
Step 1: Loaded training data JSON in 0.5461 seconds (train_docs=2625, val_docs=656).
Step 2: Loaded vocabularies in 0.0547 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.6598 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.5910 seconds (BiLM weights: True).
Label diagnostics [train] | docs=2625 tokens=601086 kp_tokens=157110 kp_ratio=0.2614 kw_nonempty=99243/99245 kw_matched=76228 kw_unmatched=23015 match_ratio=0.7681
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=23009, no_span_match=6
Label diagnostics [val] | docs=656 tokens=152369 kp_tokens=40094 kp_ratio=0.2631 kw_nonempty=25267/25267 kw_matched=19450 kw_unmatched=5817 match_ratio=0.7698
Label diagnostics [val] top unmatched keywords: patients, implementation, management, monitoring, CDSS
Label diagnostics [val] unmatched reasons: overlap_conflict=5816, no_span_match=1
Step 5a: Prepared 430 train and 110 val CPU batches in 56.39s (cached for all epochs).
Epoch  1/20 | Train Loss: 8.5141 | Val Loss: 5.5162 | Time: 45.02s | Checkpoint Saved
Epoch  2/20 | Train Loss: 4.8558 | Val Loss: 4.8182 | Time: 44.46s | Checkpoint Saved
Epoch  3/20 | Train Loss: 3.9219 | Val Loss: 4.7151 | Time: 40.39s | Checkpoint Saved
Epoch  4/20 | Train Loss: 3.3930 | Val Loss: 4.6671 | Time: 39.46s | Checkpoint Saved
Epoch  5/20 | Train Loss: 3.0272 | Val Loss: 4.7440 | Time: 44.57s | No Save
Epoch  6/20 | Train Loss: 2.7412 | Val Loss: 4.6864 | Time: 45.94s | No Save
Epoch  7/20 | Train Loss: 2.4610 | Val Loss: 4.9665 | Time: 43.42s | No Save
Early stopping at epoch 7 after 3 non-improving validation epochs (best epoch=4, best val loss=4.6671).
Best checkpoint selected from epoch 4 with val loss 4.6671.
Step 5: Completed 7 training epochs in 394.40 seconds (Avg per epoch: 43.32s; prep: 56.39s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 397.25 seconds
  - Step 1: Loading Data:      0.5461s
  - Step 2: Loading Vocab:     0.0547s
  - Step 3: Embeddings Load:   0.6598s
  - Step 4: Model & Device:    1.5910s
  - Step 5: Epochs Train Loop: 394.40s (Avg: 43.32s/epoch)
==================================================

============================================================
Mode train completed in 397.40 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0644 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5536 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.31 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1450, 'I-KP': 578, 'O': 6898}
Confusion Matrix:
[[ 622   43  357]
 [  55  229  151]
 [ 773  306 6390]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   622.0 |   400.0 |   828.0 |   7076.0 |   0.8624 |   0.1376 |   0.4290 |   0.6086 |   0.8952 |   0.5032
I-KP       |   229.0 |   206.0 |   349.0 |   8142.0 |   0.9378 |   0.0622 |   0.3962 |   0.5264 |   0.9589 |   0.4521
O          |  6390.0 |  1079.0 |   508.0 |    949.0 |   0.8222 |   0.1778 |   0.9264 |   0.8555 |   0.6513 |   0.8895
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8742 |   0.1258 |   0.5838 |   0.6635 |   0.8352 |   0.6150
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.37      0.52      0.43      1022

   micro avg       0.37      0.52      0.43      1022
   macro avg       0.37      0.52      0.43      1022
weighted avg       0.37      0.52      0.43      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    36.62% |    51.96% |    42.96% |    81.12%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1053 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 3.00 seconds
  - Step 1: Loading Vocabs:    0.0644s
  - Step 2: Model Loading:     0.5536s
  - Step 3: Batch Inference:   1.31s
  - Step 4: Metric Report:     0.1053s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.33 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2575, 'I-KP': 941, 'O': 13721}
Confusion Matrix:
[[ 1450   103   769]
 [   80   405   312]
 [ 1045   433 12640]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1450.0 |   872.0 |  1125.0 |  13790.0 |   0.8841 |   0.1159 |   0.5631 |   0.6245 |   0.9246 |   0.5922
I-KP       |   405.0 |   392.0 |   536.0 |  15904.0 |   0.9462 |   0.0538 |   0.4304 |   0.5082 |   0.9674 |   0.4661
O          | 12640.0 |  1478.0 |  1081.0 |   2038.0 |   0.8515 |   0.1485 |   0.9212 |   0.8953 |   0.6534 |   0.9081
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8939 |   0.1061 |   0.6382 |   0.6760 |   0.8485 |   0.6554
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.51      0.56      0.53      2322

   micro avg       0.51      0.56      0.53      2322
   macro avg       0.51      0.56      0.53      2322
weighted avg       0.51      0.56      0.53      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    50.60% |    56.12% |    53.22% |    84.09%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.4439 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 6.91 seconds
  - Step 1: Loading Vocabs:    0.0644s
  - Step 2: Model Loading:     0.5536s
  - Step 3: Batch Inference:   2.33s
  - Step 4: Metric Report:     0.4439s
==================================================

============================================================
Mode testGS completed in 6.92 seconds
============================================================
