from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384 # Dimension for MiniLM

    def encode(self, text_list):
        return self.model.encode(text_list).tolist()