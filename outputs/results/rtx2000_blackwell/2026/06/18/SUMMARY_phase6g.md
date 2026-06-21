config                                TEST    GS42    GS91
------------------------------------------------------------
bilstm_crf_BILOU                    63.93  40.76  53.15
bilstm_crf_BIO                      63.08  40.09  51.43
bilstm_crf_IOBES                    64.94  41.86  53.40
han_sentence_only_BILOU             65.58  41.10  52.48
han_sentence_only_BIO               65.56  41.39  52.78
han_sentence_only_IOBES             66.21  40.33  52.87
han_token_doc_attn_BILOU            64.64  40.73  51.97
han_token_doc_attn_BIO              66.00  41.43  52.14
han_token_doc_attn_IOBES            64.95  40.80  51.87
han_token_doc_attn_gated_BILOU      64.67  40.60  52.38
han_token_doc_attn_gated_BIO        64.40  40.09  51.82
han_token_doc_attn_gated_IOBES      64.62  40.51  52.53
transformer_biobert                 52.47  45.12  46.87
transformer_pubmedbert              52.59  46.12  45.40
transformer_scibert                 55.71  45.34  47.96

Best on TEST: han_sentence_only_IOBES = 66.21
Best on GS42: transformer_pubmedbert = 46.12
Best on GS91: bilstm_crf_IOBES = 53.40