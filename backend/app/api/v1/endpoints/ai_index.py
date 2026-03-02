from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from app.services.ai.indexer import FindingIndexer
from pydantic import BaseModel

router = APIRouter()

class IndexResponse(BaseModel):
    indexed_count: int
    message: str

@router.post("/index", response_model=IndexResponse)
async def index_all_findings(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin only")
    
    indexer = FindingIndexer()
    count = await indexer.index_all(db)
    
    return IndexResponse(
        indexed_count=count,
        message=f"Successfully indexed {count} findings"
    )

@router.get("/status")
async def index_status(
    current_user: User = Depends(deps.get_current_user)
):
    from app.services.ai.faiss_service import FAISSService
    
    try:
        faiss = FAISSService(dimension=384, index_path="data/findings")
        return {
            "indexed": True,
            "total_vectors": faiss.size(),
            "dimension": faiss.dimension
        }
    except:
        return {
            "indexed": False,
            "total_vectors": 0,
            "dimension": 384
        }
