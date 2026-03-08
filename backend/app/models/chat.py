from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class ChatSession(Base):
    __tablename__ = "chat_session"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    title = Column(String(200), default="New Chat")
    model_name = Column(String(100), default="qwen2.5-coder:7b")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    user = relationship("User")

class ChatMessage(Base):
    __tablename__ = "chat_message"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_session.id"), index=True)
    role = Column(String(20))  # "user" or "assistant"
    content = Column(Text)
    enhanced_prompt = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("ChatSession", back_populates="messages")