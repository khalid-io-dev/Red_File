from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Optional, List, Dict

from app.api import deps
from app.services.network_topology import network_topology_mapper
from app.services.honeypot_manager import honeypot_manager
from app.services.ids_ips_manager import ids_ips_manager
from app.services.websocket_manager import websocket_manager
from app.services.custom_tool_integration import custom_tool_integration
from app.services.performance_optimizer import performance_optimizer

router = APIRouter()

# Network Topology
@router.get("/topology/status")
async def get_topology_status(current_user = Depends(deps.get_current_user)):
    """Get network topology status"""
    return {
        "enabled": True,
        "nodes": len(network_topology_mapper.topology.get("nodes", [])),
        "edges": len(network_topology_mapper.topology.get("edges", []))
    }

@router.post("/topology/discover")
async def discover_network_topology(
    target_range: str,
    current_user = Depends(deps.get_current_user)
):
    """Discover and map network topology"""
    try:
        result = await network_topology_mapper.discover_topology(target_range)
        return result
    except Exception as e:
        return {"error": str(e)}

@router.get("/topology/current")
async def get_current_topology(current_user = Depends(deps.get_current_user)):
    """Get current network topology"""
    return network_topology_mapper.topology

# Honeypot Management
@router.get("/honeypot/status")
async def get_honeypot_status(current_user = Depends(deps.get_current_user)):
    """Get honeypot status"""
    return await honeypot_manager.get_honeypot_status()

@router.get("/honeypot/dionaea")
async def get_dionaea_logs(current_user = Depends(deps.get_current_user)):
    """Get Dionaea honeypot logs"""
    return await honeypot_manager.parse_dionaea_logs()

@router.get("/honeypot/cowrie")
async def get_cowrie_logs(current_user = Depends(deps.get_current_user)):
    """Get Cowrie honeypot logs"""
    return await honeypot_manager.parse_cowrie_logs()

@router.get("/honeypot/analytics")
async def get_honeypot_analytics(current_user = Depends(deps.get_current_user)):
    """Get honeypot attack analytics"""
    return await honeypot_manager.get_attack_analytics()

class HoneypotControlRequest(BaseModel):
    honeypot_type: str

@router.post("/honeypot/{action}")
async def control_honeypot(
    action: str,
    request: HoneypotControlRequest,
    current_user = Depends(deps.get_current_user)
):
    """Start or stop a honeypot"""
    honeypot_type = request.honeypot_type
    
    if action not in ["start", "stop"]:
        return {"success": False, "message": "Invalid action. Use 'start' or 'stop'"}
    
    if honeypot_type not in ["cowrie", "dionaea"]:
        return {"success": False, "message": "Invalid honeypot type. Use 'cowrie' or 'dionaea'"}
    
    if action == "start":
        return await honeypot_manager.start_honeypot(honeypot_type)
    else:
        return await honeypot_manager.stop_honeypot(honeypot_type)

# IDS/IPS Management
@router.get("/ids/status")
async def get_ids_status(current_user = Depends(deps.get_current_user)):
    """Get IDS/IPS status"""
    return {
        "enabled": True,
        "systems": ["snort", "suricata"],
        "active": True
    }

@router.get("/ids/snort/alerts")
async def get_snort_alerts(
    limit: int = 100,
    current_user = Depends(deps.get_current_user)
):
    """Get Snort alerts"""
    return await ids_ips_manager.get_snort_alerts(limit)

@router.get("/ids/suricata/alerts")
async def get_suricata_alerts(
    limit: int = 100,
    current_user = Depends(deps.get_current_user)
):
    """Get Suricata alerts"""
    return await ids_ips_manager.get_suricata_alerts(limit)

@router.get("/ids/combined")
async def get_combined_ids_alerts(current_user = Depends(deps.get_current_user)):
    """Get combined IDS/IPS alerts"""
    return await ids_ips_manager.get_combined_alerts()

@router.post("/ids/snort/rules")
async def manage_snort_rules(
    action: str,
    rule: Optional[str] = None,
    current_user = Depends(deps.get_current_user)
):
    """Manage Snort rules"""
    return await ids_ips_manager.manage_snort_rules(action, rule)

@router.post("/ids/suricata/rules")
async def manage_suricata_rules(
    action: str,
    rule: Optional[str] = None,
    current_user = Depends(deps.get_current_user)
):
    """Manage Suricata rules"""
    return await ids_ips_manager.manage_suricata_rules(action, rule)

# WebSocket Real-Time Updates
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            
            # Handle subscription
            if data.get("action") == "subscribe":
                topic = data.get("topic")
                await websocket_manager.subscribe(websocket, topic)
                await websocket.send_json({"status": "subscribed", "topic": topic})
            
            # Handle ping
            elif data.get("action") == "ping":
                await websocket.send_json({"status": "pong"})
    
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

# Custom Tool Integration
@router.post("/tools/register")
async def register_custom_tool(
    name: str,
    category: str,
    config: Dict,
    current_user = Depends(deps.get_current_user)
):
    """Register custom tool"""
    # Note: executor would need to be provided separately
    return {"status": "registered", "name": name, "category": category}

@router.post("/tools/execute")
async def execute_custom_tool(
    tool_name: str,
    params: Dict,
    current_user = Depends(deps.get_current_user)
):
    """Execute custom tool"""
    return await custom_tool_integration.execute_tool(tool_name, params)

@router.get("/tools/list")
async def list_custom_tools(current_user = Depends(deps.get_current_user)):
    """List all custom tools"""
    return custom_tool_integration.get_all_tools()

@router.get("/tools/category/{category}")
async def get_tools_by_category(
    category: str,
    current_user = Depends(deps.get_current_user)
):
    """Get tools by category"""
    return {"category": category, "tools": custom_tool_integration.get_tools_by_category(category)}

# Performance Optimization
@router.get("/performance/stats")
async def get_performance_stats(current_user = Depends(deps.get_current_user)):
    """Get performance statistics"""
    return performance_optimizer.get_performance_stats()

@router.get("/performance/slow-queries")
async def get_slow_queries(
    threshold_ms: float = 100,
    current_user = Depends(deps.get_current_user)
):
    """Get slow queries"""
    return {"slow_queries": performance_optimizer.get_slow_queries(threshold_ms)}

@router.post("/performance/clear-cache")
async def clear_performance_cache(current_user = Depends(deps.get_current_user)):
    """Clear performance cache"""
    performance_optimizer.clear_cache()
    return {"status": "cache_cleared"}

@router.get("/enhancements/status")
async def get_enhancements_status(current_user = Depends(deps.get_current_user)):
    """Get status of all Phase 2 enhancements"""
    return {
        "network_topology": {"enabled": True, "nodes": len(network_topology_mapper.topology.get("nodes", []))},
        "honeypots": {"enabled": True, "types": ["dionaea", "cowrie"]},
        "ids_ips": {"enabled": True, "systems": ["snort", "suricata"]},
        "websocket": {"enabled": True, "active_connections": len(websocket_manager.active_connections)},
        "custom_tools": {"enabled": True, "registered": len(custom_tool_integration.registered_tools)},
        "performance": {"enabled": True, "cache_size": len(performance_optimizer.cache)}
    }
