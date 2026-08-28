from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Lazy-loading embedding service.

    The SentenceTransformer model is loaded only when
    encode() or encode_batch() is actually called.
    """

    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        self.model = None

    def _get_model(self) -> SentenceTransformer:
        """Load the embedding model only when required."""

        if self.model is None:
            self.model = SentenceTransformer(
                self.MODEL_NAME
            )

        return self.model

    def encode(self, text: str) -> list[float]:
        """
        Generate an embedding vector for a single text.
        """

        model = self._get_model()

        return model.encode(
            text
        ).tolist()

    def encode_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        model = self._get_model()

        return model.encode(
            texts
        ).tolist()