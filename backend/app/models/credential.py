from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Credential(Base):
    __tablename__ = "credential"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    password = Column(Text, nullable=False)
    hash_value = Column(Text)
    
    service = Column(String(100))
    protocol = Column(String(50))
    port = Column(Integer)
    target = Column(String(255))
    
    source_tool = Column(String(100))
    is_valid = Column(Boolean, default=False)
    tested_at = Column(DateTime, nullable=True)
    
    scan_id = Column(Integer, ForeignKey("scan.id"), nullable=True)
    campaign_id = Column(String(100), nullable=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    scan = relationship("Scan", back_populates="credentials")
    owner = relationship("User")
