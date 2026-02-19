"""Business logic for auth operations."""

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import RefreshToken, Role, User
from app.auth.schemas import AuthResponse, LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password


async def register_user(data: RegisterRequest, session: AsyncSession) -> AuthResponse:
    """Create a new user, assign default role, generate tokens."""

    hashed = hash_password(data.password)

    # Look up the default "viewer" role
    result = await session.execute(select(Role).where(Role.name == "viewer"))
    viewer_role = result.scalar_one_or_none()
    if not viewer_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Default role 'viewer' not found. Run the seed script.",
        )

    # Create user with default role
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hashed,
        roles=[viewer_role],
    )
    session.add(user)

    try:
        await session.flush()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists.",
        )

    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token_str = create_refresh_token(user.id)

    # Store refresh token in DB
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    session.add(RefreshToken(
        token=refresh_token_str,
        user_id=user.id,
        expires_at=expires_at,
    ))

    await session.commit()

    # Build response
    user_resp = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        roles=[role.name for role in user.roles],
    )

    token_resp = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_str,
    )

    return AuthResponse(user=user_resp, tokens=token_resp)


async def login_user(data: LoginRequest, session: AsyncSession) -> AuthResponse:
    """Verify credentials and return tokens."""

    # Look up user by username
    result = await session.execute(select(User).where(User.username == data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is disabled.",
        )

    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token_str = create_refresh_token(user.id)

    # Store refresh token in DB
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    session.add(RefreshToken(
        token=refresh_token_str,
        user_id=user.id,
        expires_at=expires_at,
    ))

    await session.commit()

    # Build response
    user_resp = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        roles=[role.name for role in user.roles],
    )

    token_resp = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_str,
    )

    return AuthResponse(user=user_resp, tokens=token_resp)
