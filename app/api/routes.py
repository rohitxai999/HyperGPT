from fastapi import APIRouter
from app.schemas.request import ChatRequest
from app.schemas.response import ChatResponse
from app.services.llm_service import LLMService

router = APIRouter()

llm = LLMService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    reply = llm.generate_response(request.message)

    return ChatResponse(response=reply)