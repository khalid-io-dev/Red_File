from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, field_validator, model_validator
from app.models.scan import ScanStatus

class FindingBase(BaseModel):
    title: str
    severity: str
    description: Optional[str] = None
    url: Optional[str] = None

class FindingCreate(FindingBase):
    evidence: Optional[str] = None

class Finding(FindingBase):
    id: int
    scan_id: int

    class Config:
        from_attributes = True

class ScanBase(BaseModel):
    target_url: Optional[str] = None
    target: Optional[str] = None  # Accept 'target' from frontend
    scan_type: Optional[str] = "passive"
    tools: Optional[List[str]] = []
    
    @model_validator(mode='before')
    @classmethod
    def normalize_target(cls, data):
        """Accept either 'target' or 'target_url' from frontend"""
        if isinstance(data, dict):
            # If target is provided but target_url is not, use target as target_url
            if data.get('target') and not data.get('target_url'):
                data['target_url'] = data['target']
            elif data.get('target_url') and not data.get('target'):
                data['target'] = data['target_url']
        return data

class ScanCreate(ScanBase):
    @field_validator('target_url', mode='before')
    @classmethod
    def validate_target(cls, v, info):
        """Ensure we have a valid target"""
        if not v:
            # Try to get from 'target' field
            target = info.data.get('target') if hasattr(info, 'data') else None
            if target:
                return target
        return v

class ScanUpdate(BaseModel):
    status: Optional[ScanStatus] = None

class Scan(ScanBase):
    id: int
    status: ScanStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    owner_id: int
    progress: Optional[int] = 0
    findings_count: Optional[int] = 0
    credentials_count: Optional[int] = 0

    class Config:
        from_attributes = True
