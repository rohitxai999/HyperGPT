from app.rag.embeddings import get_embeddings

embedding = get_embeddings()

vector = embedding.embed_query("Hello HyperGPT")

print(f"Vector Length: {len(vector)}")
print(vector[:10])