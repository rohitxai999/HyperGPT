from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.orchestrator import Orchestrator
from app.services.memory_service import MemoryService

router = APIRouter(
    prefix="/orchestrator",
    tags=["Orchestrator"],
)

orchestrator = Orchestrator()
memory_service = MemoryService()


class ChatRequest(BaseModel):
    query: str


@router.post("/")
async def orchestrate(request: ChatRequest):

    # Analyze and save memory
    memory = memory_service.save_memory(
        user_id="default",
        text=request.query,
    )

    # Generate AI response
    response = orchestrator.run(request.query)

    return {
        "memory": memory,
        "response": response,
    }