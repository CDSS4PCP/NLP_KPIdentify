import numpy as np

class calc_cosine_similarity_class:
    def __init__(self):
        pass
    
    def calc_cosine_similarity(self, vA, vB):
        return np.dot(vA, vB) / (np.sqrt(np.dot(vA,vA)) * np.sqrt(np.dot(vB,vB)))
