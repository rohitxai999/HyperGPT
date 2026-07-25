import chromadb
from app.rag.embeddings import generate_embeddings


client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="hypergpt_documents"
)


def create_vector_store():

    return collection


def add_documents(documents):

    texts = [
        doc.page_content 
        for doc in documents
    ]

    embeddings = generate_embeddings(texts)

    ids = [
        str(i)
        for i in range(len(texts))
    ]

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids
    )


    return True