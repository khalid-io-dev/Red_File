from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.session import get_db
from app.models.user import User
from app.models.compliance import ComplianceFramework, ComplianceControl, ComplianceMapping
from app.models.finding import Finding
from app.api.deps import get_current_user
from typing import List

router = APIRouter()

@router.get("/frameworks")
async def list_frameworks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(ComplianceFramework))
    frameworks = result.scalars().all()
    return [{
        "id": f.id,
        "name": f.name,
        "version": f.version,
        "description": f.description
    } for f in frameworks]

@router.get("/frameworks/{framework_id}/controls")
async def list_controls(
    framework_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(ComplianceControl).where(ComplianceControl.framework_id == framework_id)
    )
    controls = result.scalars().all()
    return [{
        "id": c.id,
        "control_id": c.control_id,
        "title": c.title,
        "description": c.description,
        "category": c.category
    } for c in controls]

@router.get("/frameworks/{framework_id}/coverage")
async def get_coverage(
    framework_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get total controls
    total_result = await db.execute(
        select(func.count(ComplianceControl.id))
        .where(ComplianceControl.framework_id == framework_id)
    )
    total = total_result.scalar()
    
    # Get mapped controls
    mapped_result = await db.execute(
        select(func.count(func.distinct(ComplianceMapping.control_id)))
        .join(ComplianceControl)
        .where(ComplianceControl.framework_id == framework_id)
    )
    mapped = mapped_result.scalar()
    
    coverage = (mapped / total * 100) if total > 0 else 0
    
    return {
        "framework_id": framework_id,
        "total_controls": total,
        "mapped_controls": mapped,
        "coverage_percentage": round(coverage, 2),
        "gaps": total - mapped
    }

@router.get("/owasp-top10")
async def get_owasp_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get OWASP framework
    result = await db.execute(
        select(ComplianceFramework).where(ComplianceFramework.name == "OWASP Top 10")
    )
    framework = result.scalar_one_or_none()
    
    if not framework:
        return {"message": "OWASP Top 10 framework not initialized"}
    
    # Get controls with finding counts
    controls_result = await db.execute(
        select(ComplianceControl).where(ComplianceControl.framework_id == framework.id)
    )
    controls = controls_result.scalars().all()
    
    dashboard = []
    for control in controls:
        # Count findings mapped to this control
        count_result = await db.execute(
            select(func.count(ComplianceMapping.id))
            .where(ComplianceMapping.control_id == control.id)
        )
        finding_count = count_result.scalar()
        
        dashboard.append({
            "control_id": control.control_id,
            "title": control.title,
            "category": control.category,
            "finding_count": finding_count,
            "status": "compliant" if finding_count == 0 else "non-compliant"
        })
    
    return {
        "framework": "OWASP Top 10 2021",
        "controls": dashboard
    }
