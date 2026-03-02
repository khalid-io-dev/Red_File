from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from app.services.ai.rag import RAGService
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    k: int = 5

class ReportRequest(BaseModel):
    scan_id: int

class AnalyzeRequest(BaseModel):
    finding_id: int

@router.post("/search")
async def search_similar_findings(
    request: SearchRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    rag = RAGService()
    results = await rag.search_similar(request.query, k=request.k, db=db)
    return {"query": request.query, "results": results}

@router.post("/report")
async def generate_scan_report(
    request: ReportRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    rag = RAGService()
    try:
        report = await rag.generate_report(request.scan_id, db)
        return {"scan_id": request.scan_id, "report": report}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/analyze")
async def analyze_vulnerability(
    request: AnalyzeRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    rag = RAGService()
    try:
        analysis = await rag.analyze_vulnerability(request.finding_id, db)
        return {"finding_id": request.finding_id, "analysis": analysis}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/index")
async def index_findings(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    rag = RAGService()
    count = await rag.index_findings(db)
    return {"indexed_count": count, "message": f"Indexed {count} findings"}
