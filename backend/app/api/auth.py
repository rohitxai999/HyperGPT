from datetime import datetime, timedelta, timezone
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_session,
    get_current_user,
    hash_password,
)
from app.database.database import get_db
from app.models.session import UserSession
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.user import UserResponse


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    """Register a new HyperGPT user."""

    existing_email = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    existing_username = (
        db.query(User)
        .filter(User.username == request.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered",
        )

    user = User(
        email=request.email,
        username=request.username,
        hashed_password=hash_password(
            request.password
        ),
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    """Authenticate a user and create a session."""

    user = authenticate_user(
        db,
        request.email,
        request.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    jti = uuid.uuid4().hex

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    session = UserSession(
        user_id=user.id,
        token_jti=jti,
        expires_at=expires_at.replace(
            tzinfo=None
        ),
    )

    db.add(session)
    db.commit()

    access_token = create_access_token(
        user_id=user.id,
        jti=jti,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """Return the currently authenticated user."""

    return current_user


@router.post(
    "/logout",
    response_model=MessageResponse,
)
def logout(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """Revoke the current user session."""

    _, session = get_current_session(
        token,
        db,
    )

    session.revoked_at = (
        datetime.now(timezone.utc)
        .replace(tzinfo=None)
    )

    db.commit()

    return MessageResponse(
        message="Successfully logged out"
    )