(base) rohangoli@TD-6L0NCJ4:~$ sshfs -o allow_other,uid=1000 rohangoli@169.254.60.39:/Users/rohangoli/Data/NLP_K
PIdentify /home/rohangoli/remote_mount/
The authenticity of host '169.254.60.39 (169.254.60.39)' can't be established.
ED25519 key fingerprint is SHA256:ZvbnzyGMMgT2hr+OUMkp9LZWwxnYhKdPB+EjuLeZmuY.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:1: [hashed name]
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
(rohangoli@169.254.60.39) Password:
(base) rohangoli@TD-6L0NCJ4:~$ ls remote_mount/
Dockerfile   api.py           cdss.yaml  environment.yml  outputs           src            web
README.md    cdss-gpu.yaml    data       interim_data     requirements.txt  test_match.py
__pycache__  cdss-macos.yaml  docs       metamap          scripts           update_gna.py
(base) rohangoli@TD-6L0NCJ4:~$ conda activate cdss-gpu
(cdss-gpu) rohangoli@TD-6L0NCJ4:~$ cd remote_mount/
(cdss-gpu) rohangoli@TD-6L0NCJ4:~/remote_mount$ ls
Dockerfile   api.py           cdss.yaml  environment.yml  outputs           src            web
README.md    cdss-gpu.yaml    data       interim_data     requirements.txt  test_match.py
__pycache__  cdss-macos.yaml  docs       metamap          scripts           update_gna.py
(cdss-gpu) rohangoli@TD-6L0NCJ4:~/remote_mount$ python src/nlp/jobs/gna_pipeline.py --mode all --taggingSchema BIO
============================================================
Running mode: createData
============================================================
Auto-selected device: cuda
Running in createData mode...
Preparing data...
Warning: parse_medline_xml failed for /home/rohangoli/remote_mount/data/pubmed_data/processed_data/processed_full_data.xml (BadGzipFile: Not a gzipped file (b'<?')). Falling back to plain XML parser.
Warning: parse_medline_xml failed for /home/rohangoli/remote_mount/data/pubmed_data/processed_data/processed_44_abstracts_test.xml (BadGzipFile: Not a gzipped file (b'<?')). Falling back to plain XML parser.
Loaded source docs: main=3326 gs=42 misc=12 combined=3380
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/spacy/util.py:910: UserWarning: [W095] Model 'en_pipeline' (0.0.0) was trained with spaCy v3.2.4 and may not be 100% compatible with the current version (3.7.5). If you see errors or degraded performance, download a newer compatible model or retrain your custom model with the current spaCy version. For more details and available updates, run: python -m spacy validate
  warnings.warn(warn_msg)
Synthetic keyword model: /home/rohangoli/remote_mount/outputs/models/cdssSciSpacy/model-best
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/spacy/util.py:910: UserWarning: [W095] Model 'en_pipeline' (0.0.0) was trained with spaCy v3.2.4 and may not be 100% compatible with the current version (3.7.5). If you see errors or degraded performance, download a newer compatible model or retrain your custom model with the current spaCy version. For more details and available updates, run: python -m spacy validate
  warnings.warn(warn_msg)
JSON pre-processing: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 3380/3380 [00:00<00:00, 231445.77it/s]
Synthetic Keywords:   0%|                                                                                                                                                                                | 0/3380 [00:00<?, ?it/s]/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/thinc/shims/pytorch.py:114: FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated. Please use `torch.amp.autocast('cuda', args...)` instead.
  with torch.cuda.amp.autocast(self._mixed_precision):
Synthetic Keywords:   0%|                                                                                                                                                                                | 0/3380 [01:21<?, ?it/s]
Traceback (most recent call last):
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/spacy_legacy/layers/staticvectors_v1.py", line 45, in forward
    vectors_data = model.ops.gemm(model.ops.as_contig(V[rows]), W, trans2=True)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "thinc/backends/numpy_ops.pyx", line 102, in thinc.backends.numpy_ops.NumpyOps.gemm
  File "blis/py.pyx", line 74, in blis.py.gemm
