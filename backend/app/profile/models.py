from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String, unique=True, nullable=False)

    name = Column(String, default="")

    profession = Column(String, default="")

    interests = Column(Text, default="[]")

    goals = Column(Text, default="[]")

    skills = Column(Text, default="[]")

    favorite_languages = Column(Text, default="[]")

    favorite_frameworks = Column(Text, default="[]")

    projects = Column(Text, default="[]")

    preferred_response_length = Column(String, default="medium")

    preferred_ui_style = Column(String, default="modern")

    personality = Column(String, default="professional")

    summary = Column(Text, default="")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )