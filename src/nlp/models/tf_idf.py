# -*- coding: utf-8 -*-
import math
from tqdm import tqdm
from collections import Counter

# Calculate IDF
def cal_idf(datas):
    total_files = len(datas)
    # Single-pass document-frequency count: O(total tokens) instead of O(vocab x docs).
    # Produces document frequencies (and therefore IDF values) identical to the previous
    # nested-loop implementation, but scales to corpora with hundreds of thousands of docs.
    document_frequency = Counter()
    for words in datas:
        for word in set(words):
            document_frequency[word] += 1.0
    idf = {}
    for word, freq in document_frequency.items():
        idf[word] = math.log((total_files + 1) / (freq + 1), 2)
    return idf

# Calculate TF-IDF
def tf_idf(datas):
    idf = cal_idf(datas)
    return_datas = []
    temp_len_datas = len(datas)
    with tqdm(enumerate(datas), total=temp_len_datas) as pbar:
        for index,words in pbar:
            # words = datas[index]
            num_words = len(words)
            tf = Counter(words)
            keywords = {}
            for k, v in tf.items():
                keywords[k] = (v / num_words) * idf[k]
            return_datas.append(keywords)
            pbar.set_description("The %s document calculation TF-IDF completed"%(index + 1))
    return return_datas
