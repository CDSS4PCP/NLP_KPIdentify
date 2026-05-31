# R8 HAN-CRF (k=5 pooled train+test for CV, fold=4, freeze embeddings, fixed+block defaults, final eval GS only)
Run started: 2026-05-29T18:55:23-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --earlyStopPatience 3 --hanUseBlockDiagonal --hanBatchMode fixed --hanFreezeEmbeddings --kFolds 5 --kFoldIndex 4 --kFoldSeed 42 --cvPoolTrainAndTest
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
CV pooling enabled: using train.json + test.json (train_docs=2461, test_docs=820, pooled_docs=3281).
Using k-fold split: k=5, fold=4, seed=42 (train_docs=2625, val_docs=656).
Step 1: Loaded training data JSON in 0.5426 seconds (train_docs=2625, val_docs=656).
Step 2: Loaded vocabularies in 0.0528 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.6760 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.6339 seconds (BiLM weights: True).
Label diagnostics [train] | docs=2625 tokens=603204 kp_tokens=158030 kp_ratio=0.2620 kw_nonempty=99671/99673 kw_matched=76657 kw_unmatched=23014 match_ratio=0.7691
Label diagnostics [train] top unmatched keywords: patients, implementation, CDSS, management, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=23010, no_span_match=4
Label diagnostics [val] | docs=656 tokens=150251 kp_tokens=39174 kp_ratio=0.2607 kw_nonempty=24839/24839 kw_matched=19021 kw_unmatched=5818 match_ratio=0.7658
Label diagnostics [val] top unmatched keywords: patients, management, implementation, CDSS, monitoring
Label diagnostics [val] unmatched reasons: overlap_conflict=5815, no_span_match=3
Step 5a: Prepared 432 train and 108 val CPU batches in 50.97s (cached for all epochs).
Epoch  1/20 | Train Loss: 7.6865 | Val Loss: 5.4275 | Time: 53.71s | Checkpoint Saved
Epoch  2/20 | Train Loss: 4.6550 | Val Loss: 4.7050 | Time: 46.86s | Checkpoint Saved
Epoch  3/20 | Train Loss: 3.8010 | Val Loss: 4.8341 | Time: 42.92s | No Save
Epoch  4/20 | Train Loss: 3.3122 | Val Loss: 4.6064 | Time: 45.05s | Checkpoint Saved
Epoch  5/20 | Train Loss: 2.9887 | Val Loss: 4.7268 | Time: 47.53s | No Save
Epoch  6/20 | Train Loss: 2.7002 | Val Loss: 4.7971 | Time: 44.50s | No Save
Epoch  7/20 | Train Loss: 2.4556 | Val Loss: 5.0104 | Time: 44.18s | No Save
Early stopping at epoch 7 after 3 non-improving validation epochs (best epoch=4, best val loss=4.6064).
Best checkpoint selected from epoch 4 with val loss 4.6064.
Step 5: Completed 7 training epochs in 404.54 seconds (Avg per epoch: 46.39s; prep: 50.97s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 407.44 seconds
  - Step 1: Loading Data:      0.5426s
  - Step 2: Loading Vocab:     0.0528s
  - Step 3: Embeddings Load:   0.6760s
  - Step 4: Model & Device:    1.6339s
  - Step 5: Epochs Train Loop: 404.54s (Avg: 46.39s/epoch)
==================================================

============================================================
Mode train completed in 407.56 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0698 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5400 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.20 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1373, 'I-KP': 539, 'O': 7014}
Confusion Matrix:
[[ 597   46  379]
 [  50  220  165]
 [ 726  273 6470]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   597.0 |   425.0 |   776.0 |   7128.0 |   0.8654 |   0.1346 |   0.4348 |   0.5841 |   0.9018 |   0.4985
I-KP       |   220.0 |   215.0 |   319.0 |   8172.0 |   0.9402 |   0.0598 |   0.4082 |   0.5057 |   0.9624 |   0.4517
O          |  6470.0 |   999.0 |   544.0 |    913.0 |   0.8271 |   0.1729 |   0.9224 |   0.8662 |   0.6266 |   0.8935
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8776 |   0.1224 |   0.5885 |   0.6520 |   0.8303 |   0.6146
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.38      0.50      0.43      1022

   micro avg       0.38      0.50      0.43      1022
   macro avg       0.38      0.50      0.43      1022
weighted avg       0.38      0.50      0.43      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    37.58% |    50.49% |    43.09% |    81.64%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0750 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 2.73 seconds
  - Step 1: Loading Vocabs:    0.0698s
  - Step 2: Model Loading:     0.5400s
  - Step 3: Batch Inference:   1.20s
  - Step 4: Metric Report:     0.0750s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.28 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2460, 'I-KP': 936, 'O': 13841}
Confusion Matrix:
[[ 1413   114   795]
 [   76   405   316]
 [  971   417 12730]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1413.0 |   909.0 |  1047.0 |  13868.0 |   0.8865 |   0.1135 |   0.5744 |   0.6085 |   0.9298 |   0.5910
I-KP       |   405.0 |   392.0 |   531.0 |  15909.0 |   0.9465 |   0.0535 |   0.4327 |   0.5082 |   0.9677 |   0.4674
O          | 12730.0 |  1388.0 |  1111.0 |   2008.0 |   0.8550 |   0.1450 |   0.9197 |   0.9017 |   0.6438 |   0.9106
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8960 |   0.1040 |   0.6423 |   0.6728 |   0.8471 |   0.6563
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.52      0.55      0.53      2322

   micro avg       0.52      0.55      0.53      2322
   macro avg       0.52      0.55      0.53      2322
weighted avg       0.52      0.55      0.53      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    51.87% |    54.95% |    53.37% |    84.40%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.5581 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 6.51 seconds
  - Step 1: Loading Vocabs:    0.0698s
  - Step 2: Model Loading:     0.5400s
  - Step 3: Batch Inference:   2.28s
  - Step 4: Metric Report:     0.5581s
==================================================

============================================================
Mode testGS completed in 6.52 seconds
============================================================
