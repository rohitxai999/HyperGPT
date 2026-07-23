from fastapi import APIRouter, HTTPException
from sqlalchemy import func

from app.models.database import SessionLocal
from app.models.chat import Chat

router = APIRouter(prefix="/chat-manager", tags=["Chat Manager"])


@router.get("/chats")
def get_all_chats():
    db = SessionLocal()

    try:
        chats = (
            db.query(
                Chat.chat_id,
                func.max(Chat.created_at).label("last_message")
            )
            .group_by(Chat.chat_id)
            .order_by(func.max(Chat.created_at).desc())
            .all()
        )

        return [
            {
                "chat_id": chat.chat_id,
                "last_message": chat.last_message
            }
            for chat in chats
        ]

    finally:
        db.close()


@router.get("/chat/{chat_id}")
def get_chat(chat_id: str):

    db = SessionLocal()

    try:
        messages = (
            db.query(Chat)
            .filter(Chat.chat_id == chat_id)
            .order_by(Chat.created_at.asc())
            .all()
        )

        return [
            {
                "role": msg.role,
                "message": msg.message,
                "created_at": msg.created_at
            }
            for msg in messages
        ]

    finally:
        db.close()


@router.delete("/chat/{chat_id}")
def delete_chat(chat_id: str):

    db = SessionLocal()

    try:

        deleted = (
            db.query(Chat)
            .filter(Chat.chat_id == chat_id)
            .delete()
        )

        db.commit()

        if deleted == 0:
            raise HTTPException(
                status_code=404,
                detail="Chat not found"
            )

        return {
            "message": "Chat deleted successfully"
        }

    finally:
        db.close()