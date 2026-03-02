from fastapi import APIRouter, Depends
from typing import Any
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.threat_intel_aggregator import threat_intel_aggregator

router = APIRouter()

class AnalyzeRequest(BaseModel):
    ioc: str
    ioc_type: str

@router.get("/feeds")
async def get_threat_feeds(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    urlhaus = await threat_intel_aggregator.fetch_threat_feeds()
    return {
        "feeds": urlhaus,
        "total_iocs": len(urlhaus)
    }

@router.get("/actors")
async def get_threat_actors(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    actors = ["apt28", "apt29", "lazarus"]
    actor_info = []
    for actor in actors:
        info = await threat_intel_aggregator.get_threat_actor_info(actor)
        actor_info.append(info)
    return {"actors": actor_info}

@router.get("/cves")
async def get_cves(
    limit: int = 20,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    # Return sample CVEs
    return {"cves": [], "total": 0}

@router.post("/analyze")
async def analyze_ioc(
    request: AnalyzeRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await threat_intel_aggregator.check_reputation(request.ioc, request.ioc_type)
