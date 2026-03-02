from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

from app.api import deps
from app.services.multi_agent_orchestrator import multi_agent_orchestrator
from app.services.exploit_dev_framework import exploit_dev_framework
from app.services.automated_pentest import automated_pentest_engine
from app.services.continuous_monitor import continuous_monitor
from app.services.workflow_engine import workflow_engine

router = APIRouter()

# Request Models
class MultiAgentMissionRequest(BaseModel):
    objective: str
    target: str

class ExploitGenerationRequest(BaseModel):
    vulnerability_type: str
    target: str
    details: str
    cve: Optional[str] = None

class AutomatedPentestRequest(BaseModel):
    target: str
    scope: Dict
    methodology: str = "PTES"

class MonitoringRequest(BaseModel):
    targets: List[str]
    config: Dict

class WorkflowRequest(BaseModel):
    name: str
    description: str
    requirements: List[str]

class WorkflowExecutionRequest(BaseModel):
    workflow_id: int
    context: Optional[Dict] = None

# Multi-Agent Orchestration
@router.post("/multi-agent/mission")
async def execute_multi_agent_mission(
    request: MultiAgentMissionRequest,
    current_user = Depends(deps.get_current_user)
):
    """Execute coordinated multi-agent mission"""
    try:
        result = await multi_agent_orchestrator.execute_mission(
            request.objective,
            request.target
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/multi-agent/collaborate")
async def adaptive_collaboration(
    agents: List[str],
    problem: str,
    current_user = Depends(deps.get_current_user)
):
    """Agents collaborate on complex problem"""
    try:
        result = await multi_agent_orchestrator.adaptive_collaboration(agents, problem)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Exploit Development
@router.post("/exploit-dev/generate")
async def generate_custom_exploit(
    request: ExploitGenerationRequest,
    current_user = Depends(deps.get_current_user)
):
    """Generate custom exploit with AI"""
    try:
        vuln_info = {
            "type": request.vulnerability_type,
            "target": request.target,
            "details": request.details,
            "cve": request.cve
        }
        result = await exploit_dev_framework.generate_exploit(vuln_info)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/exploit-dev/add-evasion")
async def add_evasion_techniques(
    exploit_code: str,
    techniques: List[str],
    current_user = Depends(deps.get_current_user)
):
    """Add AV/EDR evasion to exploit"""
    try:
        result = await exploit_dev_framework.add_evasion(exploit_code, techniques)
        return {"evaded_code": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/exploit-dev/chain")
async def chain_exploits(
    exploit_ids: List[int],
    target: str,
    current_user = Depends(deps.get_current_user)
):
    """Chain multiple exploits"""
    try:
        exploits = [exploit_dev_framework.exploit_library[i] for i in exploit_ids if i < len(exploit_dev_framework.exploit_library)]
        result = await exploit_dev_framework.chain_exploits(exploits, target)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/exploit-dev/weaponize")
async def weaponize_poc(
    poc_code: str,
    target_info: Dict,
    current_user = Depends(deps.get_current_user)
):
    """Weaponize PoC code"""
    try:
        result = await exploit_dev_framework.auto_weaponize(poc_code, target_info)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Automated Penetration Testing
@router.post("/automated-pentest/full")
async def full_automated_pentest(
    request: AutomatedPentestRequest,
    current_user = Depends(deps.get_current_user)
):
    """Execute full automated penetration test"""
    try:
        result = await automated_pentest_engine.full_automated_pentest(
            request.target,
            request.scope,
            request.methodology
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/automated-pentest/history")
async def get_pentest_history(current_user = Depends(deps.get_current_user)):
    """Get penetration test history"""
    return {
        "history": automated_pentest_engine.pentest_history[-20:]
    }

# Continuous Monitoring
@router.post("/monitoring/start")
async def start_continuous_monitoring(
    request: MonitoringRequest,
    current_user = Depends(deps.get_current_user)
):
    """Start continuous security monitoring"""
    try:
        # Start monitoring in background
        asyncio.create_task(continuous_monitor.start_monitoring(request.targets, request.config))
        return {"status": "monitoring_started", "targets": request.targets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/monitoring/stop")
async def stop_continuous_monitoring(current_user = Depends(deps.get_current_user)):
    """Stop continuous monitoring"""
    try:
        result = await continuous_monitor.stop_monitoring()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monitoring/alerts")
async def get_monitoring_alerts(current_user = Depends(deps.get_current_user)):
    """Get recent monitoring alerts"""
    return {
        "alerts": list(continuous_monitor.alert_queue)[-50:]
    }

@router.get("/monitoring/threats")
async def get_detected_threats(current_user = Depends(deps.get_current_user)):
    """Get detected threats"""
    return {
        "threats": continuous_monitor.threat_history[-20:]
    }

# Workflow Automation
@router.post("/workflow/create")
async def create_workflow(
    request: WorkflowRequest,
    current_user = Depends(deps.get_current_user)
):
    """AI creates custom workflow"""
    try:
        result = await workflow_engine.create_workflow(
            request.name,
            request.description,
            request.requirements
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/workflow/execute")
async def execute_workflow(
    request: WorkflowExecutionRequest,
    current_user = Depends(deps.get_current_user)
):
    """Execute workflow"""
    try:
        result = await workflow_engine.execute_workflow(
            request.workflow_id,
            request.context
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/workflow/optimize/{workflow_id}")
async def optimize_workflow(
    workflow_id: int,
    current_user = Depends(deps.get_current_user)
):
    """AI optimizes workflow"""
    try:
        result = await workflow_engine.optimize_workflow(workflow_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/workflow/parallel")
async def execute_parallel_workflows(
    workflow_ids: List[int],
    context: Optional[Dict] = None,
    current_user = Depends(deps.get_current_user)
):
    """Execute multiple workflows in parallel"""
    try:
        result = await workflow_engine.parallel_workflow_execution(workflow_ids, context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/workflow/chain")
async def chain_workflows(
    workflow_ids: List[int],
    context: Optional[Dict] = None,
    current_user = Depends(deps.get_current_user)
):
    """Chain workflows"""
    try:
        result = await workflow_engine.workflow_chain(workflow_ids, context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workflow/templates")
async def get_workflow_templates(current_user = Depends(deps.get_current_user)):
    """Get workflow templates"""
    return {
        "templates": workflow_engine.workflow_templates
    }

@router.get("/workflow/history")
async def get_workflow_history(current_user = Depends(deps.get_current_user)):
    """Get workflow execution history"""
    return {
        "history": workflow_engine.execution_history[-50:]
    }

@router.get("/status")
async def get_automation_status(current_user = Depends(deps.get_current_user)):
    """Get status of all automation systems"""
    return {
        "multi_agent": {
            "agents": len(multi_agent_orchestrator.agents),
            "missions_completed": len(multi_agent_orchestrator.mission_history)
        },
        "exploit_dev": {
            "exploits_generated": len(exploit_dev_framework.exploit_library)
        },
        "automated_pentest": {
            "pentests_completed": len(automated_pentest_engine.pentest_history)
        },
        "monitoring": {
            "active": continuous_monitor.monitoring_active,
            "alerts": len(continuous_monitor.alert_queue),
            "threats": len(continuous_monitor.threat_history)
        },
        "workflows": {
            "total_workflows": len(workflow_engine.workflows),
            "executions": len(workflow_engine.execution_history)
        }
    }

# Status and Health
@router.get("/automation/status")
async def get_automation_status_legacy(current_user = Depends(deps.get_current_user)):
    """Get status of all automation systems"""
    return {
        "multi_agent": {
            "agents": len(multi_agent_orchestrator.agents),
            "missions_completed": len(multi_agent_orchestrator.mission_history)
        },
        "exploit_dev": {
            "exploits_generated": len(exploit_dev_framework.exploit_library)
        },
        "automated_pentest": {
            "pentests_completed": len(automated_pentest_engine.pentest_history)
        },
        "monitoring": {
            "active": continuous_monitor.monitoring_active,
            "alerts": len(continuous_monitor.alert_queue),
            "threats": len(continuous_monitor.threat_history)
        },
        "workflows": {
            "total_workflows": len(workflow_engine.workflows),
            "executions": len(workflow_engine.execution_history)
        }
    }
