from pathlib import Path

from app.rag.loader import load_document

UPLOADS = Path("uploads")

pdfs = list(UPLOADS.glob("*.pdf"))

if not pdfs:
    print("❌ No PDF files found in uploads folder.")
    exit()

pdf = pdfs[0]

print(f"Loading: {pdf.name}")

docs = load_document(str(pdf))

print(f"\n✅ Loaded {len(docs)} pages\n")

print("=" * 60)
print(docs[0].page_content[:500])
print("=" * 60)