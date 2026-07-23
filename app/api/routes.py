from fastapi import APIRouter
from app.schemas.request import ChatRequest
from app.schemas.response import ChatResponse
from app.services.llm_service import LLMService

router = APIRouter()

llm = LLMService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    reply = llm.generate_response(
        message=request.message,
        chat_id=request.chat_id or "default",
        model=request.model
    )

    return ChatResponse(
        response=reply,
        chat_id=request.chat_id or "default"
    )