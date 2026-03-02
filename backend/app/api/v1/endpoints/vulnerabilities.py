from fastapi import APIRouter, Depends
from typing import Any, Optional, Dict
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.vulnerability_manager import vulnerability_manager

router = APIRouter()

class VulnerabilityCreate(BaseModel):
    title: str
    cve_id: Optional[str] = None
    cvss_score: Optional[float] = None
    severity: str
    description: str
    affected_assets: list
    status: Optional[str] = "open"

class RemediationPlan(BaseModel):
    steps: list
    timeline: str
    assigned_to: Optional[str] = None

@router.get("/")
async def list_vulnerabilities(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    filters = {}
    if severity: filters['severity'] = severity
    if status: filters['status'] = status
    return await vulnerability_manager.get_vulnerabilities(filters)

@router.post("/")
async def create_vulnerability(
    vuln: VulnerabilityCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await vulnerability_manager.add_vulnerability(vuln.model_dump())

@router.put("/{vuln_id}")
async def update_vulnerability(
    vuln_id: str,
    updates: Dict,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await vulnerability_manager.update_vulnerability(vuln_id, updates)

@router.post("/{vuln_id}/remediation")
async def create_remediation_plan(
    vuln_id: str,
    plan: RemediationPlan,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await vulnerability_manager.create_remediation_plan(vuln_id, plan.steps, plan.timeline, plan.assigned_to)

@router.post("/{vuln_id}/accept-risk")
async def accept_risk(
    vuln_id: str,
    justification: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await vulnerability_manager.accept_risk(vuln_id, justification, current_user.email)

@router.get("/trends")
async def get_trends(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await vulnerability_manager.get_vulnerability_trends()
