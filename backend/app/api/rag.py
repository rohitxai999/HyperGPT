from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.retriever import retrieve_documents


router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def rag_query(request: QueryRequest):

    documents = retrieve_documents(
        request.question
    )

    return {
        "question": request.question,
        "results": documents
    }