from typing import Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class ReportRequest(BaseModel):
    scan_id: int
    format: str = "json" # json, pdf

class ReportResponse(BaseModel):
    id: Optional[int] = None
    scan_id: int
    content: str
    generated_at: datetime
