from langchain_core.vectorstores import InMemoryVectorStore

from app.rag.embeddings import get_embeddings


_vector_store = None


def create_vector_store(chunks):
    """
    Create an in-memory vector store.
    """

    global _vector_store

    embeddings = get_embeddings()

    _vector_store = InMemoryVectorStore(embedding=embeddings)

    _vector_store.add_documents(chunks)

    return _vector_store


def load_vector_store():
    """
    Return the current vector store.
    """

    if _vector_store is None:
        raise ValueError("Vector store has not been created yet.")

    return _vector_store