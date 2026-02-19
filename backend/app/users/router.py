"""User API endpoints."""

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.auth.schemas import UserMeResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserMeResponse)
async def me(user: User = Depends(get_current_user)):
    # Collect unique permissions from all roles
    permissions = {perm.name for role in user.roles for perm in role.permissions}

    return UserMeResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
        roles=[role.name for role in user.roles],
        permissions=sorted(permissions),
    )
