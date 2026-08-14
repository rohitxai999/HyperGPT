from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.orchestrator import Orchestrator


router = APIRouter()

orchestrator = Orchestrator()


class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
def chat(request: ChatRequest):

    result = orchestrator.run(
        request.query
    )

    return result