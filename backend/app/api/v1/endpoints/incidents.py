from fastapi import APIRouter, Depends
from typing import Any, Optional, Dict, List
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.incident_responder import incident_responder

router = APIRouter()

class IncidentCreate(BaseModel):
    title: str
    severity: str
    description: str
    affected_systems: List[str]

class IncidentAction(BaseModel):
    action_type: str
    description: str
    details: Optional[Dict] = {}

class Evidence(BaseModel):
    type: str
    description: str
    file_path: Optional[str] = None
    data: Optional[Dict] = {}

@router.get("/")
async def list_incidents(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    filters = {}
    if status: filters['status'] = status
    if severity: filters['severity'] = severity
    return await incident_responder.get_incidents(filters)

@router.post("/")
async def create_incident(
    incident: IncidentCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await incident_responder.create_incident(incident.model_dump())

@router.put("/{incident_id}")
async def update_incident(
    incident_id: str,
    updates: Dict,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await incident_responder.update_incident(incident_id, updates)

@router.post("/{incident_id}/actions")
async def add_action(
    incident_id: str,
    action: IncidentAction,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await incident_responder.add_action(incident_id, action.action_type, action.description, action.details)

@router.get("/{incident_id}/timeline")
async def get_timeline(
    incident_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await incident_responder.get_incident_timeline(incident_id)

@router.post("/{incident_id}/evidence")
async def add_evidence(
    incident_id: str,
    evidence: Evidence,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await incident_responder.collect_evidence(incident_id, evidence.type, evidence.description, evidence.file_path, evidence.data)
