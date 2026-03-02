from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Any, Optional, Dict
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.cloud_scanner import cloud_scanner
import uuid

router = APIRouter()

class AWSCredentials(BaseModel):
    access_key: str
    secret_key: str
    region: Optional[str] = "us-east-1"

class AzureCredentials(BaseModel):
    subscription_id: str
    tenant_id: str
    client_id: str
    client_secret: str

class GCPCredentials(BaseModel):
    project_id: str
    credentials_json: str

scans = {}

@router.post("/scan/aws")
async def scan_aws(
    credentials: AWSCredentials,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    scan_id = str(uuid.uuid4())
    scans[scan_id] = {"status": "running", "provider": "aws", "results": None}
    
    async def execute():
        result = await cloud_scanner.scan_aws(credentials.access_key, credentials.secret_key, credentials.region)
        scans[scan_id] = {"status": "completed", "provider": "aws", "results": result}
    
    background_tasks.add_task(execute)
    return {"scan_id": scan_id, "status": "running", "provider": "aws"}

@router.post("/scan/azure")
async def scan_azure(
    credentials: AzureCredentials,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    scan_id = str(uuid.uuid4())
    scans[scan_id] = {"status": "running", "provider": "azure", "results": None}
    
    async def execute():
        result = await cloud_scanner.scan_azure(credentials.subscription_id, credentials.tenant_id, credentials.client_id, credentials.client_secret)
        scans[scan_id] = {"status": "completed", "provider": "azure", "results": result}
    
    background_tasks.add_task(execute)
    return {"scan_id": scan_id, "status": "running", "provider": "azure"}

@router.post("/scan/gcp")
async def scan_gcp(
    credentials: GCPCredentials,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    scan_id = str(uuid.uuid4())
    scans[scan_id] = {"status": "running", "provider": "gcp", "results": None}
    
    async def execute():
        result = await cloud_scanner.scan_gcp(credentials.project_id, credentials.credentials_json)
        scans[scan_id] = {"status": "completed", "provider": "gcp", "results": result}
    
    background_tasks.add_task(execute)
    return {"scan_id": scan_id, "status": "running", "provider": "gcp"}

@router.get("/scans")
async def list_scans(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return list(scans.values())

@router.get("/scan/{scan_id}")
async def get_scan(
    scan_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    if scan_id not in scans:
        return {"error": "Scan not found"}
    return scans[scan_id]
