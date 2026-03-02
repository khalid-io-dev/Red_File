from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.services.websocket_manager import websocket_manager as manager
import jwt
from app.core.config import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

async def get_user_from_token(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        logger.info(f"Token decoded successfully, user_id: {user_id}")
        return int(user_id) if user_id else None
    except Exception as e:
        logger.error(f"Token decode failed: {e}")
        return None

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    logger.info(f"WebSocket connection attempt with token: {token[:20]}...")
    user_id = await get_user_from_token(token)
    
    if not user_id:
        logger.warning("Invalid token, rejecting connection")
        await websocket.accept()
        await websocket.close(code=4001)
        return
    
    logger.info(f"User {user_id} connecting to WebSocket")
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("action") == "subscribe":
                topic = data.get("topic", "default")
                await manager.subscribe(websocket, topic)
                await websocket.send_json({"type": "subscribed", "topic": topic})
            
            elif data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    
    except WebSocketDisconnect:
        logger.info(f"User {user_id} disconnected")
        manager.disconnect(websocket)

@router.websocket("/ws/scan/{scan_id}")
async def scan_websocket(websocket: WebSocket, scan_id: int, token: str = Query(...)):
    user_id = await get_user_from_token(token)
    if not user_id:
        await websocket.accept()
        await websocket.close(code=4001)
        return
    
    room = f"scan_{scan_id}"
    await manager.connect(websocket)
    await manager.subscribe(websocket, room)
    
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.websocket("/ws/campaign/{campaign_id}")
async def campaign_websocket(websocket: WebSocket, campaign_id: int, token: str = Query(...)):
    user_id = await get_user_from_token(token)
    if not user_id:
        await websocket.accept()
        await websocket.close(code=4001)
        return
    
    room = f"campaign_{campaign_id}"
    await manager.connect(websocket)
    await manager.subscribe(websocket, room)
    
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
