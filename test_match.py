import json

with open("interim_data/token2int.json") as f:
    word_to_ix = json.load(f)

with open("data/pubmed_data/json_data_synthetic_labels_v2/test.json") as f:
    test_data = json.load(f)

unk_count = 0
total_count = 0
for article in test_data:
    for sent in article['sentences']:
        for word in sent:
            total_count += 1
            if word not in word_to_ix:
                unk_count += 1

print(f"TEST.JSON: PyTorch UNKs: {unk_count}/{total_count} ({(unk_count/total_count)*100:.2f}%)")

with open("data/pubmed_data/json_data_synthetic_labels_v2/testgs42.json") as f:
    gs_data = json.load(f)

import spacy
nlp = spacy.blank("en")
nlp.add_pipe('sentencizer')

unk_count2 = 0
total_count2 = 0
for article in gs_data:
    text = article.get('title', '') + ' ' + article.get('abstract', '')
    doc = nlp(text)
    sentences = [[token.orth_.lower() for token in sent if not token.is_punct | token.is_space] for sent in doc.sents]
    for sent in sentences:
        for word in sent:
            total_count2 += 1
            if word not in word_to_ix:
                unk_count2 += 1

print(f"TESTGS42.JSON (lowercased): PyTorch UNKs: {unk_count2}/{total_count2} ({(unk_count2/total_count2)*100:.2f}%)")
