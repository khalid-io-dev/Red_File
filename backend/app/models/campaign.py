from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class CampaignStatusEnum(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class Campaign(Base):
    __tablename__ = "campaign"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    targets = Column(JSON)
    chain_type = Column(String(50), default="auto")
    status = Column(SQLEnum(CampaignStatusEnum), default=CampaignStatusEnum.PENDING)
    
    progress = Column(Integer, default=0)
    results = Column(JSON)
    extra_data = Column(JSON)
    
    owner_id = Column(Integer, ForeignKey("user.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    owner = relationship("User")