ValueError: Shape mismatch for blis.gemm: (5781, 0), (200, 96)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/rohangoli/remote_mount/src/nlp/jobs/gna_pipeline.py", line 123, in <module>
    run(args)
  File "/home/rohangoli/remote_mount/src/nlp/jobs/gna_pipeline.py", line 85, in run
    experiment.run()
  File "/home/rohangoli/remote_mount/src/nlp/experiments/gna_experiment.py", line 1248, in run
    self.prepare_data()
  File "/home/rohangoli/remote_mount/src/nlp/experiments/gna_experiment.py", line 125, in prepare_data
    builder.generate_synthetic_dataset(
  File "/home/rohangoli/remote_mount/src/nlp/data/dataset.py", line 117, in generate_synthetic_dataset
    for doc in tqdm(nlp.pipe(comb_arr), total=len(comb_arr), desc="Synthetic Keywords"):
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/tqdm/std.py", line 1181, in __iter__
    for obj in iterable:
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/spacy/language.py", line 1618, in pipe
    for doc in docs:
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/spacy/util.py", line 1703, in _pipe
    yield from proc.pipe(docs, **kwargs)
  File "spacy/pipeline/pipe.pyx", line 55, in pipe
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/spacy/util.py", line 1703, in _pipe
    yield from proc.pipe(docs, **kwargs)
  File "spacy/pipeline/transition_parser.pyx", line 255, in pipe
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/spacy/util.py", line 1722, in raise_error
    raise e
  File "spacy/pipeline/transition_parser.pyx", line 251, in spacy.pipeline.transition_parser.Parser.pipe
  File "spacy/pipeline/transition_parser.pyx", line 264, in spacy.pipeline.transition_parser.Parser.predict
  File "spacy/pipeline/transition_parser.pyx", line 285, in spacy.pipeline.transition_parser.Parser.greedy_parse
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/thinc/model.py", line 334, in predict
    return self._func(self, X, is_train=False)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/spacy/ml/tb_framework.py", line 34, in forward
    step_model = ParserStepModel(
                 ^^^^^^^^^^^^^^^^
  File "spacy/ml/parser_model.pyx", line 250, in spacy.ml.parser_model.ParserStepModel.__init__
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/thinc/model.py", line 310, in __call__
    return self._func(self, X, is_train=is_train)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/thinc/layers/chain.py", line 54, in forward
    Y, inc_layer_grad = layer(X, is_train=is_train)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/thinc/model.py", line 310, in __call__
    return self._func(self, X, is_train=is_train)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/thinc/layers/chain.py", line 54, in forward
    Y, inc_layer_grad = layer(X, is_train=is_train)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/thinc/model.py", line 310, in __call__
    return self._func(self, X, is_train=is_train)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/thinc/layers/chain.py", line 54, in forward
    Y, inc_layer_grad = layer(X, is_train=is_train)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/thinc/model.py", line 310, in __call__
    return self._func(self, X, is_train=is_train)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/thinc/layers/concatenate.py", line 57, in forward
    Ys, callbacks = zip(*[layer(X, is_train=is_train) for layer in model.layers])
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/thinc/layers/concatenate.py", line 57, in <listcomp>
    Ys, callbacks = zip(*[layer(X, is_train=is_train) for layer in model.layers])
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/thinc/model.py", line 310, in __call__
    return self._func(self, X, is_train=is_train)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/spacy_legacy/layers/staticvectors_v1.py", line 47, in forward
    raise RuntimeError(Errors.E896)
RuntimeError: [E896] There was an error using the static vectors. Ensure that the vectors of the vocab are properly initialized, or set 'include_static_vectors' to False.
(cdss-gpu) rohangoli@TD-6L0NCJ4:~/remote_mount$ python src/nlp/jobs/gna_pipeline.py --mode preTrain --taggingSchema BIO
============================================================
Running mode: preTrain
============================================================
Auto-selected device: cuda
Running in preTrain mode...
Pre-training language model...
Step 1: Loaded train/test dataset JSON in 0.6738 seconds.
Step 2: Extracted sentences corpus in 0.0048 seconds (Total sents: 34593).
Training Word2Vec model...
Step 3: Trained and saved Word2Vec embeddings in 4.0053 seconds (Vocab size: 27195, CPU workers: 15).
Training Bi-Directional Language Model...
Step 4: Generated input/target sequences in 3.2224 seconds (Train seqs: 435843, Test seqs: 144995).
/home/rohangoli/miniconda3/envs/cdss-gpu/lib/python3.11/site-packages/torch/nn/modules/rnn.py:1013: UserWarning: dropout option adds dropout after all but last recurrent layer, so non-zero dropout expects num_layers greater than 1, but got dropout=0.3 and num_layers=1
  super().__init__("LSTM", *args, **kwargs)
/home/rohangoli/remote_mount/src/nlp/models/trainer.py:87: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
  scaler = torch.cuda.amp.GradScaler(enabled=True)
CUDA device: NVIDIA RTX PRO 2000 Blackwell Generation Laptop GPU
DataLoader workers: 0 | pin_memory: True
Starting Bi-Language Model training on device: cuda...
Epoch: 1/20... Completed in 75.92s | mean_loss : 3.46 | Perplexity : 31.78
Epoch: 2/20... Completed in 77.18s | mean_loss : 1.99 | Perplexity : 7.35
Epoch: 3/20... Completed in 77.15s | mean_loss : 1.67 | Perplexity : 5.32
Epoch: 4/20... Completed in 71.87s | mean_loss : 1.55 | Perplexity : 4.69
Epoch: 5/20... Completed in 71.83s | mean_loss : 1.48 | Perplexity : 4.40
Epoch: 6/20... Completed in 73.27s | mean_loss : 1.43 | Perplexity : 4.18
Epoch: 7/20... Completed in 76.91s | mean_loss : 1.39 | Perplexity : 4.03
Epoch: 8/20... Completed in 76.79s | mean_loss : 1.36 | Perplexity : 3.90
Epoch: 9/20... Completed in 74.63s | mean_loss : 1.34 | Perplexity : 3.82
Epoch: 10/20... Completed in 73.04s | mean_loss : 1.32 | Perplexity : 3.73
Epoch: 11/20... Completed in 75.24s | mean_loss : 1.30 | Perplexity : 3.66
Epoch: 12/20... Completed in 75.68s | mean_loss : 1.28 | Perplexity : 3.59
Epoch: 13/20... Completed in 78.25s | mean_loss : 1.26 | Perplexity : 3.53
Epoch: 14/20... Completed in 80.52s | mean_loss : 1.25 | Perplexity : 3.47
Epoch: 15/20... Completed in 78.46s | mean_loss : 1.23 | Perplexity : 3.43
Epoch: 16/20... Completed in 76.50s | mean_loss : 1.22 | Perplexity : 3.40
Epoch: 17/20... Completed in 76.50s | mean_loss : 1.22 | Perplexity : 3.38
Epoch: 18/20... Completed in 75.96s | mean_loss : 1.22 | Perplexity : 3.39
Epoch: 19/20... Completed in 75.41s | mean_loss : 1.22 | Perplexity : 3.38
Epoch: 20/20... Completed in 75.96s | mean_loss : 1.21 | Perplexity : 3.37
Total BiLM training time: 1517.08s (Avg per epoch: 75.85s)
Test Perplexity: 23.80 (Evaluated in 5.34s)
Step 5: Completed BiLM neural network training in 1527.94 seconds.
Step 6: Saved language model checkpoint to /home/rohangoli/remote_mount/interim_data/BiLM.pt in 1.0878 seconds.

==================================================
PRE-TRAIN MODE SUMMARY (BiLM on device: cuda)
Total Pre-Train Mode Time: 1536.93 seconds
  - Step 1: Loading Data:      0.6738s
  - Step 2: Sentences Corpus:  0.0048s
  - Step 3: Word2Vec Training: 4.0053s
  - Step 4: Sequence Splitting:3.2224s
  - Step 5: BiLM Training:     1527.94s
  - Step 6: Save Checkpoint:   1.0878s
==================================================

============================================================
Mode preTrain completed in 1537.02 seconds
============================================================
(cdss-gpu) rohangoli@TD-6L0NCJ4:~/remote_mount$ python src/nlp/jobs/gna_pipeline.py --mode train,test,testGS --taggingSchema BIO
============================================================
Running mode: train
============================================================
Auto-selected device: cuda
Running in train mode...
Training BiLSTM_CRF...
Step 1: Loaded training data JSON in 0.4164 seconds (train_docs=2461, val_docs=0).
Step 2: Loaded vocabularies in 0.0698 seconds (Size: 27195).
Loading pre-trained Word2Vec embeddings...
Step 3: Loaded pre-trained Word2Vec embeddings in 0.5412 seconds.
Loading pre-trained Bi-Language Model weights...
Step 4: Initialized model & routed to device 'cuda' in 1.5352 seconds (BiLM weights: True).
Label diagnostics [train] | docs=2461 tokens=565485 kp_tokens=147604 kp_ratio=0.2610 kw_nonempty=93069/93071 kw_matched=71661 kw_unmatched=21408 match_ratio=0.7700
Label diagnostics [train] top unmatched keywords: patients, implementation, management, CDSS, monitoring
Label diagnostics [train] unmatched reasons: overlap_conflict=21402, no_span_match=6
Step 5a: Prepared 405 train and 0 val CPU batches in 36.05s (cached for all epochs).
Epoch  1/20 | Train Loss: 8.4377 | Val Loss: n/a | Time: 36.29s | Checkpoint Saved
Epoch  2/20 | Train Loss: 4.9125 | Val Loss: n/a | Time: 33.29s | Checkpoint Saved
Epoch  3/20 | Train Loss: 3.8987 | Val Loss: n/a | Time: 34.09s | Checkpoint Saved
Epoch  4/20 | Train Loss: 3.3632 | Val Loss: n/a | Time: 35.06s | Checkpoint Saved
Epoch  5/20 | Train Loss: 2.9825 | Val Loss: n/a | Time: 31.66s | Checkpoint Saved
Epoch  6/20 | Train Loss: 2.6560 | Val Loss: n/a | Time: 31.64s | Checkpoint Saved
Epoch  7/20 | Train Loss: 2.3635 | Val Loss: n/a | Time: 34.08s | Checkpoint Saved
Epoch  8/20 | Train Loss: 2.0830 | Val Loss: n/a | Time: 34.99s | Checkpoint Saved
Epoch  9/20 | Train Loss: 1.8181 | Val Loss: n/a | Time: 36.63s | Checkpoint Saved
Epoch 10/20 | Train Loss: 1.5652 | Val Loss: n/a | Time: 33.69s | Checkpoint Saved
Epoch 11/20 | Train Loss: 1.3320 | Val Loss: n/a | Time: 34.40s | Checkpoint Saved
Epoch 12/20 | Train Loss: 1.1266 | Val Loss: n/a | Time: 33.99s | Checkpoint Saved
Epoch 13/20 | Train Loss: 0.9502 | Val Loss: n/a | Time: 30.88s | Checkpoint Saved
Epoch 14/20 | Train Loss: 0.7936 | Val Loss: n/a | Time: 36.30s | Checkpoint Saved
Epoch 15/20 | Train Loss: 0.6715 | Val Loss: n/a | Time: 33.61s | Checkpoint Saved
Epoch 16/20 | Train Loss: 0.5883 | Val Loss: n/a | Time: 32.02s | Checkpoint Saved
Epoch 17/20 | Train Loss: 0.4885 | Val Loss: n/a | Time: 32.06s | Checkpoint Saved
Epoch 18/20 | Train Loss: 0.4383 | Val Loss: n/a | Time: 33.42s | Checkpoint Saved
Epoch 19/20 | Train Loss: 0.3758 | Val Loss: n/a | Time: 33.12s | Checkpoint Saved
Epoch 20/20 | Train Loss: 0.3449 | Val Loss: n/a | Time: 28.36s | Checkpoint Saved
Step 5: Completed 20 training epochs in 737.48 seconds (Avg per epoch: 33.48s; prep: 36.05s).

==================================================
TRAIN MODE SUMMARY (BILSTM_CRF on device: cuda)
Total Train Mode Time: 740.05 seconds
  - Step 1: Loading Data:      0.4164s
  - Step 2: Loading Vocab:     0.0698s
  - Step 3: Embeddings Load:   0.5412s
  - Step 4: Model & Device:    1.5352s
  - Step 5: Epochs Train Loop: 737.48s (Avg: 33.48s/epoch)
==================================================

============================================================
Mode train completed in 740.11 seconds
============================================================
============================================================
Running mode: test
============================================================
Auto-selected device: cuda
Running in test mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0375 seconds.
Loaded model weights from /home/rohangoli/remote_mount/interim_data/BiLSTM-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.6981 seconds.

Evaluating on Test dataset: test.json
Label diagnostics [test] | docs=820 tokens=187970 kp_tokens=49600 kp_ratio=0.2639 kw_nonempty=31441/31441 kw_matched=24017 kw_unmatched=7424 match_ratio=0.7639
Label diagnostics [test] top unmatched keywords: patients, implementation, monitoring, management, CDSS
Label diagnostics [test] unmatched reasons: overlap_conflict=7423, no_span_match=1
Step 3: Inference prediction loop completed in 19.42 seconds.
Metrics on Test DS:
Label counts (target): {'B-KP': 37737, 'I-KP': 11851, 'O': 138314}
Label counts (pred):   {'B-KP': 39248, 'I-KP': 11480, 'O': 137174}
Confusion Matrix:
[[ 30303    619   6815]
 [   766   8506   2579]
 [  8179   2355 127780]]
Row sums (target support by label order): [37737, 11851, 138314]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       | 30303.0 |  7434.0 |  8945.0 | 141220.0 |   0.9128 |   0.0872 |   0.7721 |   0.8030 |   0.9404 |   0.7872
I-KP       |  8506.0 |  3345.0 |  2974.0 | 173077.0 |   0.9664 |   0.0336 |   0.7409 |   0.7177 |   0.9831 |   0.7292
O          | 127780.0 | 10534.0 |  9394.0 |  40194.0 |   0.8939 |   0.1061 |   0.9315 |   0.9238 |   0.8106 |   0.9277
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.9244 |   0.0756 |   0.8148 |   0.8149 |   0.9114 |   0.8147
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.73      0.76      0.75     37737

   micro avg       0.73      0.76      0.75     37737
   macro avg       0.73      0.76      0.75     37737
weighted avg       0.73      0.76      0.75     37737

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    73.28% |    76.22% |    74.72% |    88.66%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 2.9247 seconds.

==================================================
EVALUATION SUMMARY ON TEST (BILSTM_CRF on device: cuda)
Total Dataset Eval Time: 29.86 seconds
  - Step 1: Loading Vocabs:    0.0375s
  - Step 2: Model Loading:     0.6981s
  - Step 3: Batch Inference:   19.42s
  - Step 4: Metric Report:     2.9247s
==================================================

============================================================
Mode test completed in 29.89 seconds
============================================================
============================================================
Running mode: testGS
============================================================
Auto-selected device: cuda
Running in testGS mode...
Evaluating BiLSTM_CRF...
Step 1: Loaded vocabulary mappings in 0.0584 seconds.
Loaded model weights from /home/rohangoli/remote_mount/interim_data/BiLSTM-CRF_BIO.pt
Step 2: Initialized model & loaded weights on 'cuda' in 0.7053 seconds.

Evaluating on Gold Standard 42 dataset: testgs42.json
Label diagnostics [gold_standard_42] | docs=42 tokens=11567 kp_tokens=1939 kp_ratio=0.1676 kw_nonempty=1087/1087 kw_matched=945 kw_unmatched=142 match_ratio=0.8694
Label diagnostics [gold_standard_42] top unmatched keywords: rule-based , rule-based, semantic interoperability , implementation, decision-making
Label diagnostics [gold_standard_42] unmatched reasons: no_span_match=92, overlap_conflict=50
Step 3: Inference prediction loop completed in 1.15 seconds.
Metrics on Gold Standard 42 DS:
Label counts (target): {'B-KP': 1022, 'I-KP': 435, 'O': 7469}
Label counts (pred):   {'B-KP': 1465, 'I-KP': 504, 'O': 6957}
Confusion Matrix:
[[ 611   37  374]
 [  47  193  195]
 [ 807  274 6388]]
Row sums (target support by label order): [1022, 435, 7469]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |   611.0 |   411.0 |   854.0 |   7050.0 |   0.8583 |   0.1417 |   0.4171 |   0.5978 |   0.8920 |   0.4914
I-KP       |   193.0 |   242.0 |   311.0 |   8180.0 |   0.9380 |   0.0620 |   0.3829 |   0.4437 |   0.9634 |   0.4111
O          |  6388.0 |  1081.0 |   569.0 |    888.0 |   0.8151 |   0.1849 |   0.9182 |   0.8553 |   0.6095 |   0.8856
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8705 |   0.1295 |   0.5727 |   0.6323 |   0.8216 |   0.5960
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.36      0.51      0.42      1022

   micro avg       0.36      0.51      0.42      1022
   macro avg       0.36      0.51      0.42      1022
weighted avg       0.36      0.51      0.42      1022

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    35.90% |    51.47% |    42.30% |    80.57%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.0946 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 42 (BILSTM_CRF on device: cuda)
Total Dataset Eval Time: 2.91 seconds
  - Step 1: Loading Vocabs:    0.0584s
  - Step 2: Model Loading:     0.7053s
  - Step 3: Batch Inference:   1.15s
  - Step 4: Metric Report:     0.0946s
==================================================


Evaluating on Gold Standard 91 dataset: testgs91.json
Label diagnostics [gold_standard_91] | docs=91 tokens=22799 kp_tokens=4086 kp_ratio=0.1792 kw_nonempty=2364/2364 kw_matched=2091 kw_unmatched=273 match_ratio=0.8845
Label diagnostics [gold_standard_91] top unmatched keywords: guideline-based, follow-up, real-time, rule-based, ontology-based
Label diagnostics [gold_standard_91] unmatched reasons: no_span_match=191, overlap_conflict=82
Step 3: Inference prediction loop completed in 2.24 seconds.
Metrics on Gold Standard 91 DS:
Label counts (target): {'B-KP': 2322, 'I-KP': 797, 'O': 14118}
Label counts (pred):   {'B-KP': 2562, 'I-KP': 877, 'O': 13798}
Confusion Matrix:
[[ 1470    95   757]
 [   70   395   332]
 [ 1022   387 12709]]
Row sums (target support by label order): [2322, 797, 14118]
Note: Rows represent Actual/True labels, Columns represent Predicted labels.
Label order: ['B-KP', 'I-KP', 'O']
-------------------------------------------------------------------------------------------------------------------
Label      |      TP |      FN |      FP |       TN | Accuracy | Misclass |    Prec. |   Recall |    Spec. |       F1
-------------------------------------------------------------------------------------------------------------------
B-KP       |  1470.0 |   852.0 |  1092.0 |  13823.0 |   0.8872 |   0.1128 |   0.5738 |   0.6331 |   0.9268 |   0.6020
I-KP       |   395.0 |   402.0 |   482.0 |  15958.0 |   0.9487 |   0.0513 |   0.4504 |   0.4956 |   0.9707 |   0.4719
O          | 12709.0 |  1409.0 |  1089.0 |   2030.0 |   0.8551 |   0.1449 |   0.9211 |   0.9002 |   0.6508 |   0.9105
-------------------------------------------------------------------------------------------------------------------
Average    |       - |       - |       - |        - |   0.8970 |   0.1030 |   0.6484 |   0.6763 |   0.8494 |   0.6615
-------------------------------------------------------------------------------------------------------------------
SeqEval Metrics:
              precision    recall  f1-score   support

          KP       0.52      0.57      0.54      2322

   micro avg       0.52      0.57      0.54      2322
   macro avg       0.52      0.57      0.54      2322
weighted avg       0.52      0.57      0.54      2322

-----------------------------------------------------------------
SeqEval Overall   | Precision |    Recall |  F1-Score |  Accuracy
-----------------------------------------------------------------
Score (%)         |    51.60% |    56.93% |    54.14% |    84.55%
-----------------------------------------------------------------
Step 4: Metric calculations & reports completed in 0.1524 seconds.

==================================================
EVALUATION SUMMARY ON GOLD STANDARD 91 (BILSTM_CRF on device: cuda)
Total Dataset Eval Time: 6.27 seconds
  - Step 1: Loading Vocabs:    0.0584s
  - Step 2: Model Loading:     0.7053s
  - Step 3: Batch Inference:   2.24s
  - Step 4: Metric Report:     0.1524s
==================================================

============================================================
Mode testGS completed in 6.28 seconds
============================================================
(cdss-gpu) rohangoli@TD-6L0NCJ4:~/remote_mount$