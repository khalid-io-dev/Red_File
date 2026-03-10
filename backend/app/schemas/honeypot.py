from typing import Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

class HoneypotLogBase(BaseModel):
    honeypot_name: str
    attacker_ip: str
    port: int
    protocol: str
    payload: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = {}

class HoneypotLogCreate(HoneypotLogBase):
    pass

class HoneypotLog(HoneypotLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class HoneypotInstanceBase(BaseModel):
    name: str
    type: str
    config: Optional[Dict[str, Any]] = None

class HoneypotInstanceCreate(HoneypotInstanceBase):
    pass

class HoneypotInstanceUpdate(BaseModel):
    status: str

class HoneypotInstance(HoneypotInstanceBase):
    id: int
    status: str
    ip_address: Optional[str] = None

    class Config:
        from_attributes = True
