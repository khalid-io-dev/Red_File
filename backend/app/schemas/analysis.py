from typing import Any, List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel

class AnalysisBase(BaseModel):
    filename: str
    file_hash_sha256: str

class AnalysisCreate(AnalysisBase):
    md5: str
    file_size: int
    entropy: float
    yara_matches: List[str] = []
    static_features: Dict[str, Any] = {}
    risk_score: float = 0.0

class Analysis(AnalysisBase):
    id: int
    md5: str
    file_size: int
    entropy: float
    yara_matches: List[str]
    static_features: Dict[str, Any]
    risk_score: float
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True
