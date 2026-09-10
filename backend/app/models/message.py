from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text

from backend.app.database.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=False,
        index=True,
    )

    role = Column(
        Text,
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    conversation = __import__(
        "sqlalchemy.orm",
        fromlist=["relationship"],
    ).relationship(
        "Conversation",
        back_populates="messages",
    )