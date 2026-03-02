from fastapi import APIRouter, Depends
from typing import Any, List
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.ioc_analyzer import ioc_analyzer

router = APIRouter()

class IPRequest(BaseModel):
    ip: str

class DomainRequest(BaseModel):
    domain: str

class HashRequest(BaseModel):
    hash: str

class URLRequest(BaseModel):
    url: str

class BatchRequest(BaseModel):
    iocs: List[dict]

@router.post("/analyze/ip")
async def analyze_ip(
    request: IPRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await ioc_analyzer.analyze_ip(request.ip)

@router.post("/analyze/domain")
async def analyze_domain(
    request: DomainRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await ioc_analyzer.analyze_domain(request.domain)

@router.post("/analyze/hash")
async def analyze_hash(
    request: HashRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await ioc_analyzer.analyze_hash(request.hash)

@router.post("/analyze/url")
async def analyze_url(
    request: URLRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await ioc_analyzer.analyze_url(request.url)

@router.post("/batch")
async def batch_analyze(
    request: BatchRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await ioc_analyzer.batch_analyze(request.iocs)
