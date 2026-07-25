from app.rag.loader import load_document
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_vector_store, add_documents
from app.rag.retriever import retrieve_documents


# Load your test document
documents = load_document(
    "data/sample.txt"
)


# Split documents into chunks
chunks = split_documents(documents)


# Create Chroma collection
vector_store = create_vector_store()


# Store embeddings
add_documents(chunks)


# Query
query = "What is artificial intelligence?"


results = retrieve_documents(query)


for doc in results:
    print("=" * 50)
    print(doc)