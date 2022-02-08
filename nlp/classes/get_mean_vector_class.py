import numpy as np
class get_mean_vector_class:
    def __init__(self):
        pass
    
    def get_mean_vector(self, w2v_model, words, dims=(150,)):
        # remove out-of-vocabulary words
        #In gensin 3.8, words = [word for word in words if word in word2vec_model.wv.vocab]
        for word in words:
            if word in w2v_model.wv.key_to_index:
                continue
            else:
                return "vocab not present"

        if len(words) >= 1:
            dummy_zeros = np.zeros(dims)
            for word in words:
                dummy_zeros = dummy_zeros + w2v_model.wv.get_vector(word)
            return dummy_zeros/len(words)
        else:
            return "nothing"
