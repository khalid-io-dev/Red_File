from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.config import settings
from app.crud import crud_user
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema, UserUpdate

router = APIRouter()

@router.get("/", response_model=List[UserSchema])
async def read_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    # Note: CRUDUser.get_multi not implemented yet, using placeholder logic or needing implementation
    # For now, just return empty list or implement get_multi in CRUDUser
    # Assuming get_multi exists or implementing basic select
    # This is a placeholder for the list endpoint
    return [] 

@router.post("/", response_model=UserSchema)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = await crud_user.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await crud_user.user.create(db, obj_in=user_in)
    return user

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
