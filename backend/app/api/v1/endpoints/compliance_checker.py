from fastapi import APIRouter, Depends
from typing import Any, List
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.compliance_checker import compliance_checker

router = APIRouter()

class ControlMapping(BaseModel):
    framework: str
    control_id: str
    asset_ids: List[str]

@router.get("/frameworks")
async def list_frameworks(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await compliance_checker.get_supported_frameworks()

@router.post("/check/{framework}")
async def check_compliance(
    framework: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await compliance_checker.check_compliance(framework)

@router.get("/gaps")
async def get_compliance_gaps(
    framework: str = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await compliance_checker.identify_gaps(framework)

@router.get("/audit-readiness")
async def get_audit_readiness(
    framework: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await compliance_checker.assess_audit_readiness(framework)

@router.post("/map-controls")
async def map_controls(
    mapping: ControlMapping,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await compliance_checker.map_controls_to_assets(mapping.framework, mapping.control_id, mapping.asset_ids)
