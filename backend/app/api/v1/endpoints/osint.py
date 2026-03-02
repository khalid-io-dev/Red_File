from fastapi import APIRouter, Depends, HTTPException
from typing import Any, Optional
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.osint_collector import osint_collector

router = APIRouter()

class EmailHarvestRequest(BaseModel):
    domain: str
    limit: Optional[int] = 100

class WhoisRequest(BaseModel):
    domain: str

class SubdomainRequest(BaseModel):
    domain: str

class SocialProfileRequest(BaseModel):
    username: str

class GeolocationRequest(BaseModel):
    ip_address: str

class FullScanRequest(BaseModel):
    target: str

@router.post("/email-harvest")
async def harvest_emails(
    request: EmailHarvestRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await osint_collector.harvest_emails(request.domain, request.limit)

@router.post("/whois")
async def whois_lookup(
    request: WhoisRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await osint_collector.whois_lookup(request.domain)

@router.post("/subdomains")
async def enumerate_subdomains(
    request: SubdomainRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await osint_collector.enumerate_subdomains(request.domain)

@router.post("/social-profiles")
async def find_social_profiles(
    request: SocialProfileRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await osint_collector.find_social_profiles(request.username)

@router.post("/geolocation")
async def geolocate_ip(
    request: GeolocationRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await osint_collector.geolocate_ip(request.ip_address)

@router.post("/full-scan")
async def full_osint_scan(
    request: FullScanRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await osint_collector.full_osint_gathering(request.target)

@router.get("/results/{scan_id}")
async def get_scan_results(
    scan_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return {"scan_id": scan_id, "status": "completed", "results": {}}
