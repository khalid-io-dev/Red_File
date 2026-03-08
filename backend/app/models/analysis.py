from sqlalchemy import Column, Integer, String, Text, Float, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class MalwareAnalysis(Base):
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_hash_sha256 = Column(String(64), index=True, unique=True)
    md5 = Column(String(32))
    file_size = Column(Integer)
    entropy = Column(Float)
    
    # Analysis results
    yara_matches = Column(JSON) # List of rule names
    static_features = Column(JSON) # PE header info, strings, etc.
    risk_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("user.id"))
    
    owner = relationship("User", backref="analyses")
