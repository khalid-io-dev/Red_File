from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

from app.api import deps
from app.services.ai_orchestrator import ai_orchestrator

router = APIRouter()

class AutonomousAssessmentRequest(BaseModel):
    target: str
    assessment_type: str = "full"

class ExploitGenerationRequest(BaseModel):
    vulnerability: str
    target_info: Dict

class CommandFixRequest(BaseModel):
    failed_command: str
    error: str

class NextStepsRequest(BaseModel):
    current_results: List[Dict]

class ConsensusRequest(BaseModel):
    question: str

@router.post("/autonomous-assessment")
async def autonomous_security_assessment(
    request: AutonomousAssessmentRequest,
    current_user = Depends(deps.get_current_user)
):
    """AI-driven autonomous security assessment"""
    try:
        result = await ai_orchestrator.autonomous_assessment(
            request.target,
            request.assessment_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-exploit")
async def generate_exploit_code(
    request: ExploitGenerationRequest,
    current_user = Depends(deps.get_current_user)
):
    """AI generates exploit code for vulnerability"""
    try:
        result = await ai_orchestrator.generate_exploit_code(
            request.vulnerability,
            request.target_info
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fix-command")
async def fix_failed_command(
    request: CommandFixRequest,
    current_user = Depends(deps.get_current_user)
):
    """AI fixes failed commands automatically"""
    try:
        result = await ai_orchestrator.fix_failed_command(
            request.failed_command,
            request.error
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/suggest-next-steps")
async def suggest_next_steps(
    request: NextStepsRequest,
    current_user = Depends(deps.get_current_user)
):
    """AI suggests next steps based on findings"""
    try:
        result = await ai_orchestrator.suggest_next_steps(
            request.current_results
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/consensus")
async def multi_model_consensus(
    request: ConsensusRequest,
    current_user = Depends(deps.get_current_user)
):
    """Get consensus from all AI models"""
    try:
        result = await ai_orchestrator.multi_model_consensus(
            request.question
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tools")
async def get_available_tools(current_user = Depends(deps.get_current_user)):
    """Get list of tools AI can use"""
    return {
        "tools": ai_orchestrator.tools,
        "models": ai_orchestrator.models
    }

@router.get("/history")
async def get_execution_history(current_user = Depends(deps.get_current_user)):
    """Get AI execution history"""
    return {
        "history": ai_orchestrator.execution_history[-50:]
    }
