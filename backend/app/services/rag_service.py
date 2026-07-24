from pathlib import Path

from app.rag.loader import load_document
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_vector_store
from app.rag.retriever import retrieve_documents

UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)


def process_document(file_path: str):
    """
    Load a document, split it into chunks,
    and create the vector store.
    """

    documents = load_document(file_path)

    chunks = split_documents(documents)

    create_vector_store(chunks)

    return {
        "status": "success",
        "chunks": len(chunks),
    }


def ask_document(question: str):
    """
    Search the vector store and return
    the most relevant document chunks.
    """

    results = retrieve_documents(question)

    answer = "\n\n".join(
        [doc.page_content for doc in results]
    )

    return {
        "question": question,
        "answer": answer,
        "sources": len(results),
    }