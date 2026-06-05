# R6 BiLSTM-CRF (validation/early-stop control)
Run started: 2026-05-29T17:27:24-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model bilstm_crf --mode train,test,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --validationSplit 0.1 --earlyStopPatience 3
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
Step 1: Loaded training data JSON in 0.4808 seconds (train_docs=2215, val_docs=246).
Step 2: Loaded vocabularies in 0.0605 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.6636 seconds.
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.5229 seconds (BiLM weights: True).
Label diagnostics [train] | docs=2215 tokens=511382 kp_tokens=133876 kp_ratio=0.2618 kw_nonempty=84211/84213 kw_matched=64782 kw_unmatched=19429 match_ratio=0.7693
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, treatment
Label diagnostics [train] unmatched reasons: overlap_conflict=19423, no_span_match=6
Label diagnostics [val] | docs=246 tokens=54103 kp_tokens=13728 kp_ratio=0.2537 kw_nonempty=8858/8858 kw_matched=6879 kw_unmatched=1979 match_ratio=0.7766
Label diagnostics [val] top unmatched keywords: patients, CDSS, alerts, CDS, implementation
Label diagnostics [val] unmatched reasons: overlap_conflict=1979
Step 5a: Prepared 367 train and 39 val CPU batches in 39.47s (cached for all epochs).
Epoch  1/20 | Train Loss: 8.7178 | Val Loss: 6.1388 | Time: 34.42s | Checkpoint Saved
Epoch  2/20 | Train Loss: 5.1293 | Val Loss: 5.2569 | Time: 31.90s | Checkpoint Saved
Epoch  3/20 | Train Loss: 4.0233 | Val Loss: 4.9364 | Time: 33.23s | Checkpoint Saved
Epoch  4/20 | Train Loss: 3.4037 | Val Loss: 4.9541 | Time: 34.94s | No Save
Epoch  5/20 | Train Loss: 2.9762 | Val Loss: 4.9569 | Time: 35.03s | No Save
Epoch  6/20 | Train Loss: 2.6231 | Val Loss: 5.2454 | Time: 33.08s | No Save
Early stopping at epoch 6 after 3 non-improving validation epochs (best epoch=3, best val loss=4.9364).
Best checkpoint selected from epoch 3 with val loss 4.9364.
Step 5: Completed 6 training epochs in 263.98 seconds (Avg per epoch: 33.77s; prep: 39.47s).

==================================================
TRAIN MODE SUMMARY (BILSTM_CRF on device: cuda)
Total Train Mode Time: 266.71 seconds
  - Step 1: Loading Data:      0.4808s
  - Step 2: Loading Vocab:     0.0605s
  - Step 3: Embeddings Load:   0.6636s
  - Step 4: Model & Device:    1.5229s
  - Step 5: Epochs Train Loop: 263.98s (Avg: 33.77s/epoch)
==================================================

============================================================
Mode train completed in 266.77 seconds
============================================================
============================================================
Running mode: test
============================================================
Auto-selected device: cuda
Running in test mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0766 seconds.
Loaded model weights from /home/rohangoli/remote_mount/interim_data/BiLSTM-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5739 seconds.

Evaluating on Test dataset: test.json
Label diagnostics [test] | docs=820 tokens=187970 kp_tokens=49600 kp_ratio=0.2639 kw_nonempty=31441/31441 kw_matched=24017 kw_unmatched=7424 match_ratio=0.7639
Label diagnostics [test] top unmatched keywords: patients, implementation, monitoring, management, CDSS
Label diagnostics [test] unmatched reasons: overlap_conflict=7423, no_span_match=1
Step 3: Inference prediction loop completed in 18.94 seconds.
Metrics on Test DS:
Label counts (target): {'B-KP': 37737, 'I-KP': 11851, 'O': 138314}
Label counts (pred):   {'B-KP': 37543, 'I-KP': 11321, 'O': 139038}
Confusion Matrix:
[[ 30075    659   7003]
 [   843   8485   2523]
 [  6625   2177 129512]]
