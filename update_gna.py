import sys

with open("src/nlp/experiments/gna_experiment.py", "r") as f:
    content = f.read()

# Update train
new_train = content.replace(
"""            for inputs, targets, masks in self._get_batches(trainData, word_to_ix, tag_to_ix, batch_size, schema=schema):
                inputs, targets, masks = inputs.to(self.device), targets.to(self.device), masks.to(self.device)""",
"""            tf_idf_dict = read_json_array(os.path.join(WORKING_PATH, config.JSON_DATA, "tf_idf.json")) if os.path.exists(os.path.join(WORKING_PATH, config.JSON_DATA, "tf_idf.json")) else {}
            textrank_dict = read_json_array(os.path.join(WORKING_PATH, config.JSON_DATA, "textrank.json")) if os.path.exists(os.path.join(WORKING_PATH, config.JSON_DATA, "textrank.json")) else {}
            for inputs, targets, masks, feats_pos, feats_cont in self._get_batches(trainData, word_to_ix, tag_to_ix, tf_idf_dict, textrank_dict, batch_size, schema=schema):
                inputs, targets, masks = inputs.to(self.device), targets.to(self.device), masks.to(self.device)
                feats_pos, feats_cont = feats_pos.to(self.device), feats_cont.to(self.device)"""
)

# Update _get_batches def
new_train = new_train.replace(
"""    def _get_batches(self, data, word_to_ix, tag_to_ix, batch_size=64, max_len=128, schema="IOBES"):
        from src.nlp.models.preProcessData import mark_keyword_all_sentences""",
"""    def _get_batches(self, data, word_to_ix, tag_to_ix, tf_idf_dict=None, textrank_dict=None, batch_size=64, max_len=128, schema="IOBES"):
        from src.nlp.models.preProcessData import mark_keyword_all_sentences
        import nltk
        import re
        PENN_POS_TAGS = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB']
        POS_TO_IX = {tag: i+1 for i, tag in enumerate(PENN_POS_TAGS)}
"""
)

# Replace the inner loop of _get_batches
old_inner = """            _, labels, sentences = mark_keyword_all_sentences(article['keywords'], article['sentences'], schema=schema)
            sent_count = 0
            for x, y in zip(sentences, labels):
                if len(x) > 3:
                    prcd_data.append((x, y))
                    sent_count += 1"""
                    
new_inner = """            _, labels, sentences = mark_keyword_all_sentences(article['keywords'], article['sentences'], schema=schema)
            
            plain_text = ' '.join([' '.join(sent) for sent in sentences]).lower().strip()
            wfof_dict = {}
            for word in set(plain_text.split()):
                if len(word) < 2: continue
                item = re.search(re.escape(word), plain_text)
                if item is not None:
                    wfof_dict[word] = item.start() / max(1, len(plain_text))
                    
            article_ti = tf_idf_dict.get(article.get('id', ''), {}) if tf_idf_dict else {}
            article_tr = textrank_dict.get(article.get('id', ''), {}) if textrank_dict else {}
            
            sent_count = 0
            for x, y in zip(sentences, labels):
                if len(x) > 3:
                    pos_tags = [POS_TO_IX.get(p, 0) for w, p in nltk.pos_tag(x)]
                    lens = [len(w) for w in x]
                    wfofs = [wfof_dict.get(w.lower(), 0.0) for w in x]
                    tis = [article_ti.get(w.lower(), 0.0) for w in x]
                    trs = [article_tr.get(w.lower(), 0.0) for w in x]
                    prcd_data.append((x, y, pos_tags, lens, wfofs, tis, trs))
                    sent_count += 1"""
new_train = new_train.replace(old_inner, new_inner)

with open("src/nlp/experiments/gna_experiment.py", "w") as f:
    f.write(new_train)
