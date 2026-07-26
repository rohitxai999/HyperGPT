from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.orchestrator import Orchestrator

router = APIRouter(
    prefix="/orchestrator",
    tags=["Orchestrator"],
)

orchestrator = Orchestrator()


class ChatRequest(BaseModel):
    query: str


@router.post("/")
async def orchestrate(request: ChatRequest):
    return orchestrator.run(request.query)