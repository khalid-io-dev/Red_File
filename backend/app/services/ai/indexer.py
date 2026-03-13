from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.finding import Finding
from .faiss_service import FAISSService
from .embedding_service import EmbeddingService
import logging

logger = logging.getLogger(__name__)

class FindingIndexer:
    def __init__(self, index_path: str = "data/findings"):
        self.embedder = EmbeddingService()
        self.faiss = FAISSService(dimension=384, index_path=index_path)
        self.batch_size = 100
    
    async def index_all(self, db: AsyncSession) -> int:
        result = await db.execute(select(Finding))
        findings = result.scalars().all()
        
        if not findings:
            logger.info("No findings to index")
            return 0
        
        texts = [f"{f.title}: {f.description}" for f in findings]
        ids = [f.id for f in findings]
        
        total_indexed = 0
        for i in range(0, len(texts), self.batch_size):
            batch_texts = texts[i:i + self.batch_size]
            batch_ids = ids[i:i + self.batch_size]
            
            embeddings = self.embedder.embed_documents(batch_texts)
            self.faiss.add(embeddings, batch_ids)
            total_indexed += len(batch_ids)
            
            logger.info(f"Indexed {total_indexed}/{len(findings)} findings")
        
        self.faiss.save("data/findings")
        logger.info(f"Index saved with {total_indexed} findings")
        return total_indexed
    
    async def index_incremental(self, db: AsyncSession, finding_ids: List[int]) -> int:
        if not finding_ids:
            return 0
        
        result = await db.execute(
            select(Finding).where(Finding.id.in_(finding_ids))
        )
        findings = result.scalars().all()
        
        texts = [f"{f.title}: {f.description}" for f in findings]
        ids = [f.id for f in findings]
        
        embeddings = self.embedder.embed_documents(texts)
        self.faiss.add(embeddings, ids)
        self.faiss.save("data/findings")
        
        logger.info(f"Incrementally indexed {len(findings)} findings")
        return len(findings)
