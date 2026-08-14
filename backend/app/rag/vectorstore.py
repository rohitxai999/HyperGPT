import chromadb

from app.rag.embeddings import generate_embeddings


client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="hypergpt_documents"
)


def create_vector_store(documents=None):
    """
    Create or return the HyperGPT vector store.

    If documents are provided, they are embedded
    and added to the Chroma collection.
    """

    if documents:

        texts = [
            doc.page_content
            for doc in documents
        ]

        embeddings = generate_embeddings(texts)

        ids = [
            f"doc_{i}"
            for i in range(len(texts))
        ]

        collection.upsert(
            documents=texts,
            embeddings=embeddings,
            ids=ids
        )

    return collection


def add_documents(documents):
    """
    Add documents to the existing vector store.
    """

    return create_vector_store(documents)