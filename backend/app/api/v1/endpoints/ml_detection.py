from fastapi import APIRouter, Depends, UploadFile, File
from typing import Any
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.ml_detector import ml_detector

router = APIRouter()

class EmailContent(BaseModel):
    subject: str
    body: str
    sender: str

class TrafficData(BaseModel):
    packets: list
    metadata: dict

@router.post("/detect/malware")
async def detect_malware(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    content = await file.read()
    return await ml_detector.detect_malware(content, file.filename)

@router.post("/detect/phishing")
async def detect_phishing(
    email: EmailContent,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await ml_detector.detect_phishing_email(email.subject, email.body, email.sender)

@router.post("/detect/intrusion")
async def detect_intrusion(
    traffic: TrafficData,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await ml_detector.detect_network_intrusion(traffic.packets, traffic.metadata)

@router.post("/detect/anomaly")
async def detect_anomaly(
    data: dict,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await ml_detector.detect_anomaly(data)

@router.get("/models")
async def list_models(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await ml_detector.get_model_info()
