from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.models.user_management import UserActivity
from app.api.deps import get_current_user
from app.core.rbac import has_permission
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class ActivityLog(BaseModel):
    action: str
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None

@router.get("/")
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(current_user, "users:manage"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return [{
        "id": u.id,
        "email": u.email,
        "full_name": u.full_name,
        "role": getattr(u, 'role', 'viewer'),
        "is_active": u.is_active
    } for u in users]

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(current_user, "users:manage"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": getattr(user, 'role', 'viewer'),
        "is_active": user.is_active
    }

@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(current_user, "users:manage"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.full_name:
        user.full_name = user_update.full_name
    if user_update.role:
        setattr(user, 'role', user_update.role)
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    
    await db.commit()
    return {"message": "User updated"}

@router.post("/activity")
async def log_activity(
    activity: ActivityLog,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = UserActivity(
        user_id=current_user.id,
        action=activity.action,
        resource_type=activity.resource_type,
        resource_id=activity.resource_id
    )
    db.add(log)
    await db.commit()
    return {"message": "Activity logged"}

@router.get("/{user_id}/activity")
async def get_user_activity(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_permission(current_user, "users:manage"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    result = await db.execute(
        select(UserActivity)
        .where(UserActivity.user_id == user_id)
        .order_by(UserActivity.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    activities = result.scalars().all()
    return [{
        "id": a.id,
        "action": a.action,
        "resource_type": a.resource_type,
        "resource_id": a.resource_id,
        "created_at": a.created_at.isoformat()
    } for a in activities]
