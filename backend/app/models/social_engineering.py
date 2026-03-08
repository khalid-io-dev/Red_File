from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class SEStatusEnum(str, enum.Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"

class SECampaign(Base):
    __tablename__ = "se_campaign"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    target_email = Column(String(255))
    target_name = Column(String(255))
    target_company = Column(String(255))
    
    target_info = Column(JSON)  # OSINT data
    phishing_template = Column(Text)
    payload_id = Column(Integer, ForeignKey("payload.id"))
    
    tracking_link = Column(String(500))
    email_opened = Column(Boolean, default=False)
    link_clicked = Column(Boolean, default=False)
    opened_at = Column(DateTime)
    clicked_at = Column(DateTime)
    
    credentials_captured = Column(JSON)
    status = Column(SQLEnum(SEStatusEnum), default=SEStatusEnum.PLANNING)
    
    owner_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User")
    payload = relationship("Payload")
