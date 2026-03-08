from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class ScanStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    STOPPED = "STOPPED"

class Scan(Base):
    __tablename__ = "scan"
    
    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String(500), nullable=False, index=True)
    scan_type = Column(String(50), default="passive", index=True)
    status = Column(SAEnum(ScanStatus), default=ScanStatus.PENDING, index=True)
    progress = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey("user.id"), index=True)
    
    # Lazy loading relationships to prevent eager loading issues
    findings = relationship("Finding", back_populates="scan", lazy="select")
    credentials = relationship("Credential", back_populates="scan", lazy="select")
    owner = relationship("User", lazy="select")
