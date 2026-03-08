from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class ReportTypeEnum(str, enum.Enum):
    EXECUTIVE = "executive"
    TECHNICAL = "technical"
    COMPLIANCE = "compliance"

class ReportFormatEnum(str, enum.Enum):
    JSON = "json"
    MARKDOWN = "markdown"
    PDF = "pdf"
    HTML = "html"

class Report(Base):
    __tablename__ = "report"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    report_type = Column(SQLEnum(ReportTypeEnum), default=ReportTypeEnum.TECHNICAL)
    format = Column(SQLEnum(ReportFormatEnum), default=ReportFormatEnum.JSON)
    
    content = Column(Text)
    file_path = Column(String(500))
    
    scan_id = Column(Integer, ForeignKey("scan.id"), nullable=True)
    campaign_id = Column(Integer, ForeignKey("campaign.id"), nullable=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    scan = relationship("Scan")
    campaign = relationship("Campaign")
    owner = relationship("User")
