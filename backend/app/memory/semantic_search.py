from app.memory.embedding_service import EmbeddingService
from app.memory.vector_index import VectorIndex


class SemanticSearch:

    def __init__(self):
        self.embedder = EmbeddingService()
        self.index = VectorIndex()

    def add_memory(self, memory_id: int, text: str):
        embedding = self.embedder.encode(text)
        self.index.add(memory_id, embedding)

    def search(self, query: str, k: int = 5):
        embedding = self.embedder.encode(query)
        return self.index.search(embedding, k)