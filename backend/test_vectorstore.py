from pathlib import Path

from app.rag.loader import load_document
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_vector_store

UPLOADS = Path("uploads")

pdfs = list(UPLOADS.glob("*.pdf"))

if not pdfs:
    print("No PDF found.")
    exit()

pdf = pdfs[0]

print(f"Loading: {pdf.name}")

documents = load_document(str(pdf))

chunks = split_documents(documents)

db = create_vector_store(chunks)

print("=" * 60)
print("✅ InMemory Vector Store Created Successfully!")
print(f"Pages  : {len(documents)}")
print(f"Chunks : {len(chunks)}")
print("=" * 60)