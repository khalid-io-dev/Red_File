from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.session import get_db
from app.models.user import User
from app.models.scan import Scan
from app.models.finding import Finding
from app.models.credential import Credential
from app.models.campaign import Campaign
from app.api.deps import get_current_user
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_scans = await db.scalar(select(func.count(Scan.id)))
    total_findings = await db.scalar(select(func.count(Finding.id)))
    total_credentials = await db.scalar(select(func.count(Credential.id)))
    total_campaigns = await db.scalar(select(func.count(Campaign.id)))
    
    active_scans = await db.scalar(
        select(func.count(Scan.id)).where(Scan.status == "RUNNING")
    )
    
    critical_findings = await db.scalar(
        select(func.count(Finding.id)).where(Finding.severity == "critical")
    )
    
    high_findings = await db.scalar(
        select(func.count(Finding.id)).where(Finding.severity == "high")
    )
    
    active_campaigns = await db.scalar(
        select(func.count(Campaign.id)).where(Campaign.status == "active")
    )
    
    validated_credentials = await db.scalar(
        select(func.count(Credential.id)).where(Credential.is_valid == True)
    )
    
    return {
        "total_scans": total_scans or 0,
        "total_findings": total_findings or 0,
        "total_credentials": total_credentials or 0,
        "total_campaigns": total_campaigns or 0,
        "active_scans": active_scans or 0,
        "critical_findings": critical_findings or 0,
        "high_findings": high_findings or 0,
        "active_campaigns": active_campaigns or 0,
        "validated_credentials": validated_credentials or 0
    }

@router.get("/activity")
async def get_recent_activity(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Scan).order_by(Scan.created_at.desc()).limit(limit)
    )
    scans = result.scalars().all()
    
    activities = []
    for s in scans:
        # Map scan status to activity type
        if s.status == "RUNNING":
            activity_type = "scan"
        elif s.status == "COMPLETED":
            activity_type = "defense"
        elif s.status == "FAILED":
            activity_type = "attack"
        else:
            activity_type = "scan"
        
        activities.append({
            "id": s.id,
            "type": activity_type,
            "title": f"Scan {s.scan_type}",
            "description": f"{s.scan_type.title()} scan on {s.target_url} - {s.status}",
            "timestamp": s.created_at.isoformat() if s.created_at else datetime.utcnow().isoformat(),
            "severity": "medium" if s.status == "RUNNING" else "low"
        })
    
    return activities

@router.get("/severity-distribution")
async def get_severity_distribution(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get findings distribution by severity"""
    critical = await db.scalar(select(func.count(Finding.id)).where(Finding.severity == "critical"))
    high = await db.scalar(select(func.count(Finding.id)).where(Finding.severity == "high"))
    medium = await db.scalar(select(func.count(Finding.id)).where(Finding.severity == "medium"))
    low = await db.scalar(select(func.count(Finding.id)).where(Finding.severity == "low"))
    info = await db.scalar(select(func.count(Finding.id)).where(Finding.severity == "info"))
    
    return {
        "critical": critical or 0,
        "high": high or 0,
        "medium": medium or 0,
        "low": low or 0,
        "info": info or 0
    }

@router.get("/tool-usage")
async def get_tool_usage(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get scan type distribution"""
    result = await db.execute(
        select(Scan.scan_type, func.count(Scan.id))
        .group_by(Scan.scan_type)
    )
    rows = result.all()
    
    return {row[0]: row[1] for row in rows}

