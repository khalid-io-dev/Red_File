from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.models.user import User
from app.models.payload import Payload
from app.services.ai_payload import ai_payload_generator as payload_generator
from app.services.obfuscation_engine import obfuscation_engine
from app.services.stegano_tool import stegano_tool
from pydantic import BaseModel
from typing import List, Optional
import os

router = APIRouter()

class PayloadCreate(BaseModel):
    name: str
    payload_type: str
    platform: str
    language: str
    lhost: str
    lport: int
    features: Optional[List[str]] = []

# New schema matching frontend PayloadGenerator.tsx request
class PayloadGenerateRequest(BaseModel):
    type: str  # reverse_shell, bind_shell, meterpreter, web_shell
    platform: str
    lhost: str
    lport: str
    encoder: Optional[str] = None
    format: Optional[str] = "exe"
    model: Optional[str] = None  # AI model selection

class ObfuscateRequest(BaseModel):
    code: str
    techniques: List[str]
    language: str = "python"

class EmbedRequest(BaseModel):
    payload_id: int
    embed_type: str  # image, pdf, office

# Map format to language
FORMAT_TO_LANGUAGE = {
    "exe": "c",
    "dll": "c",
    "ps1": "powershell",
    "py": "python",
    "raw": "shellcode"
}

from app.services.ai_payload import ai_payload_generator

@router.get("/models")
async def get_available_models(
    current_user: User = Depends(deps.get_current_user)
):
    """Get list of available AI models for payload generation"""
    models = ai_payload_generator.get_available_models()
    import logging
    logging.info(f"Returning {len(models)} models: {list(models.keys())}")
    return {"models": models}

@router.post("/generate")
async def generate_payload(
    request: PayloadGenerateRequest,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Generate new payload with AI model selection"""
    try:
        language = FORMAT_TO_LANGUAGE.get(request.format, "python")
        lport_int = int(request.lport)
        
        try:
            result = await ai_payload_generator.generate_payload_async(
                payload_type=request.type,
                platform=request.platform,
                language=language,
                lhost=request.lhost,
                lport=lport_int,
                encoder=request.encoder,
                model=request.model
            )
        except Exception as ai_error:
            import logging
            logging.warning(f"AI generation failed: {ai_error}. Falling back.")
            
            if request.type == "reverse_shell":
                result = {"code": payload_generator.generate_reverse_shell(request.lhost, lport_int, request.platform)}
            elif request.type == "bind_shell":
                result = {"code": payload_generator.generate_bind_shell(lport_int, request.platform)}
            elif request.type == "meterpreter":
                result = {"code": payload_generator.generate_reverse_shell(request.lhost, lport_int, "bash")}
            elif request.type == "web_shell":
                result = {"code": payload_generator.generate_web_shell("php")}
            else:
                raise HTTPException(400, f"Invalid payload type: {request.type}")
        
        code = result.get("code", "")
        
        if request.encoder and request.encoder != "none":
            try:
                obfuscated = obfuscation_engine.obfuscate(code, [request.encoder], language)
                code = obfuscated.get("obfuscated_code", code)
            except:
                pass
        
        import uuid
        name = f"payload_{uuid.uuid4().hex[:8]}"
        filename = f"{name}.{request.format}"
        
        try:
            filepath = payload_generator.save_payload(code, filename)
        except:
            os.makedirs("payloads", exist_ok=True)
            filepath = os.path.abspath(f"payloads/{filename}")
            with open(filepath, "w") as f:
                f.write(code)
        
        payload = Payload(
            name=name,
            payload_type=request.type,
            platform=request.platform,
            language=language,
            code=code,
            file_path=filepath,
            lhost=request.lhost,
            lport=lport_int,
            owner_id=current_user.id
        )
        
        db.add(payload)
        await db.commit()
        await db.refresh(payload)
        
        return {
            "id": payload.id,
            "name": payload.name,
            "type": payload.payload_type,
            "platform": payload.platform,
            "code": code,
            "obfuscated_code": code if request.encoder else None,
            "file_path": filepath,
            "model": result.get("model", "standard"),
            "created_at": payload.created_at.isoformat() if payload.created_at else None
        }
    except ValueError:
        raise HTTPException(400, f"Invalid port: {request.lport}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Error: {str(e)}")

@router.post("/obfuscate")
async def obfuscate_payload(
    request: ObfuscateRequest,
    current_user: User = Depends(deps.get_current_user)
):
    """Obfuscate payload code"""
    result = obfuscation_engine.obfuscate(
        request.code, request.techniques, request.language
    )
    return result

@router.post("/embed")
async def embed_payload(
    request: EmbedRequest,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Embed payload in file"""
    # Get payload
    result = await db.execute(select(Payload).filter(Payload.id == request.payload_id))
    payload = result.scalar_one_or_none()
    
    if not payload:
        raise HTTPException(404, "Payload not found")
    
    # Save uploaded file
    upload_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(upload_path, "wb") as f:
        f.write(await file.read())
    
    # Embed payload
    if request.embed_type == "image":
        result = stegano_tool.embed_in_image(payload.code, upload_path)
    elif request.embed_type == "pdf":
        result = stegano_tool.embed_in_pdf(payload.code, upload_path)
    else:
        result = stegano_tool.embed_in_office(payload.code, upload_path)
    
    # Update payload record
    payload.embedded_file_path = result.get("output_path")
    await db.commit()
    
    return result

@router.get("/")
async def list_payloads(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """List user's payloads"""
    result = await db.execute(
        select(Payload).filter(Payload.owner_id == current_user.id)
    )
    payloads = result.scalars().all()
    
    return {
        "payloads": [
            {
                "id": p.id,
                "name": p.name,
                "type": p.payload_type,
                "platform": p.platform,
                "language": p.language,
                "created_at": p.created_at.isoformat()
            }
            for p in payloads
        ]
    }

@router.get("/{payload_id}/download")
async def download_payload(
    payload_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Download payload file"""
    result = await db.execute(select(Payload).filter(Payload.id == payload_id))
    payload = result.scalar_one_or_none()
    
    if not payload or payload.owner_id != current_user.id:
        raise HTTPException(404, "Payload not found")
    
    if not os.path.exists(payload.file_path):
        raise HTTPException(404, "File not found")
    
    return FileResponse(payload.file_path, filename=os.path.basename(payload.file_path))

@router.post("/test-evasion")
async def test_evasion(
    payload_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Test payload AV evasion"""
    result = await db.execute(select(Payload).filter(Payload.id == payload_id))
    payload = result.scalar_one_or_none()
    
    if not payload:
        raise HTTPException(404, "Payload not found")
    
    test_result = payload_generator.test_av_evasion(payload.file_path)
    
    # Update payload record
    payload.detection_rate = test_result["detection_rate"]
    payload.tested_at = test_result["tested_at"]
    await db.commit()
    
    return test_result
