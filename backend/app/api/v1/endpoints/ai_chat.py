from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
import logging

from app.api import deps
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage
from app.services.ai_chat_service import ai_chat_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/models")
async def get_models(current_user: User = Depends(deps.get_current_active_user)):
    """Get available AI models"""
    return ai_chat_service.get_available_models()

@router.post("/sessions")
async def create_session(
    payload: dict = Body(...),
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Create new chat session"""
    title = payload.get("title", "New Chat")
    model_name = payload.get("model", "qwen2.5-coder:7b-instruct")
    
    session = ChatSession(
        user_id=current_user.id,
        title=title,
        model_name=model_name
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    
    return {
        "id": session.id,
        "title": session.title,
        "model_name": session.model_name,
        "created_at": session.created_at.isoformat()
    }

@router.get("/sessions")
async def get_sessions(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get user's chat sessions"""
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == current_user.id)
        .order_by(desc(ChatSession.updated_at))
        .limit(50)
    )
    sessions = result.scalars().all()
    
    return [
        {
            "id": s.id,
            "title": s.title,
            "model_name": s.model_name,
            "created_at": s.created_at.isoformat(),
            "updated_at": s.updated_at.isoformat()
        }
        for s in sessions
    ]

@router.get("/sessions/{session_id}/messages")
async def get_messages(
    session_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Get messages for a chat session"""
    # Verify session ownership
    session_result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id
        )
    )
    session = session_result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get messages
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    )
    messages = result.scalars().all()
    
    return {
        "session": {
            "id": session.id,
            "title": session.title,
            "model_name": session.model_name
        },
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "enhanced_prompt": m.enhanced_prompt,
                "created_at": m.created_at.isoformat()
            }
            for m in messages
        ]
    }

@router.post("/sessions/{session_id}/chat")
async def send_message(
    session_id: int,
    payload: dict = Body(...),
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Send message and get AI response"""
    message = payload.get("message", "")
    if not message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Verify session ownership
    session_result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id
        )
    )
    session = session_result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Enhance prompt
    enhanced_prompt = await ai_chat_service.enhance_prompt(message)
    
    # Save user message
    user_message = ChatMessage(
        session_id=session_id,
        role="user",
        content=message,
        enhanced_prompt=enhanced_prompt if enhanced_prompt != message else None
    )
    db.add(user_message)
    
    # Get conversation history
    history_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
        .limit(20)  # Last 20 messages for context
    )
    history = history_result.scalars().all()
    
    # Build messages for AI
    messages = [{"role": msg.role, "content": msg.content} for msg in history]
    messages.append({"role": "user", "content": message})
    
    # Get AI response
    ai_response = await ai_chat_service.chat_with_model(
        session.model_name, 
        messages, 
        enhanced_prompt
    )
    
    # Save AI response
    ai_message = ChatMessage(
        session_id=session_id,
        role="assistant",
        content=ai_response
    )
    db.add(ai_message)
    
    # Update session timestamp
    session.updated_at = user_message.created_at
    
    await db.commit()
    await db.refresh(user_message)
    await db.refresh(ai_message)
    
    return {
        "user_message": {
            "id": user_message.id,
            "role": "user",
            "content": message,
            "enhanced_prompt": enhanced_prompt,
            "created_at": user_message.created_at.isoformat()
        },
        "ai_response": {
            "id": ai_message.id,
            "role": "assistant", 
            "content": ai_response,
            "created_at": ai_message.created_at.isoformat()
        }
    }

@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Delete chat session"""
    result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id
        )
    )
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    await db.delete(session)
    await db.commit()
    
    return {"message": "Session deleted"}