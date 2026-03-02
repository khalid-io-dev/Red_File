from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Any, Optional
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.web_scanner import web_scanner
import uuid

router = APIRouter()

class SQLIRequest(BaseModel):
    url: str
    method: Optional[str] = "GET"
    data: Optional[str] = None

class XSSRequest(BaseModel):
    url: str
    forms: Optional[bool] = True

class CSRFRequest(BaseModel):
    url: str

class FullScanRequest(BaseModel):
    url: str

scans = {}

@router.post("/scan/sqli")
async def scan_sqli(
    request: SQLIRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    scan_id = str(uuid.uuid4())
    scans[scan_id] = {"status": "running", "type": "sqli", "results": None}
    
    async def execute():
        result = await web_scanner.test_sql_injection(request.url, request.method, request.data)
        scans[scan_id] = {"status": "completed", "type": "sqli", "results": result}
    
    background_tasks.add_task(execute)
    return {"scan_id": scan_id, "status": "running", "type": "sqli"}

@router.post("/scan/xss")
async def scan_xss(
    request: XSSRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    scan_id = str(uuid.uuid4())
    scans[scan_id] = {"status": "running", "type": "xss", "results": None}
    
    async def execute():
        result = await web_scanner.test_xss(request.url, request.forms)
        scans[scan_id] = {"status": "completed", "type": "xss", "results": result}
    
    background_tasks.add_task(execute)
    return {"scan_id": scan_id, "status": "running", "type": "xss"}

@router.post("/scan/csrf")
async def scan_csrf(
    request: CSRFRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    scan_id = str(uuid.uuid4())
    scans[scan_id] = {"status": "running", "type": "csrf", "results": None}
    
    async def execute():
        result = await web_scanner.test_csrf(request.url)
        scans[scan_id] = {"status": "completed", "type": "csrf", "results": result}
    
    background_tasks.add_task(execute)
    return {"scan_id": scan_id, "status": "running", "type": "csrf"}

@router.post("/scan/full")
async def scan_full(
    request: FullScanRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    scan_id = str(uuid.uuid4())
    scans[scan_id] = {"status": "running", "type": "full", "results": None}
    
    async def execute():
        result = await web_scanner.full_web_scan(request.url)
        scans[scan_id] = {"status": "completed", "type": "full", "results": result}
    
    background_tasks.add_task(execute)
    return {"scan_id": scan_id, "status": "running", "type": "full"}

@router.get("/scans")
async def list_scans(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return list(scans.values())
