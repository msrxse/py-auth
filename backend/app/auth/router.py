"""Auth API endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import AuthResponse, LoginRequest, RegisterRequest
from app.auth.service import login_user, register_user
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, session: AsyncSession = Depends(get_db)):
    return await register_user(data, session)


@router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest, session: AsyncSession = Depends(get_db)):
    return await login_user(data, session)
