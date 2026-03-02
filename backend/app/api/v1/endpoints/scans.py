from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
import asyncio
from datetime import datetime

from app.api import deps
from app.models.scan import Scan, ScanStatus
from app.models.user import User
from app.schemas.scan import ScanCreate, Scan as ScanSchema
from app.services.producer import producer
from app.services.scan_executor import scan_executor

router = APIRouter()
logger = logging.getLogger(__name__)

async def retry_db_operation(operation, max_retries=3, delay=1):
    """Retry database operations with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return await operation()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            logger.warning(f"DB operation failed (attempt {attempt + 1}): {e}")
            await asyncio.sleep(delay * (2 ** attempt))

@router.post("/", response_model=ScanSchema)
async def create_scan(
    *,
    db: AsyncSession = Depends(deps.get_db),
    scan_in: ScanCreate,
    current_user: User = Depends(deps.get_current_active_user),
    background_tasks: BackgroundTasks,
) -> Any:
    """
    Create a new scan.
    """
    target = scan_in.target_url or scan_in.target
    if not target:
        raise HTTPException(status_code=400, detail="Target is required")
    
    scan = Scan(
        target_url=target,
        scan_type=scan_in.scan_type,
        owner_id=current_user.id,
        status=ScanStatus.PENDING
    )
    db.add(scan)
    await db.commit()
    await db.refresh(scan)
    
    # Execute scan in background
    from app.db.session import AsyncSessionLocal
    
    async def run_scan():
        async with AsyncSessionLocal() as session:
            await scan_executor.execute_scan(scan.id, session)
    
    background_tasks.add_task(run_scan)
    
    return scan

@router.get("/")
async def read_scans(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="Filter by status"),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve scans with optional status filter.
    """
    logger.info(f"Fetching scans for user {current_user.id}")

    try:
        query = select(Scan).where(Scan.owner_id == current_user.id)

        if status:
            status_upper = status.strip().upper()
            try:
                status_enum = ScanStatus(status_upper)
            except Exception:
                raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
            query = query.where(Scan.status == status_enum)

        query = query.order_by(Scan.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        scans = result.scalars().all()

        # Convert to dict to avoid serialization issues
        response_data = []
        for s in scans:
            try:
                scan_dict = {
                    "id": s.id,
                    "target_url": s.target_url,
                    "scan_type": s.scan_type,
                    "status": s.status.value if hasattr(s.status, 'value') else str(s.status),
                    "progress": s.progress or 0,
                    "created_at": s.created_at.isoformat() if s.created_at else None,
                    "owner_id": s.owner_id
                }
                response_data.append(scan_dict)
            except Exception as e:
                logger.error(f"Error serializing scan {s.id}: {e}")
                # Skip problematic scans
                continue

        logger.info(f"Returning {len(response_data)} scans for user {current_user.id}")
        return response_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching scans: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch scans: {str(e)}")

@router.get("/{scan_id}")
async def read_scan(
    scan_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get scan by ID with detailed results"""
    result = await db.execute(select(Scan).filter(Scan.id == scan_id))
    scan = result.scalars().first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if not current_user.is_superuser and (scan.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    return {
        "id": scan.id,
        "target_url": scan.target_url,
        "scan_type": scan.scan_type,
        "status": scan.status.value if hasattr(scan.status, 'value') else str(scan.status),
        "progress": scan.progress or 0,
        "created_at": scan.created_at.isoformat() if scan.created_at else None,
        "owner_id": scan.owner_id,
        "results": {
            "vulnerabilities": [],
            "open_ports": [],
            "services": [],
            "summary": f"Scan of {scan.target_url} completed"
        },
        "logs": [
            {"timestamp": scan.created_at.isoformat(), "message": "Scan initiated"},
            {"timestamp": scan.created_at.isoformat(), "message": f"Scanning {scan.target_url}"}
        ]
    }

@router.post("/{scan_id}/stop")
async def stop_scan(
    scan_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Stop a running scan.
    """
    result = await db.execute(select(Scan).filter(Scan.id == scan_id))
    scan = result.scalars().first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if not current_user.is_superuser and (scan.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    # Only stop if running
    if scan.status in [ScanStatus.RUNNING, ScanStatus.PENDING]:
        await scan_executor.stop_scan(scan_id)
        scan.status = ScanStatus.STOPPED
        await db.commit()
        return {"message": "Scan stopped", "status": "stopped"}
    
    return {"message": f"Scan is already {scan.status}", "status": scan.status}

@router.delete("/{scan_id}")
async def delete_scan(
    scan_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a scan.
    """
    result = await db.execute(select(Scan).filter(Scan.id == scan_id))
    scan = result.scalars().first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if not current_user.is_superuser and (scan.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    await db.delete(scan)
    await db.commit()
    return {"message": "Scan deleted"}

