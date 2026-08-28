import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.session import UserSession
from app.models.user import User


SECRET_KEY = os.getenv(
    "HYPERGPT_SECRET_KEY",
    "CHANGE_THIS_SECRET_KEY_IN_PRODUCTION",
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def hash_password(password: str) -> str:
    """Hash a plain-text password securely."""
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Verify a plain password against its hash."""
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    user_id: int,
    jti: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT access token."""

    now = datetime.now(timezone.utc)

    expire = (
        now + expires_delta
        if expires_delta
        else now
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "jti": jti,
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""

    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    """Authenticate a user using email and password."""

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    return user


def get_current_session(
    token: str,
    db: Session,
) -> tuple[User, UserSession]:
    """Validate JWT and associated database session."""

    payload = decode_token(token)

    user_id = payload.get("sub")
    jti = payload.get("jti")

    if not user_id or not jti:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    session = (
        db.query(UserSession)
        .filter(
            UserSession.token_jti == jti,
            UserSession.revoked_at.is_(None),
        )
        .first()
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is invalid or revoked",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    user = (
        db.query(User)
        .filter(User.id == int(user_id))
        .first()
    )

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive or does not exist",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    now = datetime.now(timezone.utc)

    expires_at = session.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(
            tzinfo=timezone.utc
        )

    if expires_at <= now:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    return user, session


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """FastAPI dependency for protected endpoints."""

    user, _ = get_current_session(
        token,
        db,
    )

    return user