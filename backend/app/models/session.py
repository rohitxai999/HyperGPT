from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.database.database import Base


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    token_jti = Column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    expires_at = Column(
        DateTime,
        nullable=False,
    )

    revoked_at = Column(
        DateTime,
        nullable=True,
    )