from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode(self, text: str):
        """
        Generate embedding vector for a text.
        """
        return self.model.encode(text).tolist()

    def encode_batch(self, texts: list[str]):
        """
        Generate embeddings for multiple texts.
        """
        return self.model.encode(texts).tolist()