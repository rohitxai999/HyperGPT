from app.memory.embedding_service import EmbeddingService

embedder = EmbeddingService()

vector = embedder.encode(
    "HyperGPT now has a persistent memory engine."
)

print(f"Vector Length: {len(vector)}")
print("\nFirst 10 Values:")
print(vector[:10])