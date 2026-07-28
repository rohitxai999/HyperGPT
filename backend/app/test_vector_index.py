from app.memory.embedding_service import EmbeddingService
from app.memory.vector_index import VectorIndex

embedder = EmbeddingService()
index = VectorIndex()

texts = [
    "HyperGPT Memory Engine",
    "ForexMind AI Prediction",
    "JARVIS AI Assistant"
]

for i, text in enumerate(texts):
    embedding = embedder.encode(text)
    index.add(i + 1, embedding)

print("Total vectors:", index.total_vectors())

query = embedder.encode("HyperGPT AI")

results = index.search(query)

print("\nSearch Results:")

for item in results:
    print(item)