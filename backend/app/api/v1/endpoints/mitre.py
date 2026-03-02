from fastapi import APIRouter, Depends
from typing import Any
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.mitre_mapper import mitre_mapper

router = APIRouter()

class MapFindingRequest(BaseModel):
    finding_description: str
    tool_name: str

@router.get("/tactics")
async def get_tactics(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await mitre_mapper.get_all_tactics()

@router.get("/techniques")
async def get_techniques(
    tactic_id: str = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    if tactic_id:
        return await mitre_mapper.get_techniques_by_tactic(tactic_id)
    return await mitre_mapper.get_all_techniques()

@router.get("/matrix")
async def get_attack_matrix(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await mitre_mapper.generate_attack_matrix()

@router.post("/map-finding")
async def map_finding(
    request: MapFindingRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await mitre_mapper.map_finding_to_technique(request.finding_description, request.tool_name)

@router.get("/coverage")
async def get_coverage(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await mitre_mapper.get_coverage_statistics()
