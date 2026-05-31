# R4 HAN-CRF (freeze embeddings + validation/early-stop, fixed-batch+block-diagonal defaults)
Run started: 2026-05-29T17:20:38-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,test,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --validationSplit 0.1 --earlyStopPatience 3 --hanUseBlockDiagonal --hanBatchMode fixed --hanFreezeEmbeddings
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
Step 1: Loaded training data JSON in 0.4211 seconds (train_docs=2215, val_docs=246).
Step 2: Loaded vocabularies in 0.0662 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.6135 seconds.
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.6683 seconds (BiLM weights: True).
Label diagnostics [train] | docs=2215 tokens=511382 kp_tokens=133876 kp_ratio=0.2618 kw_nonempty=84211/84213 kw_matched=64782 kw_unmatched=19429 match_ratio=0.7693
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, treatment
Label diagnostics [train] unmatched reasons: overlap_conflict=19423, no_span_match=6
Label diagnostics [val] | docs=246 tokens=54103 kp_tokens=13728 kp_ratio=0.2537 kw_nonempty=8858/8858 kw_matched=6879 kw_unmatched=1979 match_ratio=0.7766
Label diagnostics [val] top unmatched keywords: patients, CDSS, alerts, CDS, implementation
Label diagnostics [val] unmatched reasons: overlap_conflict=1979
Step 5a: Prepared 367 train and 39 val CPU batches in 38.64s (cached for all epochs).
Epoch  1/20 | Train Loss: 10.9583 | Val Loss: 6.6646 | Time: 31.84s | Checkpoint Saved
Epoch  2/20 | Train Loss: 5.7175 | Val Loss: 5.7280 | Time: 32.43s | Checkpoint Saved
Epoch  3/20 | Train Loss: 4.4421 | Val Loss: 5.2809 | Time: 33.61s | Checkpoint Saved
Epoch  4/20 | Train Loss: 3.7440 | Val Loss: 5.1058 | Time: 33.38s | Checkpoint Saved
Epoch  5/20 | Train Loss: 3.2852 | Val Loss: 5.2022 | Time: 34.48s | No Save
Epoch  6/20 | Train Loss: 2.9365 | Val Loss: 5.2528 | Time: 34.04s | No Save
Epoch  7/20 | Train Loss: 2.6475 | Val Loss: 5.1661 | Time: 32.74s | No Save
Early stopping at epoch 7 after 3 non-improving validation epochs (best epoch=4, best val loss=5.1058).
Best checkpoint selected from epoch 4 with val loss 5.1058.
Step 5: Completed 7 training epochs in 294.96 seconds (Avg per epoch: 33.22s; prep: 38.64s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 297.73 seconds
  - Step 1: Loading Data:      0.4211s
  - Step 2: Loading Vocab:     0.0662s
  - Step 3: Embeddings Load:   0.6135s
  - Step 4: Model & Device:    1.6683s
  - Step 5: Epochs Train Loop: 294.96s (Avg: 33.22s/epoch)
==================================================

============================================================
Mode train completed in 297.82 seconds
============================================================
============================================================
Running mode: test
============================================================
Auto-selected device: cuda
Running in test mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0624 seconds.
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5124 seconds.

Evaluating on Test dataset: test.json
Label diagnostics [test] | docs=820 tokens=187970 kp_tokens=49600 kp_ratio=0.2639 kw_nonempty=31441/31441 kw_matched=24017 kw_unmatched=7424 match_ratio=0.7639
Label diagnostics [test] top unmatched keywords: patients, implementation, monitoring, management, CDSS
Label diagnostics [test] unmatched reasons: overlap_conflict=7423, no_span_match=1
Step 3: Inference prediction loop completed in 19.73 seconds.
Metrics on Test DS:
Label counts (target): {'B-KP': 37737, 'I-KP': 11851, 'O': 138314}
Label counts (pred):   {'B-KP': 35598, 'I-KP': 11460, 'O': 140844}
Confusion Matrix:
[[ 29322    688   7727]
 [   623   8671   2557]
 [  5653   2101 130560]]
Row sums (target support by label order): [37737, 11851, 138314]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       | 29322.0 |  8415.0 |  6276.0 | 143889.0 |   0.9218 |   0.0782 |   0.8237 |   0.7770 |   0.9582 |   0.7997
I-KP       |  8671.0 |  3180.0 |  2789.0 | 173262.0 |   0.9682 |   0.0318 |   0.7566 |   0.7317 |   0.9842 |   0.7439
O          | 130560.0 |  7754.0 | 10284.0 |  39304.0 |   0.9040 |   0.0960 |   0.9270 |   0.9439 |   0.7926 |   0.9354
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9314 |   0.0686 |   0.8358 |   0.8175 |   0.9117 |   0.8263
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.78      0.74      0.76     37737

   micro avg       0.78      0.74      0.76     37737
   macro avg       0.78      0.74      0.76     37737
weighted avg       0.78      0.74      0.76     37737

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    78.15% |    73.72% |    75.87% |    89.70%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 2.5260 seconds.

==================================================
EVALUATION SUMMARY ON TEST (HAN_CRF on device: cuda)
Total Dataset Eval Time: 29.40 seconds
  - Step 1: Loading Vocabs:    0.0624s
  - Step 2: Model Loading:     0.5124s
  - Step 3: Batch Inference:   19.73s
  - Step 4: Metric Report:     2.5260s
==================================================

============================================================
Mode test completed in 29.43 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0515 seconds.
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5992 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.08 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1321, 'I-KP': 454, 'O': 7151}
Confusion Matrix:
[[ 590   38  394]
 [  44  196  195]
 [ 687  220 6562]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   590.0 |   432.0 |   731.0 |   7173.0 |   0.8697 |   0.1303 |   0.4466 |   0.5773 |   0.9075 |   0.5036
I-KP       |   196.0 |   239.0 |   258.0 |   8233.0 |   0.9443 |   0.0557 |   0.4317 |   0.4506 |   0.9696 |   0.4409
O          |  6562.0 |   907.0 |   589.0 |    868.0 |   0.8324 |   0.1676 |   0.9176 |   0.8786 |   0.5957 |   0.8977
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8821 |   0.1179 |   0.5987 |   0.6355 |   0.8243 |   0.6141
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.39      0.50      0.44      1022

   micro avg       0.39      0.50      0.44      1022
   macro avg       0.39      0.50      0.44      1022
weighted avg       0.39      0.50      0.44      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    38.83% |    50.20% |    43.79% |    82.32%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0853 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 2.61 seconds
  - Step 1: Loading Vocabs:    0.0515s
  - Step 2: Model Loading:     0.5992s
  - Step 3: Batch Inference:   1.08s
  - Step 4: Metric Report:     0.0853s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.24 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2324, 'I-KP': 781, 'O': 14132}
Confusion Matrix:
[[ 1375    91   856]
 [   75   357   365]
 [  874   333 12911]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1375.0 |   947.0 |   949.0 |  13966.0 |   0.8900 |   0.1100 |   0.5917 |   0.5922 |   0.9364 |   0.5919
I-KP       |   357.0 |   440.0 |   424.0 |  16016.0 |   0.9499 |   0.0501 |   0.4571 |   0.4479 |   0.9742 |   0.4525
O          | 12911.0 |  1207.0 |  1221.0 |   1898.0 |   0.8591 |   0.1409 |   0.9136 |   0.9145 |   0.6085 |   0.9141
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8997 |   0.1003 |   0.6541 |   0.6515 |   0.8397 |   0.6528
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
Score (%)         |    53.27% |    53.32% |    53.29% |    84.95%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1510 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 5.99 seconds
  - Step 1: Loading Vocabs:    0.0515s
  - Step 2: Model Loading:     0.5992s
  - Step 3: Batch Inference:   2.24s
  - Step 4: Metric Report:     0.1510s
==================================================

============================================================
Mode testGS completed in 6.01 seconds
============================================================
