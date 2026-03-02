from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, WebSocket
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.multi_agent_orchestrator import multi_agent_orchestrator
import uuid
import asyncio

router = APIRouter()

class MissionCreate(BaseModel):
    name: str
    target: str
    objective: str
    agents: List[str]  # ["recon", "exploit", "post-exploit", "analysis"]
    strategy: Optional[str] = "adaptive"  # sequential, parallel, adaptive
    constraints: Optional[Dict] = {}
    ai_coordination: Optional[bool] = True

class AgentTask(BaseModel):
    agent_id: str
    task_type: str
    parameters: Dict
    priority: Optional[int] = 5

class CollaborationRequest(BaseModel):
    mission_id: str
    problem: str
    agents: List[str]
    context: Optional[Dict] = {}

# Mission storage
missions = {}
agent_states = {}

@router.post("/mission")
async def create_mission(
    mission: MissionCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Create AI-coordinated multi-agent mission with adaptive strategy"""
    mission_id = str(uuid.uuid4())
    
    missions[mission_id] = {
        "id": mission_id,
        "name": mission.name,
        "target": mission.target,
        "objective": mission.objective,
        "agents": mission.agents,
        "strategy": mission.strategy,
        "status": "planning",
        "phases": [],
        "results": {},
        "created_by": current_user.id
    }
    
    async def execute_mission():
        try:
            # Phase 1: AI Mission Planning
            missions[mission_id]["status"] = "planning"
            plan = await multi_agent_orchestrator.create_mission_plan(
                mission.target, mission.objective, mission.agents, 
                mission.strategy, mission.constraints
            )
            missions[mission_id]["phases"] = plan.get("phases", [])
            
            # Phase 2: Agent Initialization
            missions[mission_id]["status"] = "initializing"
            await multi_agent_orchestrator.initialize_agents(mission.agents)
            
            # Phase 3: Coordinated Execution
            missions[mission_id]["status"] = "executing"
            if mission.strategy == "parallel":
                results = await multi_agent_orchestrator.execute_parallel(
                    mission_id, plan.get("phases", [])
                )
            elif mission.strategy == "sequential":
                results = await multi_agent_orchestrator.execute_sequential(
                    mission_id, plan.get("phases", [])
                )
            else:  # adaptive
                results = await multi_agent_orchestrator.execute_adaptive(
                    mission_id, plan.get("phases", []), mission.ai_coordination
                )
            
            missions[mission_id]["results"] = results
            missions[mission_id]["status"] = "completed"
            
            # Phase 4: AI Result Synthesis
            synthesis = await multi_agent_orchestrator.synthesize_results(
                mission_id, results
            )
            missions[mission_id]["synthesis"] = synthesis
            
        except Exception as e:
            missions[mission_id]["status"] = "failed"
            missions[mission_id]["error"] = str(e)
    
    background_tasks.add_task(execute_mission)
    
    return {
        "mission_id": mission_id,
        "status": "planning",
        "message": "Mission created and planning initiated",
        "estimated_duration": "15-30 minutes"
    }

@router.get("/missions")
async def list_missions(
    status: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """List all missions with filtering"""
    user_missions = [
        m for m in missions.values() 
        if m.get("created_by") == current_user.id
    ]
    
    if status:
        user_missions = [m for m in user_missions if m.get("status") == status]
    
    return {
        "missions": user_missions,
        "total": len(user_missions),
        "by_status": {
            "planning": sum(1 for m in user_missions if m.get("status") == "planning"),
            "executing": sum(1 for m in user_missions if m.get("status") == "executing"),
            "completed": sum(1 for m in user_missions if m.get("status") == "completed"),
            "failed": sum(1 for m in user_missions if m.get("status") == "failed")
        }
    }

@router.get("/mission/{mission_id}/status")
async def get_mission_status(
    mission_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Get real-time mission status with agent progress"""
    if mission_id not in missions:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    mission = missions[mission_id]
    
    # Get agent states
    agent_progress = {}
    for agent_id in mission.get("agents", []):
        state = agent_states.get(f"{mission_id}_{agent_id}", {})
        agent_progress[agent_id] = {
            "status": state.get("status", "idle"),
            "current_task": state.get("current_task"),
            "progress": state.get("progress", 0),
            "findings": state.get("findings", [])
        }
    
    return {
        "mission_id": mission_id,
        "status": mission.get("status"),
        "current_phase": mission.get("current_phase"),
        "phases_completed": len([p for p in mission.get("phases", []) if p.get("completed")]),
        "total_phases": len(mission.get("phases", [])),
        "agent_progress": agent_progress,
        "results": mission.get("results", {}),
        "synthesis": mission.get("synthesis")
    }

@router.post("/mission/{mission_id}/pause")
async def pause_mission(
    mission_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Pause mission execution"""
    if mission_id not in missions:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    await multi_agent_orchestrator.pause_mission(mission_id)
    missions[mission_id]["status"] = "paused"
    
    return {"mission_id": mission_id, "status": "paused"}

@router.post("/mission/{mission_id}/resume")
async def resume_mission(
    mission_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Resume paused mission"""
    if mission_id not in missions:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    missions[mission_id]["status"] = "executing"
    background_tasks.add_task(multi_agent_orchestrator.resume_mission, mission_id)
    
    return {"mission_id": mission_id, "status": "resuming"}

@router.post("/coordinate")
async def coordinate_agents(
    request: CollaborationRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """AI-powered agent coordination for collaborative problem-solving"""
    result = await multi_agent_orchestrator.coordinate_agents(
        request.mission_id, request.problem, 
        request.agents, request.context
    )
    
    return {
        "mission_id": request.mission_id,
        "problem": request.problem,
        "coordination_strategy": result.get("strategy"),
        "agent_assignments": result.get("assignments"),
        "execution_plan": result.get("plan"),
        "estimated_time": result.get("estimated_time")
    }

@router.post("/agents/{agent_id}/task")
async def assign_task(
    agent_id: str,
    task: AgentTask,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Assign specific task to agent"""
    result = await multi_agent_orchestrator.assign_task(
        agent_id, task.task_type, task.parameters, task.priority
    )
    
    return {
        "agent_id": agent_id,
        "task_id": result.get("task_id"),
        "status": "assigned",
        "estimated_completion": result.get("estimated_completion")
    }

@router.get("/agents/status")
async def get_agents_status(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Get status of all agents"""
    return await multi_agent_orchestrator.get_all_agents_status()

@router.post("/agents/optimize")
async def optimize_agent_allocation(
    mission_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """AI-powered agent allocation optimization"""
    result = await multi_agent_orchestrator.optimize_allocation(mission_id)
    
    return {
        "mission_id": mission_id,
        "optimization": result.get("optimization"),
        "improvements": result.get("improvements"),
        "new_allocation": result.get("allocation")
    }

@router.get("/mission/{mission_id}/report")
async def generate_mission_report(
    mission_id: str,
    format: str = "json",
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Generate comprehensive mission report with AI insights"""
    if mission_id not in missions:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    report = await multi_agent_orchestrator.generate_report(mission_id, format)
    
    return {
        "mission_id": mission_id,
        "report": report,
        "format": format,
        "generated_at": asyncio.get_event_loop().time()
    }

@router.websocket("/mission/{mission_id}/stream")
async def stream_mission_updates(
    websocket: WebSocket,
    mission_id: str
):
    """Real-time mission updates via WebSocket"""
    await websocket.accept()
    try:
        while True:
            if mission_id in missions:
                mission = missions[mission_id]
                await websocket.send_json({
                    "mission_id": mission_id,
                    "status": mission.get("status"),
                    "progress": mission.get("progress", 0),
                    "current_phase": mission.get("current_phase"),
                    "latest_findings": mission.get("latest_findings", [])
                })
            await asyncio.sleep(2)
    except:
        pass
