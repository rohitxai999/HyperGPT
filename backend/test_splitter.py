from pathlib import Path

from app.rag.loader import load_document
from app.rag.splitter import split_documents

UPLOADS = Path("uploads")

pdfs = list(UPLOADS.glob("*.pdf"))

if not pdfs:
    print("No PDF found.")
    exit()

pdf = pdfs[0]

print(f"Loading: {pdf.name}")

documents = load_document(str(pdf))

chunks = split_documents(documents)

print("\n" + "=" * 60)
print(f"Original Pages : {len(documents)}")
print(f"Total Chunks   : {len(chunks)}")
print("=" * 60)

print("\nFirst Chunk:\n")
print(chunks[0].page_content)

print("\nChunk Metadata:\n")
print(chunks[0].metadata)