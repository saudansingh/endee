from utils.embedding import Embedder
from utils.vector_store import EndeeStore

class RAGPipeline:
    def __init__(self):
        self.embedder = Embedder()
        self.store = EndeeStore()
        self.collection = "docs_collection"

    def answer(self, query):
        query_vec = self.embedder.encode([query])[0]
        results = self.store.search(self.collection, query_vec)
        
        context = "\n".join([r.payload['text'] for r in results])
        return context, results