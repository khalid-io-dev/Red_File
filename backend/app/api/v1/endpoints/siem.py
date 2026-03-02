from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.siem_integrator import siem_integrator
import asyncio
import json

router = APIRouter()

class SplunkConnection(BaseModel):
    host: str
    port: int
    username: str
    password: str
    scheme: Optional[str] = "https"

class ElasticConnection(BaseModel):
    hosts: List[str]
    username: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None

class QRadarConnection(BaseModel):
    host: str
    api_token: str
    verify_ssl: Optional[bool] = True

class SentinelConnection(BaseModel):
    workspace_id: str
    tenant_id: str
    client_id: str
    client_secret: str

class QueryRequest(BaseModel):
    siem_type: str
    query: str
    time_range: Optional[str] = "last_24h"
    limit: Optional[int] = 1000

class DashboardCreate(BaseModel):
    name: str
    siem_type: str
    widgets: List[Dict]
    refresh_interval: Optional[int] = 60

class AlertRuleCreate(BaseModel):
    name: str
    siem_type: str
    query: str
    severity: str
    threshold: Optional[int] = 1
    actions: List[str]

# Connection management
connections = {}

@router.post("/connect/splunk")
async def connect_splunk(
    config: SplunkConnection,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Connect to Splunk SIEM with connection pooling"""
    try:
        result = await siem_integrator.connect_splunk(
            config.host, config.port, config.username, 
            config.password, config.scheme
        )
        connections[f"splunk_{current_user.id}"] = {
            "type": "splunk",
            "config": config.model_dump(exclude={"password"}),
            "status": "connected"
        }
        return {
            "status": "connected",
            "siem_type": "splunk",
            "connection_id": f"splunk_{current_user.id}",
            "capabilities": result.get("capabilities", []),
            "version": result.get("version")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Splunk connection failed: {str(e)}")

@router.post("/connect/elastic")
async def connect_elastic(
    config: ElasticConnection,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Connect to Elasticsearch with cluster health check"""
    try:
        result = await siem_integrator.connect_elasticsearch(
            config.hosts, config.username, config.password, config.api_key
        )
        connections[f"elastic_{current_user.id}"] = {
            "type": "elastic",
            "config": config.model_dump(exclude={"password", "api_key"}),
            "status": "connected"
        }
        return {
            "status": "connected",
            "siem_type": "elasticsearch",
            "connection_id": f"elastic_{current_user.id}",
            "cluster_name": result.get("cluster_name"),
            "cluster_health": result.get("cluster_health"),
            "indices_count": result.get("indices_count")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Elasticsearch connection failed: {str(e)}")

@router.post("/connect/qradar")
async def connect_qradar(
    config: QRadarConnection,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Connect to IBM QRadar with API validation"""
    try:
        result = await siem_integrator.connect_qradar(
            config.host, config.api_token, config.verify_ssl
        )
        connections[f"qradar_{current_user.id}"] = {
            "type": "qradar",
            "config": config.model_dump(exclude={"api_token"}),
            "status": "connected"
        }
        return {
            "status": "connected",
            "siem_type": "qradar",
            "connection_id": f"qradar_{current_user.id}",
            "version": result.get("version"),
            "offenses_count": result.get("offenses_count")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QRadar connection failed: {str(e)}")

@router.post("/connect/sentinel")
async def connect_sentinel(
    config: SentinelConnection,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Connect to Microsoft Sentinel with Azure AD authentication"""
    try:
        result = await siem_integrator.connect_sentinel(
            config.workspace_id, config.tenant_id, 
            config.client_id, config.client_secret
        )
        connections[f"sentinel_{current_user.id}"] = {
            "type": "sentinel",
            "config": config.model_dump(exclude={"client_secret"}),
            "status": "connected"
        }
        return {
            "status": "connected",
            "siem_type": "sentinel",
            "connection_id": f"sentinel_{current_user.id}",
            "workspace_name": result.get("workspace_name"),
            "incidents_count": result.get("incidents_count")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentinel connection failed: {str(e)}")

@router.get("/connections")
async def list_connections(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """List all active SIEM connections"""
    user_connections = {
        k: v for k, v in connections.items() 
        if k.endswith(f"_{current_user.id}")
    }
    return {"connections": list(user_connections.values()), "total": len(user_connections)}

@router.post("/query")
async def execute_query(
    request: QueryRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Execute optimized query across SIEM platforms with result caching"""
    try:
        result = await siem_integrator.execute_query(
            request.siem_type, request.query, 
            request.time_range, request.limit
        )
        return {
            "siem_type": request.siem_type,
            "query": request.query,
            "execution_time": result.get("execution_time"),
            "total_results": result.get("total_results"),
            "results": result.get("results", []),
            "cached": result.get("cached", False)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")

@router.post("/query/batch")
async def execute_batch_queries(
    queries: List[QueryRequest],
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Execute multiple queries in parallel with result aggregation"""
    tasks = [
        siem_integrator.execute_query(q.siem_type, q.query, q.time_range, q.limit)
        for q in queries
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return {
        "total_queries": len(queries),
        "successful": sum(1 for r in results if not isinstance(r, Exception)),
        "failed": sum(1 for r in results if isinstance(r, Exception)),
        "results": [r if not isinstance(r, Exception) else {"error": str(r)} for r in results]
    }

@router.get("/dashboards")
async def list_dashboards(
    siem_type: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """List SIEM dashboards with real-time metrics"""
    return await siem_integrator.get_dashboards(siem_type)

@router.post("/dashboards")
async def create_dashboard(
    dashboard: DashboardCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Create custom dashboard with auto-refresh"""
    return await siem_integrator.create_dashboard(
        dashboard.name, dashboard.siem_type, 
        dashboard.widgets, dashboard.refresh_interval
    )

@router.post("/alerts/rules")
async def create_alert_rule(
    rule: AlertRuleCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Create correlation rule with multi-action support"""
    return await siem_integrator.create_alert_rule(
        rule.name, rule.siem_type, rule.query, 
        rule.severity, rule.threshold, rule.actions
    )

@router.get("/alerts/active")
async def get_active_alerts(
    siem_type: Optional[str] = None,
    severity: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Get active alerts with filtering and correlation"""
    return await siem_integrator.get_active_alerts(siem_type, severity)

@router.post("/export")
async def export_data(
    siem_type: str,
    query: str,
    format: str = "json",
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Export SIEM data in multiple formats (JSON, CSV, STIX)"""
    return await siem_integrator.export_data(siem_type, query, format)

@router.get("/statistics")
async def get_statistics(
    siem_type: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Get comprehensive SIEM statistics and health metrics"""
    return await siem_integrator.get_statistics(siem_type)

@router.websocket("/stream/{siem_type}")
async def stream_events(
    websocket: WebSocket,
    siem_type: str,
    query: Optional[str] = None
):
    """Real-time event streaming from SIEM with WebSocket"""
    await websocket.accept()
    try:
        while True:
            events = await siem_integrator.stream_events(siem_type, query)
            await websocket.send_json({"events": events, "timestamp": asyncio.get_event_loop().time()})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass
