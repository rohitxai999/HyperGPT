from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.models.database import Base


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)

    chat_id = Column(
        String,
        index=True,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    embedding = Column(
        Text,
        nullable=True
    )

    importance = Column(
        Integer,
        default=1
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )