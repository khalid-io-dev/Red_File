from fastapi import APIRouter, Depends
from typing import Any, List
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.anomaly_detector import anomaly_detector

router = APIRouter()

class TrafficData(BaseModel):
    data_points: List[float]
    timestamps: List[str]

class LoginData(BaseModel):
    user_id: str
    login_times: List[str]
    ip_addresses: List[str]

class DataTransferData(BaseModel):
    volumes: List[float]
    timestamps: List[str]

@router.post("/detect/traffic")
async def detect_traffic_anomalies(
    request: TrafficData,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await anomaly_detector.detect_network_traffic_anomalies(request.data_points, request.timestamps)

@router.post("/detect/login")
async def detect_login_anomalies(
    request: LoginData,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await anomaly_detector.detect_login_anomalies(request.user_id, request.login_times, request.ip_addresses)

@router.post("/detect/data-transfer")
async def detect_data_transfer_anomalies(
    request: DataTransferData,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await anomaly_detector.detect_data_transfer_anomalies(request.volumes, request.timestamps)

@router.get("/statistics")
async def get_statistics(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await anomaly_detector.get_anomaly_statistics()
