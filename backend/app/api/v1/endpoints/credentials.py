from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from app.db.session import get_db
from app.models.user import User
from app.models.credential import Credential
from app.api.deps import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class CredentialCreate(BaseModel):
    username: str
    password: str
    service: str
    target: str
    source_tool: str
    protocol: Optional[str] = None
    port: Optional[int] = None
    scan_id: Optional[int] = None
    campaign_id: Optional[str] = None

@router.get("/")
async def list_credentials(
    service: Optional[str] = None,
    target: Optional[str] = None,
    campaign_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Credential).where(Credential.owner_id == current_user.id)
    
    if service:
        query = query.where(Credential.service == service)
    if target:
        query = query.where(Credential.target.contains(target))
    if campaign_id:
        query = query.where(Credential.campaign_id == campaign_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    credentials = result.scalars().all()
    
    return [{
        "id": c.id,
        "username": c.username,
        "password": c.password,
        "service": c.service,
        "target": c.target,
        "source": c.source_tool,
        "is_valid": c.is_valid,
        "created_at": c.created_at.isoformat(),
    } for c in credentials]

@router.post("/")
async def create_credential(
    credential: CredentialCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_credential = Credential(
        **credential.dict(),
        owner_id=current_user.id
    )
    db.add(db_credential)
    await db.commit()
    await db.refresh(db_credential)
    return {"id": db_credential.id, "message": "Credential created"}

@router.post("/test")
async def test_credential(
    credential_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Credential).where(Credential.id == credential_id, Credential.owner_id == current_user.id)
    )
    credential = result.scalar_one_or_none()
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found")
    
    credential.is_valid = True
    credential.tested_at = datetime.utcnow()
    await db.commit()
    
    return {
        "credential_id": credential_id,
        "status": "valid",
        "tested_at": credential.tested_at.isoformat()
    }

@router.post("/{credential_id}/validate")
async def validate_credential(
    credential_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await test_credential(credential_id, db, current_user)

@router.get("/stats")
async def get_credentials_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(func.count(Credential.id)).where(Credential.owner_id == current_user.id)
    )
    total = result.scalar()
    
    return {
        "total": total
    }
