from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from app.services.ai.campaign_manager import campaign_manager, CampaignStatus
from app.services.ai.reasoning_engine import reasoning_engine
from app.services.ai.result_parser import ResultAggregator
from app.services.ai.attack_chain import WebAttackChain, NetworkAttackChain
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union

router = APIRouter()

# Campaign Models
class CampaignCreate(BaseModel):
    name: str
    targets: List[str]
    description: Optional[str] = None
    chain_type: Optional[str] = "auto"
    options: Optional[Dict[str, Any]] = None

class CampaignUpdate(BaseModel):
    status: Optional[str] = None

class AnalyzeRequest(BaseModel):
    results: Union[Dict[str, Any], str]
    model: Optional[str] = "qwen2.5-coder:7b-instruct"

class StrategyRequest(BaseModel):
    target: str
    recon_data: Union[Dict[str, Any], str]
    model: Optional[str] = "qwen2.5-coder:7b-instruct"

class NextActionRequest(BaseModel):
    findings: Union[List[Dict], str]
    tools_used: Union[List[str], str]
    model: Optional[str] = "qwen2.5-coder:7b-instruct"

class AttackPathRequest(BaseModel):
    findings: Union[Dict[str, Any], str]
    model: Optional[str] = "qwen2.5-coder:7b-instruct"

class DefensesRequest(BaseModel):
    tool_outputs: Union[Dict[str, str], str]
    model: Optional[str] = "qwen2.5-coder:7b-instruct"

# Campaign Endpoints
@router.get("/")
async def list_campaigns(
    current_user: User = Depends(deps.get_current_user)
):
    campaigns = campaign_manager.list_campaigns(
        owner_id=None if current_user.is_superuser else current_user.id
    )
    return {'campaigns': [c.to_dict() for c in campaigns]}

@router.post("/")
async def create_campaign(
    request: CampaignCreate,
    current_user: User = Depends(deps.get_current_user)
):
    campaign = campaign_manager.create_campaign(
        name=request.name,
        targets=request.targets,
        owner_id=current_user.id
    )
    return {'success': True, 'campaign': campaign.to_dict()}

@router.get("/{campaign_id}")
async def get_campaign(
    campaign_id: str,
    current_user: User = Depends(deps.get_current_user)
):
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    if campaign.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return campaign_manager.get_campaign_summary(campaign_id)

@router.post("/{campaign_id}/start")
async def start_campaign(
    campaign_id: str,
    current_user: User = Depends(deps.get_current_user)
):
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    if campaign.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    campaign.start()
    
    # Execute attack chains for all targets
    for target in campaign.targets:
        try:
            if target.startswith('http'):
                chain = WebAttackChain(target)
            else:
                chain = NetworkAttackChain(target)
            
            results = await chain.execute()
            campaign.add_result(target, results)
            
            # Extract findings
            for phase_name, phase_results in results['results'].items():
                for tool_name, tool_result in phase_results.items():
                    if tool_result.get('success'):
                        campaign.add_finding(
                            target=target,
                            tool=tool_name,
                            severity='Medium',
                            description=f"{tool_name} completed successfully"
                        )
        except Exception as e:
            campaign.add_finding(
                target=target,
                tool='system',
                severity='Low',
                description=f"Error: {str(e)}"
            )
    
    campaign.complete()
    return {'success': True, 'campaign': campaign.to_dict()}

@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: str,
    current_user: User = Depends(deps.get_current_user)
):
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    if campaign.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    campaign_manager.delete_campaign(campaign_id)
    return {'success': True}

# Reasoning Engine Endpoints
@router.post("/reasoning/analyze")
async def analyze_results(
    request: AnalyzeRequest,
    current_user: User = Depends(deps.get_current_user)
):
    reasoning_engine.set_model(request.model)
    analysis = await reasoning_engine.analyze_results(request.results)
    return analysis

@router.post("/reasoning/strategy")
async def build_strategy(
    request: StrategyRequest,
    current_user: User = Depends(deps.get_current_user)
):
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Building strategy for target: {request.target}")
    reasoning_engine.set_model(request.model)
    strategy = await reasoning_engine.build_attack_strategy(request.target, request.recon_data)
    logger.info(f"Strategy built successfully with {len(strategy)} steps")
    
    return {'strategy': strategy}

@router.post("/reasoning/next-action")
async def suggest_next_action(
    request: NextActionRequest,
    current_user: User = Depends(deps.get_current_user)
):
    reasoning_engine.set_model(request.model)
    suggestion = await reasoning_engine.suggest_next_action(request.findings, request.tools_used)
    return suggestion

@router.post("/reasoning/attack-path")
async def identify_attack_path(
    request: AttackPathRequest,
    current_user: User = Depends(deps.get_current_user)
):
    reasoning_engine.set_model(request.model)
    path = await reasoning_engine.identify_attack_path(request.findings)
    return {'attack_path': path}

@router.post("/reasoning/detect-defenses")
async def detect_defenses(
    request: DefensesRequest,
    current_user: User = Depends(deps.get_current_user)
):
    reasoning_engine.set_model(request.model)
    defenses = await reasoning_engine.detect_defenses(request.tool_outputs)
    return defenses
