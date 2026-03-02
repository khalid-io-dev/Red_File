from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from app.services.ai.agent import SecurityAgent
from app.services.agents.manager import agent_manager
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json

router = APIRouter()

# In-memory agent state
agent_states = {
    "vuln-scanner": "idle",
    "threat-hunter": "idle",
    "exploit-gen": "idle",
    "report-writer": "idle"
}

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    stream: bool = True

class TaskRequest(BaseModel):
    task: str
    context: Optional[Dict[str, Any]] = None
    model: Optional[str] = None
    stream: bool = True

@router.post("/chat")
async def chat_with_agent(
    request: ChatRequest,
    current_user: User = Depends(deps.get_current_user)
):
    agent = SecurityAgent()
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    
    if request.stream:
        async def generate():
            async for chunk in agent.chat(messages, stream=True):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(generate(), media_type="text/event-stream")
    else:
        response = ""
        async for chunk in agent.chat(messages, stream=False):
            response += chunk
        return {"response": response}

@router.post("/task")
async def execute_task(
    request: TaskRequest,
    current_user: User = Depends(deps.get_current_user)
):
    import logging
    logger = logging.getLogger(__name__)
    
    print(f"\n\n=== TASK REQUEST RECEIVED ===")
    print(f"Task: {request.task}")
    print(f"Stream: {request.stream}")
    print(f"User: {current_user.email}")
    print(f"=== END ===")
    
    logger.info(f"Task request received: {request.task}")
    
    # Use specified model or default to GLM
    model = request.model or "huihui_ai/glm-4.7-flash-abliterated:q4_K"
    agent = SecurityAgent(model=model)
    logger.info(f"Using model: {model}")
    
    if request.stream:
        async def generate():
            try:
                print("Starting task execution generator")
                logger.info("Starting task execution")
                async for event in agent.execute_task(request.task, request.context, stream=True):
                    print(f"Event: {event['type']}")
                    logger.info(f"Event: {event}")
                    yield f"data: {json.dumps(event)}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as e:
                print(f"ERROR: {e}")
                logger.error(f"Error in task execution: {e}", exc_info=True)
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
        
        return StreamingResponse(generate(), media_type="text/event-stream")
    else:
        events = []
        async for event in agent.execute_task(request.task, request.context, stream=False):
            events.append(event)
        return {"events": events}

@router.get("/status")
async def agent_status(
    current_user: User = Depends(deps.get_current_user)
):
    from app.services.ai.tools import registry
    
    tools = [
        {
            "name": tool.name,
            "description": tool.get_description(),
            "parameters": [p.dict() for p in tool.get_parameters()]
        }
        for tool in registry.get_all_tools()
    ]
    
    available_models = [
        {"value": "huihui_ai/glm-4.7-flash-abliterated:q4_K", "label": "GLM-4.7-Flash (Best Reasoning)", "size": "18GB", "tools": True},
        {"value": "qwen2.5-coder:7b-instruct", "label": "Qwen2.5-Coder (Fast)", "size": "4.7GB", "tools": True},
        {"value": "deepseek-coder:6.7b-instruct", "label": "DeepSeek-Coder (Balanced)", "size": "3.8GB", "tools": False},
    ]
    
    return {
        "status": "operational",
        "model": "huihui_ai/glm-4.7-flash-abliterated:q4_K",
        "available_models": available_models,
        "tools_available": len(tools),
        "tools": tools
    }

@router.get("/agents")
async def list_agents(
    current_user: User = Depends(deps.get_current_user)
):
    """List all available AI agents"""
    agents = [
        {
            "id": "vuln-scanner",
            "name": "Vulnerability Scanner Agent",
            "description": "Automatically scans targets for vulnerabilities",
            "status": agent_states.get("vuln-scanner", "idle"),
            "capabilities": ["Port Scanning", "Service Detection", "CVE Matching"],
            "tasks_completed": 234,
            "success_rate": 96,
            "uptime": "15d 8h"
        },
        {
            "id": "threat-hunter",
            "name": "Threat Hunter Agent",
            "description": "Proactively hunts for threats in network traffic",
            "status": agent_states.get("threat-hunter", "idle"),
            "capabilities": ["Traffic Analysis", "Anomaly Detection", "IOC Matching"],
            "tasks_completed": 567,
            "success_rate": 92,
            "uptime": "12d 4h"
        },
        {
            "id": "exploit-gen",
            "name": "Exploit Generator Agent",
            "description": "Generates exploits based on discovered vulnerabilities",
            "status": agent_states.get("exploit-gen", "idle"),
            "capabilities": ["Exploit Generation", "Payload Creation", "Testing"],
            "tasks_completed": 89,
            "success_rate": 88,
            "uptime": "8d 12h"
        },
        {
            "id": "report-writer",
            "name": "Report Writer Agent",
            "description": "Automatically generates security reports",
            "status": agent_states.get("report-writer", "idle"),
            "capabilities": ["Data Analysis", "Report Generation", "Visualization"],
            "tasks_completed": 892,
            "success_rate": 98,
            "uptime": "20d 2h"
        }
    ]
    return {"agents": agents}

@router.post("/agents/{agent_id}/start")
async def start_agent(
    agent_id: str,
    current_user: User = Depends(deps.get_current_user),
    target: Optional[str] = Query(None)
):
    """Start an agent with optional target"""
    if agent_id not in agent_states:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    print(f"\n=== START AGENT REQUEST ===")
    print(f"Agent ID: {agent_id}")
    print(f"Target received: {target}")
    print(f"Target type: {type(target)}")
    print(f"=== END ===")
    
    # Start real agent with target
    success = await agent_manager.start_agent(agent_id, target)
    
    if success:
        agent_states[agent_id] = "active"
        return {"success": True, "message": f"Agent {agent_id} started", "status": "active", "agent_id": agent_id}
    else:
        return {"success": False, "message": "Agent already running", "status": agent_states[agent_id]}

@router.post("/agents/{agent_id}/pause")
async def pause_agent(
    agent_id: str,
    current_user: User = Depends(deps.get_current_user)
):
    """Pause an agent"""
    if agent_id not in agent_states:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Stop real agent
    success = await agent_manager.stop_agent(agent_id)
    
    agent_states[agent_id] = "idle"
    return {"success": True, "message": f"Agent {agent_id} paused", "status": "idle", "agent_id": agent_id}

@router.get("/agents/{agent_id}/logs")
async def get_agent_logs(
    agent_id: str,
    limit: int = 20,
    current_user: User = Depends(deps.get_current_user)
):
    """Get agent activity logs"""
    logs = agent_manager.get_agent_logs(agent_id, limit)
    return {"agent_id": agent_id, "logs": logs}

@router.get("/agents/{agent_id}/results")
async def get_agent_results(
    agent_id: str,
    current_user: User = Depends(deps.get_current_user)
):
    """Get agent scan results"""
    results = agent_manager.get_agent_results(agent_id)
    return {"agent_id": agent_id, "results": results, "count": len(results)}

@router.get("/agents/{agent_id}")
async def get_agent(
    agent_id: str,
    current_user: User = Depends(deps.get_current_user)
):
    """Get agent details with real-time data"""
    is_running = agent_manager.is_agent_running(agent_id)
    logs = agent_manager.get_agent_logs(agent_id, 5)
    results = agent_manager.get_agent_results(agent_id)
    
    return {
        "id": agent_id,
        "status": "active" if is_running else "idle",
        "logs": logs,
        "results_count": len(results),
        "latest_results": results[-3:] if results else []
    }
