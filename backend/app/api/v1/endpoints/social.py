from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.models.user import User
from app.models.social_engineering import SECampaign
from app.services.osint_collector import osint_collector
from app.services.phishing_crafter import phishing_crafter
from app.services.social_campaign_executor import campaign_executor
from app.services.websocket_manager import websocket_manager
from pydantic import BaseModel
from typing import Dict, Optional
import asyncio
import json

router = APIRouter()

class OSINTRequest(BaseModel):
    target: str
    target_type: str  # domain, email, name, ip

class EmailCraftRequest(BaseModel):
    target_info: Dict
    payload_link: str
    template_type: str = "urgent_security"

class SECampaignCreate(BaseModel):
    name: str
    target_email: str
    target_name: Optional[str] = None
    target_company: Optional[str] = None
    template_type: str
    payload_id: Optional[int] = None

class FakeLoginRequest(BaseModel):
    brand: str

@router.post("/osint")
async def gather_osint(
    request: OSINTRequest,
    current_user: User = Depends(deps.get_current_active_user)
):
    """Gather OSINT on target"""
    try:
        if request.target_type == "domain":
            results = {
                "emails": await osint_collector.harvest_emails(request.target),
                "whois": await osint_collector.whois_lookup(request.target),
                "subdomains": await osint_collector.subdomain_enum(request.target)
            }
        elif request.target_type == "email":
            domain = request.target.split("@")[1]
            results = {
                "emails": await osint_collector.harvest_emails(domain),
                "ip_info": await osint_collector.get_ip_info(domain)
            }
        elif request.target_type == "name":
            results = {
                "social_profiles": await osint_collector.find_social_profiles(request.target)
            }
        elif request.target_type == "ip":
            results = {
                "ip_info": await osint_collector.get_ip_info(request.target)
            }
        else:
            results = await osint_collector.gather_full_osint(request.target)
        
        return {"success": True, "data": results}
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post("/email-craft")
async def craft_email(
    request: EmailCraftRequest,
    current_user: User = Depends(deps.get_current_active_user)
):
    """Generate phishing email"""
    email = await phishing_crafter.generate_email(
        request.target_info,
        request.payload_link,
        request.template_type
    )
    return email

@router.post("/campaign")
async def create_campaign(
    request: SECampaignCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Create and execute social engineering campaign"""
    # Create campaign
    campaign = SECampaign(
        name=request.name,
        target_email=request.target_email,
        target_name=request.target_name,
        target_company=request.target_company,
        owner_id=current_user.id,
        status="planning"
    )
    
    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)
    
    # Execute campaign in background
    async def execute():
        try:
            campaign_data = {
                "target": request.target_email,
                "target_name": request.target_name,
                "target_company": request.target_company,
                "campaign_type": "phishing",
                "pretext": f"Security update for {request.target_company or 'your organization'}"
            }
            
            await campaign_executor.execute_campaign(campaign.id, campaign_data, websocket_manager)
            
            # Update campaign in DB
            async with db.begin():
                db_campaign = await db.get(SECampaign, campaign.id)
                if db_campaign:
                    status_data = campaign_executor.get_campaign_status(campaign.id)
                    db_campaign.status = status_data.get("status", "completed")
                    metrics = status_data.get("metrics", {})
                    db_campaign.email_opened = metrics.get("clicks", 0) > 0
                    db_campaign.link_clicked = metrics.get("credentials_captured", 0) > 0
        except Exception as e:
            print(f"Campaign execution error: {e}")
    
    background_tasks.add_task(execute)
    
    return {
        "success": True,
        "campaign": {
            "id": campaign.id,
            "name": campaign.name,
            "target": campaign.target_email,
            "status": "executing"
        }
    }

@router.get("/campaigns")
async def list_campaigns(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """List user's SE campaigns"""
    result = await db.execute(
        select(SECampaign).filter(SECampaign.owner_id == current_user.id)
    )
    campaigns = result.scalars().all()
    
    return {
        "campaigns": [
            {
                "id": c.id,
                "name": c.name,
                "target": c.target_email,
                "status": c.status or "planning",
                "email_opened": c.email_opened or False,
                "link_clicked": c.link_clicked or False,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "logs": [
                    {"timestamp": c.created_at.isoformat(), "event": "Campaign created", "details": f"Target: {c.target_email}"}
                ],
                "metrics": {
                    "emails_sent": 1,
                    "emails_opened": 1 if c.email_opened else 0,
                    "links_clicked": 1 if c.link_clicked else 0,
                    "credentials_captured": 0
                }
            }
            for c in campaigns
        ]
    }

@router.get("/campaign/{campaign_id}")
async def get_campaign(
    campaign_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get campaign details with real-time logs"""
    result = await db.execute(
        select(SECampaign).filter(
            SECampaign.id == campaign_id,
            SECampaign.owner_id == current_user.id
        )
    )
    campaign = result.scalars().first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Get real-time execution data
    execution_data = campaign_executor.get_campaign_status(campaign_id)
    
    return {
        "id": campaign.id,
        "name": campaign.name,
        "target": campaign.target_email,
        "target_name": campaign.target_name,
        "target_company": campaign.target_company,
        "status": execution_data.get("status", campaign.status or "planning"),
        "phase": execution_data.get("phase", "initialization"),
        "email_opened": campaign.email_opened or False,
        "link_clicked": campaign.link_clicked or False,
        "created_at": campaign.created_at.isoformat() if campaign.created_at else None,
        "logs": execution_data.get("logs", []),
        "timeline": execution_data.get("timeline", []),
        "metrics": execution_data.get("metrics", {
            "emails_sent": 1 if campaign.status != "planning" else 0,
            "emails_opened": 1 if campaign.email_opened else 0,
            "links_clicked": 1 if campaign.link_clicked else 0,
            "credentials_captured": 0
        })
    }

@router.websocket("/campaign/{campaign_id}/stream")
async def stream_campaign(
    websocket: WebSocket,
    campaign_id: int
):
    """Stream real-time campaign updates via WebSocket"""
    await websocket.accept()
    try:
        while True:
            status = campaign_executor.get_campaign_status(campaign_id)
            if status.get("status") != "unknown":
                await websocket.send_json(status)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")

@router.post("/fake-login")
async def create_fake_login(
    request: FakeLoginRequest,
    current_user: User = Depends(deps.get_current_active_user)
):
    """Generate fake login page"""
    result = await phishing_crafter.create_fake_login(request.brand)
    return result

@router.post("/tracking-link")
async def create_tracking_link(
    url: str,
    current_user: User = Depends(deps.get_current_active_user)
):
    """Generate tracking link"""
    result = await phishing_crafter.generate_tracking_link(url)
    return result

@router.post("/spear-phishing")
async def craft_spear_phishing(
    target_info: Dict,
    current_user: User = Depends(deps.get_current_active_user)
):
    """Generate highly personalized spear-phishing email"""
    email = await phishing_crafter.craft_spear_phishing(target_info)
    return email
