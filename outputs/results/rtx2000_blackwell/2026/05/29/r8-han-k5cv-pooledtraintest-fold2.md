# R8 HAN-CRF (k=5 pooled train+test for CV, fold=2, freeze embeddings, fixed+block defaults, final eval GS only)
Run started: 2026-05-29T18:39:59-05:00
Command: python src/nlp/jobs/gna_pipeline.py --model han_crf --mode train,testGS --taggingSchema BIO --epochs 20 --batchSize 64 --earlyStopPatience 3 --hanUseBlockDiagonal --hanBatchMode fixed --hanFreezeEmbeddings --kFolds 5 --kFoldIndex 2 --kFoldSeed 42 --cvPoolTrainAndTest
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
CV pooling enabled: using train.json + test.json (train_docs=2461, test_docs=820, pooled_docs=3281).
Using k-fold split: k=5, fold=2, seed=42 (train_docs=2625, val_docs=656).
Step 1: Loaded training data JSON in 0.4751 seconds (train_docs=2625, val_docs=656).
Step 2: Loaded vocabularies in 0.0494 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.6866 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.5270 seconds (BiLM weights: True).
Label diagnostics [train] | docs=2625 tokens=608125 kp_tokens=159336 kp_ratio=0.2620 kw_nonempty=100624/100625 kw_matched=77099 kw_unmatched=23525 match_ratio=0.7662
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=23520, no_span_match=5
Label diagnostics [val] | docs=656 tokens=145330 kp_tokens=37868 kp_ratio=0.2606 kw_nonempty=23886/23887 kw_matched=18579 kw_unmatched=5307 match_ratio=0.7778
Label diagnostics [val] top unmatched keywords: patients, treatment, CDSS, implementation, monitoring
Label diagnostics [val] unmatched reasons: overlap_conflict=5305, no_span_match=2
Step 5a: Prepared 435 train and 105 val CPU batches in 51.23s (cached for all epochs).
Epoch  1/20 | Train Loss: 9.2521 | Val Loss: 6.3303 | Time: 52.68s | Checkpoint Saved
Epoch  2/20 | Train Loss: 5.3412 | Val Loss: 5.4038 | Time: 49.43s | Checkpoint Saved
Epoch  3/20 | Train Loss: 4.1884 | Val Loss: 4.9222 | Time: 42.49s | Checkpoint Saved
Epoch  4/20 | Train Loss: 3.5693 | Val Loss: 4.9447 | Time: 45.30s | No Save
Epoch  5/20 | Train Loss: 3.1653 | Val Loss: 4.8235 | Time: 46.69s | Checkpoint Saved
Epoch  6/20 | Train Loss: 2.8357 | Val Loss: 4.8428 | Time: 45.54s | No Save
Epoch  7/20 | Train Loss: 2.5615 | Val Loss: 5.1627 | Time: 43.25s | No Save
Epoch  8/20 | Train Loss: 2.3021 | Val Loss: 5.3936 | Time: 44.98s | No Save
Early stopping at epoch 8 after 3 non-improving validation epochs (best epoch=5, best val loss=4.8235).
Best checkpoint selected from epoch 5 with val loss 4.8235.
Step 5: Completed 8 training epochs in 451.86 seconds (Avg per epoch: 46.30s; prep: 51.23s).

==================================================
TRAIN MODE SUMMARY (HAN_CRF on device: cuda)
Total Train Mode Time: 454.60 seconds
  - Step 1: Loading Data:      0.4751s
  - Step 2: Loading Vocab:     0.0494s
  - Step 3: Embeddings Load:   0.6866s
  - Step 4: Model & Device:    1.5270s
  - Step 5: Epochs Train Loop: 451.86s (Avg: 46.30s/epoch)
==================================================

============================================================
Mode train completed in 454.73 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0614 seconds.
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.2 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
Loaded model weights from /home/rohangoli/remote_mount/interim_data/HAN-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.5100 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making 
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.15 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1418, 'I-KP': 471, 'O': 7037}
Confusion Matrix:
[[ 590   39  393]
 [  51  205  179]
 [ 777  227 6465]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   590.0 |   432.0 |   828.0 |   7076.0 |   0.8588 |   0.1412 |   0.4161 |   0.5773 |   0.8952 |   0.4836
I-KP       |   205.0 |   230.0 |   266.0 |   8225.0 |   0.9444 |   0.0556 |   0.4352 |   0.4713 |   0.9687 |   0.4525
O          |  6465.0 |  1004.0 |   572.0 |    885.0 |   0.8234 |   0.1766 |   0.9187 |   0.8656 |   0.6074 |   0.8914
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8756 |   0.1244 |   0.5900 |   0.6380 |   0.8238 |   0.6092
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
Score (%)         |    36.18% |    50.20% |    42.05% |    81.34%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0795 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 2.58 seconds
  - Step 1: Loading Vocabs:    0.0614s
  - Step 2: Model Loading:     0.5100s
  - Step 3: Batch Inference:   1.15s
  - Step 4: Metric Report:     0.0795s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 1.98 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2590, 'I-KP': 825, 'O': 13822}
Confusion Matrix:
[[ 1447   105   770]
 [   80   377   340]
 [ 1063   343 12712]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1447.0 |   875.0 |  1143.0 |  13772.0 |   0.8829 |   0.1171 |   0.5587 |   0.6232 |   0.9234 |   0.5892
I-KP       |   377.0 |   420.0 |   448.0 |  15992.0 |   0.9496 |   0.0504 |   0.4570 |   0.4730 |   0.9727 |   0.4649
O          | 12712.0 |  1406.0 |  1110.0 |   2009.0 |   0.8540 |   0.1460 |   0.9197 |   0.9004 |   0.6441 |   0.9099
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8955 |   0.1045 |   0.6451 |   0.6655 |   0.8467 |   0.6547
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.51      0.57      0.53      2322

   micro avg       0.51      0.57      0.53      2322
   macro avg       0.51      0.57      0.53      2322
weighted avg       0.51      0.57      0.53      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    50.69% |    56.55% |    53.46% |    84.33%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.4820 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (HAN_CRF on device: cuda)
Total Dataset Eval Time: 5.93 seconds
  - Step 1: Loading Vocabs:    0.0614s
  - Step 2: Model Loading:     0.5100s
  - Step 3: Batch Inference:   1.98s
  - Step 4: Metric Report:     0.4820s
==================================================

============================================================
Mode testGS completed in 5.94 seconds
============================================================
