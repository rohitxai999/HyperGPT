from typing import List


class EmbeddingEngine:
    """
    Placeholder embedding engine.

    In future versions this class can be upgraded to use:
    - Sentence Transformers
    - OpenAI Embeddings
    - Ollama Embeddings
    - HuggingFace Models
    """

    def generate_embedding(self, text: str) -> List[float]:
        """
        Return a placeholder embedding vector.
        """
        return [0.0] * 384

    def similarity(
        self,
        embedding1: List[float],
        embedding2: List[float],
    ) -> float:
        """
        Placeholder similarity score.
        """
        return 0.0