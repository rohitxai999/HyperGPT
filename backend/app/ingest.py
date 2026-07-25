from pathlib import Path

from app.rag.loader import load_document
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_vector_store


def ingest_documents():
    """
    Load all supported documents from the uploads folder
    and build the vector store.
    """

    # Path to backend/uploads
    upload_dir = Path(__file__).resolve().parent.parent / "uploads"

    if not upload_dir.exists():
        raise FileNotFoundError(f"Uploads folder not found: {upload_dir}")

    all_chunks = []

    for file in upload_dir.iterdir():

        if file.suffix.lower() in [".pdf", ".docx", ".txt", ".md"]:

            print(f"Loading: {file.name}")

            documents = load_document(str(file))

            chunks = split_documents(documents)

            all_chunks.extend(chunks)

    print(f"\nTotal chunks created: {len(all_chunks)}")

    create_vector_store(all_chunks)

    print("\n✅ Vector store created successfully!")


if __name__ == "__main__":
    ingest_documents()