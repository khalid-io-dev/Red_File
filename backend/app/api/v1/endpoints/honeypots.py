from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.models.honeypot import HoneypotLog, HoneypotInstance
from app.models.user import User
from app.schemas.honeypot import HoneypotLog as HoneypotLogSchema, HoneypotLogCreate, HoneypotInstance as HoneypotInstanceSchema, HoneypotInstanceCreate

router = APIRouter()

@router.post("/logs", response_model=HoneypotLogSchema)
async def create_log(
    *,
    db: AsyncSession = Depends(deps.get_db),
    log_in: HoneypotLogCreate,
    # Ideally authenticated by honeypot API key, using generic deps for now
    # current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Ingest honeypot log.
    """
    log_entry = HoneypotLog(
        honeypot_name=log_in.honeypot_name,
        attacker_ip=log_in.attacker_ip,
        port=log_in.port,
        protocol=log_in.protocol,
        payload=log_in.payload,
        meta_data=log_in.meta_data
    )
    db.add(log_entry)
    await db.commit()
    await db.refresh(log_entry)
    return log_entry

@router.get("/logs", response_model=List[HoneypotLogSchema])
async def read_logs(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get honeypot logs.
    """
    result = await db.execute(select(HoneypotLog).order_by(HoneypotLog.timestamp.desc()).offset(skip).limit(limit))
    return result.scalars().all()

@router.post("/instance", response_model=HoneypotInstanceSchema)
async def create_instance(
    *,
    db: AsyncSession = Depends(deps.get_db),
    instance_in: HoneypotInstanceCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Register/Create a honeypot instance.
    """
    instance = HoneypotInstance(
        name=instance_in.name,
        type=instance_in.type,
        config=instance_in.config,
        status="stopped"
    )
    db.add(instance)
    await db.commit()
    await db.refresh(instance)
    return instance

@router.post("/instance/{name}/start", response_model=HoneypotInstanceSchema)
async def start_instance(
    name: str,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Start a honeypot instance (Mock).
    """
    result = await db.execute(select(HoneypotInstance).filter(HoneypotInstance.name == name))
    instance = result.scalars().first()
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    
    # Trigger docker start here
    instance.status = "running"
    instance.ip_address = "192.168.1.50" # Mock IP
    await db.commit()
    await db.refresh(instance)
    return instance
