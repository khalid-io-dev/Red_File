from fastapi import APIRouter, Depends, UploadFile, File
from typing import Any
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.log_analyzer import log_analyzer

router = APIRouter()

class AnalyzeRequest(BaseModel):
    log_content: str
    log_type: str

@router.post("/upload")
async def upload_logs(
    file: UploadFile = File(...),
    log_type: str = "apache",
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    content = await file.read()
    return {"file_name": file.filename, "size": len(content), "type": log_type, "status": "uploaded"}

@router.post("/analyze")
async def analyze_logs(
    request: AnalyzeRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await log_analyzer.analyze_logs(request.log_content, request.log_type)

@router.get("/threats")
async def get_threats(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await log_analyzer.detect_threats([])

@router.get("/anomalies")
async def get_anomalies(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await log_analyzer.detect_anomalies([])

@router.get("/statistics")
async def get_statistics(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await log_analyzer.generate_statistics([])
