from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from app.services.ai.attack_chain import WebAttackChain, NetworkAttackChain
from app.services.ai.agents import MasterAgent
from app.services.ai.mitre_mapper import mitre_mapper
from pydantic import BaseModel
from typing import Optional
import json

router = APIRouter()

class AttackChainRequest(BaseModel):
    target: str
    chain_type: str = "auto"  # auto, web, network

class AgentRequest(BaseModel):
    target: str
    agent_type: str = "master"  # master, web, network

@router.post("/chain/execute")
async def execute_attack_chain(
    request: AttackChainRequest,
    current_user: User = Depends(deps.get_current_active_user)
):
    """Execute predefined attack chain"""
    try:
        if request.chain_type == "web" or (request.chain_type == "auto" and request.target.startswith('http')):
            chain = WebAttackChain(request.target)
        elif request.chain_type == "network":
            chain = NetworkAttackChain(request.target)
        else:
            # Auto-detect
            if request.target.startswith('http'):
                chain = WebAttackChain(request.target)
            else:
                chain = NetworkAttackChain(request.target)
        
        results = await chain.execute()
        
        # Track MITRE techniques
        tools_used = []
        for phase_results in results['results'].values():
            tools_used.extend(phase_results.keys())
        
        mitre_coverage = mitre_mapper.get_coverage(tools_used)
        
        return {
            'success': True,
            'results': results,
            'mitre_coverage': mitre_coverage
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agent/execute")
async def execute_agent(
    request: AgentRequest,
    current_user: User = Depends(deps.get_current_active_user)
):
    """Execute specialized agent"""
    try:
        agent = MasterAgent()
        results = await agent.execute(request.target)
        
        return {
            'success': True,
            'results': results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mitre/coverage")
async def get_mitre_coverage(
    tools: str = "",  # Comma-separated tool names (optional)
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get MITRE ATT&CK coverage for tools"""
    tool_list = [t.strip() for t in tools.split(',') if t.strip()] if tools else []
    coverage = mitre_mapper.get_coverage(tool_list)
    return coverage

@router.get("/mitre/suggest")
async def suggest_next_technique(
    current_techniques: str,  # Comma-separated technique IDs
    current_user: User = Depends(deps.get_current_active_user)
):
    """Suggest next MITRE technique"""
    tech_list = [t.strip() for t in current_techniques.split(',')]
    suggestion = mitre_mapper.suggest_next_technique(tech_list)
    return suggestion

@router.get("/mitre/matrix")
async def get_attack_matrix(
    tools: str = "",
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get attack matrix visualization data"""
    tool_list = [t.strip() for t in tools.split(',') if t.strip()] if tools else []
    matrix = mitre_mapper.generate_attack_matrix(tool_list)
    return matrix

@router.get("/mitre/navigator")
async def export_navigator_layer(
    tools: str = "",
    current_user: User = Depends(deps.get_current_active_user)
):
    """Export ATT&CK Navigator layer"""
    tool_list = [t.strip() for t in tools.split(',') if t.strip()] if tools else []
    layer = mitre_mapper.export_navigator_layer(tool_list)
    return layer
