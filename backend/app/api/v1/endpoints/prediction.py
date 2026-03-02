from fastapi import APIRouter, Depends
from typing import Any, List
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.threat_predictor import threat_predictor

router = APIRouter()

class AttackLikelihoodRequest(BaseModel):
    target: str
    threat_indicators: List[str]

class VulnExploitRequest(BaseModel):
    cve_id: str
    asset_exposure: dict

@router.post("/attack-likelihood")
async def predict_attack_likelihood(
    request: AttackLikelihoodRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await threat_predictor.predict_attack_likelihood(request.target, request.threat_indicators)

@router.post("/threat-trends")
async def forecast_threat_trends(
    days: int = 30,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await threat_predictor.forecast_threat_trends(days)

@router.post("/vulnerability-exploitation")
async def predict_vulnerability_exploitation(
    request: VulnExploitRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await threat_predictor.predict_vulnerability_exploitation(request.cve_id, request.asset_exposure)

@router.get("/forecasts")
async def get_forecasts(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await threat_predictor.get_all_predictions()
