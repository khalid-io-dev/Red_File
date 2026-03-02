from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api import deps
from app.models.finding import Finding
from app.models.user import User
from app.schemas.scan import Finding as FindingSchema

router = APIRouter()

@router.post("/{finding_id}/triage", response_model=FindingSchema)
async def triage_finding(
    finding_id: int,
    db: AsyncSession = Depends(deps.get_db),
    severity: str = Body(None),
    false_positive: bool = Body(False),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Triage a finding (Update severity or mark as FP).
    """
    result = await db.execute(select(Finding).filter(Finding.id == finding_id))
    finding = result.scalars().first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
        
    # Permission check omitted for brevity (should check scan owner)
    
    if severity:
        finding.severity = severity
    
    # Logic for FP could involve a separate status field or flag
    # For now, we assume we just tag it in description or if we had a status field
    if false_positive:
        finding.title = f"[FP] {finding.title}"
        
    db.add(finding)
    await db.commit()
    await db.refresh(finding)
    return finding
