from fastapi import APIRouter, Depends
from typing import Any, Optional, List, Dict
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.alert_manager import alert_manager

router = APIRouter()

class AlertCreate(BaseModel):
    title: str
    severity: str
    description: str
    source: str
    metadata: Optional[Dict] = {}

class AlertRule(BaseModel):
    name: str
    condition: str
    severity: str
    actions: List[str]

@router.get("/")
async def list_alerts(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    filters = {}
    if severity: filters['severity'] = severity
    if status: filters['status'] = status
    return await alert_manager.get_alerts(filters)

@router.post("/")
async def create_alert(
    alert: AlertCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await alert_manager.create_alert(alert.model_dump())

@router.put("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await alert_manager.acknowledge_alert(alert_id, current_user.email)

@router.put("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: str,
    resolution: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await alert_manager.resolve_alert(alert_id, current_user.email, resolution)

@router.post("/rules")
async def create_alert_rule(
    rule: AlertRule,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await alert_manager.create_alert_rule(rule.model_dump())

@router.get("/statistics")
async def get_statistics(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await alert_manager.get_alert_statistics()
