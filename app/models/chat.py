from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.models.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)

    chat_id = Column(String, index=True)

    role = Column(String)

    message = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )