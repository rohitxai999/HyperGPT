from pathlib import Path

from app.rag.loader import load_document
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_vector_store
from app.rag.retriever import retrieve_documents

UPLOADS = Path("uploads")

pdf = list(UPLOADS.glob("*.pdf"))[0]

documents = load_document(str(pdf))
chunks = split_documents(documents)

create_vector_store(chunks)

query = "What is this document about?"

results = retrieve_documents(query)

print("=" * 60)
print(f"Query: {query}")
print("=" * 60)

for i, doc in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("-" * 40)
    print(doc.page_content[:500])