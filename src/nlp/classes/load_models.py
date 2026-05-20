from gensim.models.phrases import Phrases
from gensim.models import Word2Vec

class load_models:
    def __init__(self, word2vec_path='/zfs/dzrptlab/CDSS/saved_models/corpus_word2vec.model', phrase_path='/zfs/dzrptlab/CDSS/saved_models/my_phrase_model.pkl'):
        self.word2vec_path=word2vec_path
        self.phrase_path=phrase_path
    
    def load(self):
        phrase_model = Phrases.load(self.phrase_path)
        w2v_model = Word2Vec.load(self.word2vec_path)
        
        return w2v_model, phrase_model