Row sums (target support by label order): [37737, 11851, 138314]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       | 30075.0 |  7662.0 |  7468.0 | 142697.0 |   0.9195 |   0.0805 |   0.8011 |   0.7970 |   0.9503 |   0.7990
I-KP       |  8485.0 |  3366.0 |  2836.0 | 173215.0 |   0.9670 |   0.0330 |   0.7495 |   0.7160 |   0.9839 |   0.7323
O          | 129512.0 |  8802.0 |  9526.0 |  40062.0 |   0.9025 |   0.0975 |   0.9315 |   0.9364 |   0.8079 |   0.9339
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9296 |   0.0704 |   0.8274 |   0.8164 |   0.9140 |   0.8218
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
Score (%)         |    75.90% |    75.51% |    75.70% |    89.45%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 2.8846 seconds.

==================================================
EVALUATION SUMMARY ON TEST (BILSTM_CRF on device: cuda)
Total Dataset Eval Time: 29.03 seconds
  - Step 1: Loading Vocabs:    0.0766s
  - Step 2: Model Loading:     0.5739s
  - Step 3: Batch Inference:   18.94s
  - Step 4: Metric Report:     2.8846s
==================================================

============================================================
Mode test completed in 29.06 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0634 seconds.
Loaded model weights from /home/rohangoli/remote_mount/interim_data/BiLSTM-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5804 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.49 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1397, 'I-KP': 513, 'O': 7016}
Confusion Matrix:
[[ 590   46  386]
 [  51  219  165]
 [ 756  248 6465]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   590.0 |   432.0 |   807.0 |   7097.0 |   0.8612 |   0.1388 |   0.4223 |   0.5773 |   0.8979 |   0.4878
I-KP       |   219.0 |   216.0 |   294.0 |   8197.0 |   0.9429 |   0.0571 |   0.4269 |   0.5034 |   0.9654 |   0.4620
O          |  6465.0 |  1004.0 |   551.0 |    906.0 |   0.8258 |   0.1742 |   0.9215 |   0.8656 |   0.6218 |   0.8926
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8766 |   0.1234 |   0.5902 |   0.6488 |   0.8284 |   0.6142
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.37      0.50      0.42      1022

   micro avg       0.37      0.50      0.42      1022
   macro avg       0.37      0.50      0.42      1022
weighted avg       0.37      0.50      0.42      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    36.72% |    50.20% |    42.41% |    81.49%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0796 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (BILSTM_CRF on device: cuda)
Total Dataset Eval Time: 2.94 seconds
  - Step 1: Loading Vocabs:    0.0634s
  - Step 2: Model Loading:     0.5804s
  - Step 3: Batch Inference:   1.49s
  - Step 4: Metric Report:     0.0796s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.28 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2446, 'I-KP': 852, 'O': 13939}
Confusion Matrix:
[[ 1396   100   826]
 [   81   383   333]
 [  969   369 12780]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1396.0 |   926.0 |  1050.0 |  13865.0 |   0.8854 |   0.1146 |   0.5707 |   0.6012 |   0.9296 |   0.5856
I-KP       |   383.0 |   414.0 |   469.0 |  15971.0 |   0.9488 |   0.0512 |   0.4495 |   0.4806 |   0.9715 |   0.4645
O          | 12780.0 |  1338.0 |  1159.0 |   1960.0 |   0.8551 |   0.1449 |   0.9169 |   0.9052 |   0.6284 |   0.9110
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8964 |   0.1036 |   0.6457 |   0.6623 |   0.8432 |   0.6537
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.51      0.54      0.52      2322

   micro avg       0.51      0.54      0.52      2322
   macro avg       0.51      0.54      0.52      2322
weighted avg       0.51      0.54      0.52      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    50.98% |    53.70% |    52.31% |    84.46%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1619 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (BILSTM_CRF on device: cuda)
Total Dataset Eval Time: 6.30 seconds
  - Step 1: Loading Vocabs:    0.0634s
  - Step 2: Model Loading:     0.5804s
  - Step 3: Batch Inference:   2.28s
  - Step 4: Metric Report:     0.1619s
==================================================

============================================================
Mode testGS completed in 6.31 seconds
============================================================
