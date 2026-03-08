from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from app.db.base_class import Base

class HoneypotLog(Base):
    __tablename__ = "honeypot_log"
    
    id = Column(Integer, primary_key=True, index=True)
    honeypot_name = Column(String(255), index=True)
    attacker_ip = Column(String(50), index=True)
    port = Column(Integer)
    protocol = Column(String(50))
    payload = Column(String(1000), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class HoneypotInstance(Base):
    __tablename__ = "honeypot_instance"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    honeypot_type = Column(String(100))
    status = Column(String(50), default="stopped")
    created_at = Column(DateTime, default=datetime.utcnow)
