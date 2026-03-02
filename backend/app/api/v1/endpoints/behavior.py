from fastapi import APIRouter, Depends
from typing import Any
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.behavior_analyzer import behavior_analyzer

router = APIRouter()

class UserBehaviorRequest(BaseModel):
    user_id: str
    activities: list

class EntityBehaviorRequest(BaseModel):
    entity_id: str
    entity_type: str
    activities: list

@router.post("/analyze/user")
async def analyze_user_behavior(
    request: UserBehaviorRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await behavior_analyzer.analyze_user_behavior(request.user_id, request.activities)

@router.post("/analyze/entity")
async def analyze_entity_behavior(
    request: EntityBehaviorRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await behavior_analyzer.analyze_entity_behavior(request.entity_id, request.entity_type, request.activities)

@router.get("/baselines")
async def get_baselines(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await behavior_analyzer.get_behavioral_baselines()

@router.get("/anomalies")
async def get_anomalies(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await behavior_analyzer.detect_insider_threats()

@router.get("/risk-scores")
async def get_risk_scores(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await behavior_analyzer.get_risk_scores()
