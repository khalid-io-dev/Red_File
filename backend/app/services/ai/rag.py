from typing import List, Dict, Any
from .faiss_service import FAISSService
from .embedding_service import EmbeddingService
from .llm_service import OllamaLLMService
from .prompts.system import REPORT_GENERATOR_PROMPT, VULNERABILITY_ANALYZER_PROMPT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.finding import Finding
from app.models.scan import Scan
import json

class RAGService:
    def __init__(self, index_path: str = "data/findings"):
        self.embedder = EmbeddingService()
        self.faiss = FAISSService(dimension=384, index_path=index_path)
        self.llm = OllamaLLMService()
    
    async def index_findings(self, db: AsyncSession):
        result = await db.execute(select(Finding))
        findings = result.scalars().all()
        
        if not findings:
            return 0
        
        texts = [f"{f.title}: {f.description}" for f in findings]
        ids = [f.id for f in findings]
        
        embeddings = self.embedder.embed_documents(texts)
        self.faiss.add(embeddings, ids)
        self.faiss.save("data/findings")
        
        return len(findings)
    
    async def search_similar(self, query: str, k: int = 5, db: AsyncSession = None) -> List[Dict[str, Any]]:
        query_embedding = self.embedder.embed(query)
        results = self.faiss.search(query_embedding, k=k)
        
        if not db:
            return [{"id": id, "distance": dist} for id, dist in results]
        
        similar_findings = []
        for finding_id, distance in results:
            result = await db.execute(select(Finding).where(Finding.id == finding_id))
            finding = result.scalar_one_or_none()
            if finding:
                similar_findings.append({
                    "id": finding.id,
                    "title": finding.title,
                    "description": finding.description,
                    "severity": finding.severity,
                    "distance": distance
                })
        
        return similar_findings
    
    async def generate_report(self, scan_id: int, db: AsyncSession) -> str:
        result = await db.execute(
            select(Scan).where(Scan.id == scan_id)
        )
        scan = result.scalar_one_or_none()
        
        if not scan:
            raise ValueError(f"Scan {scan_id} not found")
        
        findings_result = await db.execute(
            select(Finding).where(Finding.scan_id == scan_id)
        )
        findings = findings_result.scalars().all()
        
        findings_data = [
            {
                "title": f.title,
                "description": f.description,
                "severity": f.severity,
                "cvss_score": f.cvss_score,
                "remediation": f.remediation
            }
            for f in findings
        ]
        
        from .report_generator import ReportGenerator
        generator = ReportGenerator()
        
        scan_data = {
            "target": scan.target,
            "scan_type": scan.scan_type,
            "status": scan.status
        }
        
        report = await generator.generate_executive_summary(scan_data, findings_data)
        return report
    
    async def analyze_vulnerability(self, finding_id: int, db: AsyncSession) -> str:
        result = await db.execute(
            select(Finding).where(Finding.id == finding_id)
        )
        finding = result.scalar_one_or_none()
        
        if not finding:
            raise ValueError(f"Finding {finding_id} not found")
        
        similar = await self.search_similar(finding.description, k=3, db=db)
        
        context = {
            "finding": {
                "title": finding.title,
                "description": finding.description,
                "severity": finding.severity,
                "cvss_score": finding.cvss_score
            },
            "similar_findings": similar
        }
        
        prompt = f"""Analyze this vulnerability in detail:

{json.dumps(context, indent=2)}

Provide:
1. True severity assessment
2. Exploitation difficulty and likelihood
3. Business impact analysis
4. Specific remediation steps
5. Detection and monitoring recommendations"""
        
        analysis = await self.llm.generate(prompt, system=VULNERABILITY_ANALYZER_PROMPT, max_tokens=2048)
        return analysis
    
    def _get_severity_breakdown(self, findings: List[Finding]) -> Dict[str, int]:
        breakdown = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for f in findings:
            severity = f.severity.lower() if f.severity else "info"
            if severity in breakdown:
                breakdown[severity] += 1
        return breakdown
