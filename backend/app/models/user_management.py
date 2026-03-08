from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"

class UserActivity(Base):
    __tablename__ = "user_activity"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(String(100))
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

class Team(Base):
    __tablename__ = "team"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    owner_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class TeamMember(Base):
    __tablename__ = "team_member"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    role = Column(String(50), default="member")
    joined_at = Column(DateTime, default=datetime.utcnow)
