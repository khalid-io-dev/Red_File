from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.v1.api import api_router
from app.api.v1.endpoints import websocket
from app.core.config import settings
from app.db.session import close_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(websocket.router)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await close_db()

@app.get("/")
def root():
    return {"message": "SecureSight API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
