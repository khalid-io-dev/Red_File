from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class SeverityEnum(str, enum.Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"

class StatusEnum(str, enum.Enum):
    NEW = "new"
    CONFIRMED = "confirmed"
    FALSE_POSITIVE = "false_positive"
    FIXED = "fixed"
    IGNORED = "ignored"

class Finding(Base):
    __tablename__ = "finding"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(SQLEnum(SeverityEnum), default=SeverityEnum.MEDIUM)
    status = Column(SQLEnum(StatusEnum), default=StatusEnum.NEW)
    
    target = Column(String(255))
    tool = Column(String(100))
    cve_id = Column(String(50))
    cvss_score = Column(String(10))
    
    evidence = Column(Text)
    remediation = Column(Text)
    references = Column(Text)
    
    scan_id = Column(Integer, ForeignKey("scan.id"), nullable=True)
    campaign_id = Column(String(100), nullable=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    scan = relationship("Scan", back_populates="findings")
    owner = relationship("User")
