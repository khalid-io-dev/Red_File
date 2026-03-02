from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from pathlib import Path
import shutil
import hashlib
from typing import List

router = APIRouter()

UPLOAD_DIR = Path("uploads")
MALWARE_DIR = UPLOAD_DIR / "malware"
WORDLIST_DIR = UPLOAD_DIR / "wordlists"

for dir in [UPLOAD_DIR, MALWARE_DIR, WORDLIST_DIR]:
    dir.mkdir(parents=True, exist_ok=True)

def get_file_hash(file_path: Path) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@router.post("/malware")
async def upload_malware(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user)
):
    file_path = MALWARE_DIR / file.filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_hash = get_file_hash(file_path)
    
    return {
        "filename": file.filename,
        "size": file_path.stat().st_size,
        "hash": file_hash,
        "path": str(file_path)
    }

@router.post("/wordlist")
async def upload_wordlist(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user)
):
    if not file.filename.endswith(('.txt', '.lst')):
        raise HTTPException(status_code=400, detail="Only .txt or .lst files allowed")
    
    file_path = WORDLIST_DIR / file.filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    with file_path.open("r") as f:
        line_count = sum(1 for _ in f)
    
    return {
        "filename": file.filename,
        "size": file_path.stat().st_size,
        "lines": line_count,
        "path": str(file_path)
    }

@router.get("/wordlists")
async def list_wordlists(
    current_user: User = Depends(deps.get_current_user)
):
    wordlists = []
    for file_path in WORDLIST_DIR.glob("*.txt"):
        wordlists.append({
            "filename": file_path.name,
            "size": file_path.stat().st_size,
            "path": str(file_path)
        })
    for file_path in WORDLIST_DIR.glob("*.lst"):
        wordlists.append({
            "filename": file_path.name,
            "size": file_path.stat().st_size,
            "path": str(file_path)
        })
    return {"wordlists": wordlists}

@router.get("/malware")
async def list_malware(
    current_user: User = Depends(deps.get_current_user)
):
    malware_files = []
    for file_path in MALWARE_DIR.iterdir():
        if file_path.is_file():
            malware_files.append({
                "filename": file_path.name,
                "size": file_path.stat().st_size,
                "hash": get_file_hash(file_path),
                "path": str(file_path)
            })
    return {"files": malware_files}
