from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    chat_id: Optional[str] = None
    model: str = "llama-3.3-70b-versatile"