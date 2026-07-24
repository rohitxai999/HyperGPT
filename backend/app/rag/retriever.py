from app.rag.vectorstore import load_vector_store


def retrieve_documents(query: str, k: int = 4):
    """
    Retrieve the most relevant document chunks.
    """

    vectorstore = load_vector_store()

    results = vectorstore.similarity_search(
        query=query,
        k=k
    )

    return results