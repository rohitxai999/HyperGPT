from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database.database import Base


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, default="default", index=True)
    content = Column(Text, nullable=False)
    importance = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)