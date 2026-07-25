from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.retriever import retrieve_documents


router = APIRouter()


class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
def chat(request: ChatRequest):

    documents = retrieve_documents(
        request.query
    )

    context = "\n".join(documents)

    return {
        "query": request.query,
        "context": context
    }