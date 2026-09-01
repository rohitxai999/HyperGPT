from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.agents.orchestrator import Orchestrator
from app.auth.security import get_current_user
from app.database.database import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User


router = APIRouter()

orchestrator = Orchestrator()


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1)
    conversation_id: int | None = None


@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Authenticated HyperGPT chat endpoint.

    Creates or reuses a conversation, persists the user message,
    executes the existing orchestrator, and persists the assistant
    response.
    """

    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Query cannot be empty",
        )

    # --------------------------------------------------
    # Find or create conversation
    # --------------------------------------------------

    if request.conversation_id is not None:
        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == request.conversation_id,
                Conversation.user_id == current_user.id,
            )
            .first()
        )

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )

    else:
        conversation = Conversation(
            user_id=current_user.id,
            title=query[:255],
        )

        db.add(conversation)
        db.flush()

    # --------------------------------------------------
    # Persist user message
    # --------------------------------------------------

    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=query,
    )

    db.add(user_message)
    db.flush()

    # --------------------------------------------------
    # Execute existing HyperGPT orchestrator
    # --------------------------------------------------

    try:
        result = orchestrator.run(query)

    except Exception:
        db.rollback()
        raise

    assistant_text = result.get(
        "final_response",
        "",
    )

    if not assistant_text:
        assistant_text = "No response generated."

    # --------------------------------------------------
    # Persist assistant response
    # --------------------------------------------------

    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=assistant_text,
    )

    db.add(assistant_message)

    # --------------------------------------------------
    # Update conversation activity
    # --------------------------------------------------

    conversation.updated_at = datetime.utcnow()

    db.commit()

    db.refresh(conversation)
    db.refresh(user_message)
    db.refresh(assistant_message)

    # --------------------------------------------------
    # Return existing orchestrator response + persistence
    # --------------------------------------------------

    result["conversation_id"] = conversation.id
    result["user_message_id"] = user_message.id
    result["assistant_message_id"] = assistant_message.id

    return result
