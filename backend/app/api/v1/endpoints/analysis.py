from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select

from app.api import deps
from app.models.analysis import MalwareAnalysis
from app.models.user import User
from app.services.analyzer import analyzer
from pydantic import BaseModel

router = APIRouter()


class AnalysisResult(BaseModel):
    malicious: bool
    score: int
    risk_score: float
    signatures: List[str] = []
    indicators: List[Any] = []


class AnalysisOut(BaseModel):
    id: int
    file_name: str
    file_hash: str
    analysis_type: str
    status: str
    results: AnalysisResult
    created_at: datetime


class HashAnalyzeRequest(BaseModel):
    hash: str


def _to_frontend_result(analysis: MalwareAnalysis) -> AnalysisResult:
    risk_score = float(analysis.risk_score or 0)
    score = int(round(risk_score * 10))
    malicious = risk_score >= 7
    signatures = analysis.yara_matches or []
    return AnalysisResult(
        malicious=malicious,
        score=score,
        risk_score=risk_score,
        signatures=signatures,
        indicators=[],
    )


def _to_frontend_analysis(analysis: MalwareAnalysis, analysis_type: str = "static") -> AnalysisOut:
    return AnalysisOut(
        id=analysis.id,
        file_name=analysis.filename,
        file_hash=analysis.file_hash_sha256,
        analysis_type=analysis_type,
        status="completed",
        results=_to_frontend_result(analysis),
        created_at=analysis.created_at,
    )

@router.post("/upload", response_model=AnalysisOut)
async def upload_file(
    *,
    db: AsyncSession = Depends(deps.get_db),
    file: UploadFile = File(...),
    analysis_type: str = Form("static"),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Upload file for static analysis.
    """
    contents = await file.read()
    
    # Perform analysis
    result = analyzer.analyze(contents, file.filename)
    
    # Check if analysis exists (hash check)
    existing = await db.execute(select(MalwareAnalysis).filter(MalwareAnalysis.file_hash_sha256 == result["sha256"]))
    if existing.scalars().first():
        # Ideally return existing or update, for now just create new entry or return existing logic
        # For simplicity, create new entry but maybe handle unique constraint error or check first
        # We will create new for now but uniqueness on schema might block.
        # Let's simple check:
        pass

    db_obj = MalwareAnalysis(
        filename=result["filename"],
        file_hash_sha256=result["sha256"],
        md5=result["md5"],
        file_size=result["file_size"],
        entropy=result["entropy"],
        yara_matches=result["yara_matches"],
        static_features=result["static_features"],
        risk_score=result["risk_score"],
        owner_id=current_user.id
    )
    
    try:
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
    except Exception:
        await db.rollback()
        # Fallback to fetching existing if race condition or unique violation
        existing = await db.execute(select(MalwareAnalysis).filter(MalwareAnalysis.file_hash_sha256 == result["sha256"]))
        db_obj = existing.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=500, detail="Analysis failed to save")
        
    return _to_frontend_analysis(db_obj, analysis_type=analysis_type)


@router.get("/", response_model=List[AnalysisOut])
async def list_analyses(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(
        select(MalwareAnalysis)
        .where(MalwareAnalysis.owner_id == current_user.id)
        .order_by(MalwareAnalysis.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    analyses = result.scalars().all()
    return [_to_frontend_analysis(a, analysis_type="static") for a in analyses]

@router.get("/{analysis_id}", response_model=AnalysisOut)
async def read_analysis(
    analysis_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get analysis by ID.
    """
    result = await db.execute(select(MalwareAnalysis).filter(MalwareAnalysis.id == analysis_id))
    analysis = result.scalars().first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    if analysis.owner_id != current_user.id and not getattr(current_user, "is_superuser", False):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return _to_frontend_analysis(analysis, analysis_type="static")


@router.post("/hash", response_model=AnalysisResult)
async def analyze_hash(
    request: HashAnalyzeRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    hash_value = request.hash.strip()
    if not hash_value:
        raise HTTPException(status_code=400, detail="Hash is required")

    result = await db.execute(
        select(MalwareAnalysis).where(
            MalwareAnalysis.owner_id == current_user.id,
            or_(
                MalwareAnalysis.file_hash_sha256 == hash_value,
                MalwareAnalysis.md5 == hash_value,
            ),
        )
    )
    analysis = result.scalars().first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return _to_frontend_result(analysis)
