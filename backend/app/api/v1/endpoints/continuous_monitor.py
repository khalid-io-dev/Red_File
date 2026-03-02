from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.continuous_monitor import continuous_monitor
import asyncio

router = APIRouter()

class MonitorConfig(BaseModel):
    name: str
    targets: List[str]
    monitor_types: List[str]  # network, logs, files, behavior
    ai_detection: Optional[bool] = True
    auto_response: Optional[bool] = False
    alert_threshold: Optional[str] = "medium"

class ResponseAction(BaseModel):
    action_type: str  # block, isolate, alert, log
    parameters: Dict

monitors = {}
threats = []

@router.post("/start")
async def start_monitoring(
    config: MonitorConfig,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Start continuous security monitoring"""
    monitor_id = f"monitor_{current_user.id}"
    
    monitors[monitor_id] = {
        "id": monitor_id,
        "name": config.name,
        "targets": config.targets,
        "types": config.monitor_types,
        "status": "active",
        "threats_detected": 0,
        "started_at": asyncio.get_event_loop().time()
    }
    
    # Start monitoring tasks
    await continuous_monitor.start_monitoring(
        monitor_id, config.targets, config.monitor_types,
        config.ai_detection, config.auto_response, config.alert_threshold
    )
    
    return {
        "monitor_id": monitor_id,
        "status": "active",
        "message": "Continuous monitoring started",
        "monitoring": config.monitor_types
    }

@router.post("/stop")
async def stop_monitoring(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Stop continuous monitoring"""
    monitor_id = f"monitor_{current_user.id}"
    
    if monitor_id not in monitors:
        raise HTTPException(status_code=404, detail="No active monitor found")
    
    await continuous_monitor.stop_monitoring(monitor_id)
    monitors[monitor_id]["status"] = "stopped"
    
    return {
        "monitor_id": monitor_id,
        "status": "stopped",
        "threats_detected": monitors[monitor_id].get("threats_detected", 0)
    }

@router.get("/status")
async def get_monitoring_status(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Get current monitoring status"""
    monitor_id = f"monitor_{current_user.id}"
    
    if monitor_id not in monitors:
        return {"status": "inactive", "message": "No active monitoring"}
    
    monitor = monitors[monitor_id]
    stats = await continuous_monitor.get_statistics(monitor_id)
    
    return {
        "monitor_id": monitor_id,
        "status": monitor.get("status"),
        "name": monitor.get("name"),
        "targets": monitor.get("targets"),
        "monitoring_types": monitor.get("types"),
        "uptime": asyncio.get_event_loop().time() - monitor.get("started_at", 0),
        "threats_detected": monitor.get("threats_detected", 0),
        "statistics": stats
    }

@router.get("/threats")
async def get_detected_threats(
    severity: Optional[str] = None,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Get detected threats with filtering"""
    monitor_id = f"monitor_{current_user.id}"
    
    filtered_threats = threats
    if severity:
        filtered_threats = [t for t in threats if t.get("severity") == severity]
    
    return {
        "threats": filtered_threats[:limit],
        "total": len(filtered_threats),
        "by_severity": {
            "critical": sum(1 for t in threats if t.get("severity") == "critical"),
            "high": sum(1 for t in threats if t.get("severity") == "high"),
            "medium": sum(1 for t in threats if t.get("severity") == "medium"),
            "low": sum(1 for t in threats if t.get("severity") == "low")
        }
    }

@router.post("/response")
async def execute_response(
    threat_id: str,
    action: ResponseAction,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Execute automated response to threat"""
    result = await continuous_monitor.execute_response(
        threat_id, action.action_type, action.parameters
    )
    
    return {
        "threat_id": threat_id,
        "action": action.action_type,
        "status": result.get("status"),
        "message": result.get("message")
    }

@router.get("/baselines")
async def get_baselines(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Get behavioral baselines"""
    monitor_id = f"monitor_{current_user.id}"
    return await continuous_monitor.get_baselines(monitor_id)

@router.post("/baselines/update")
async def update_baselines(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Update behavioral baselines"""
    monitor_id = f"monitor_{current_user.id}"
    result = await continuous_monitor.update_baselines(monitor_id)
    
    return {
        "monitor_id": monitor_id,
        "status": "updated",
        "baselines": result
    }

@router.get("/alerts/queue")
async def get_alert_queue(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Get prioritized alert queue"""
    monitor_id = f"monitor_{current_user.id}"
    return await continuous_monitor.get_alert_queue(monitor_id)

@router.get("/history")
async def get_threat_history(
    days: int = 7,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Get threat detection history"""
    monitor_id = f"monitor_{current_user.id}"
    return await continuous_monitor.get_threat_history(monitor_id, days)

@router.websocket("/stream")
async def stream_threats(
    websocket: WebSocket,
    current_user: User = Depends(deps.get_current_active_user)
):
    """Real-time threat streaming via WebSocket"""
    await websocket.accept()
    monitor_id = f"monitor_{current_user.id}"
    
    try:
        while True:
            if monitor_id in monitors and monitors[monitor_id].get("status") == "active":
                # Get latest threats
                latest_threats = await continuous_monitor.get_latest_threats(monitor_id, 10)
                
                await websocket.send_json({
                    "monitor_id": monitor_id,
                    "status": "active",
                    "threats": latest_threats,
                    "timestamp": asyncio.get_event_loop().time()
                })
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        pass
