from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from app.db.session import get_db
from app.models.user import User
from app.models.finding import Finding, SeverityEnum, StatusEnum
from app.api.deps import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class FindingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    severity: SeverityEnum
    target: str
    tool: str
    evidence: Optional[str] = None
    remediation: Optional[str] = None
    cve_id: Optional[str] = None
    cvss_score: Optional[str] = None
    scan_id: Optional[int] = None
    campaign_id: Optional[str] = None

@router.get("/")
async def list_findings(
    severity: Optional[str] = None,
    target: Optional[str] = None,
    tool: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Finding).where(Finding.owner_id == current_user.id)
    
    if severity:
        query = query.where(Finding.severity == severity)
    if target:
        query = query.where(Finding.target.contains(target))
    if tool:
        query = query.where(Finding.tool == tool)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    findings = result.scalars().all()
    
    return [{
        "id": f.id,
        "title": f.title,
        "description": f.description,
        "severity": f.severity.value,
        "status": f.status.value,
        "target": f.target,
        "tool": f.tool,
        "evidence": f.evidence,
        "cvss_score": f.cvss_score,
        "cve_id": f.cve_id,
        "created_at": f.created_at.isoformat(),
    } for f in findings]

@router.post("/")
async def create_finding(
    finding: FindingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_finding = Finding(
        **finding.dict(),
        owner_id=current_user.id
    )
    db.add(db_finding)
    await db.commit()
    await db.refresh(db_finding)
    return {"id": db_finding.id, "message": "Finding created"}

@router.get("/{finding_id}")
async def get_finding(
    finding_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Finding).where(Finding.id == finding_id, Finding.owner_id == current_user.id)
    )
    finding = result.scalar_one_or_none()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    return {
        "id": finding.id,
        "title": finding.title,
        "description": finding.description,
        "severity": finding.severity.value,
        "status": finding.status.value,
        "target": finding.target,
        "tool": finding.tool,
        "evidence": finding.evidence,
        "remediation": finding.remediation,
        "cvss_score": finding.cvss_score,
        "cve_id": finding.cve_id,
    }

@router.get("/stats/summary")
async def get_findings_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(func.count(Finding.id)).where(Finding.owner_id == current_user.id)
    )
    total = result.scalar()
    
    severity_counts = {}
    for severity in SeverityEnum:
        result = await db.execute(
            select(func.count(Finding.id)).where(
                Finding.owner_id == current_user.id,
                Finding.severity == severity
            )
        )
        severity_counts[severity.value.lower()] = result.scalar()
    
    return {
        "total": total,
        **severity_counts
    }
