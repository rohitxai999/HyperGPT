from app.rag.vectorstore import create_vector_store
from app.rag.embeddings import generate_embeddings



def retrieve_documents(query, k=3):

    collection = create_vector_store()


    query_embedding = generate_embeddings(
        [query]
    )[0]


    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=k
    )


    documents = results["documents"][0]


    return documents