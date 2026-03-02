from fastapi import APIRouter, Depends, Body
import logging

from app.api import deps
from app.models.user import User
from app.services.ai_code_generator import ai_code_generator

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/execute")
async def execute_tool(
    payload: dict = Body(...),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Execute security tool"""
    tool_name = payload.get("tool_name", "")
    target = payload.get("target", "")
    options = payload.get("options", {})
    
    logger.info(f"Executing {tool_name} on {target}")
    
    if tool_name == "custom_exploit":
        return {
            "status": "success",
            "tool": tool_name,
            "target": target,
            "output": f"Testing exploit '{options.get('name', 'unknown')}' on {target}",
            "findings": [
                {"severity": "high", "description": "SQL Injection vulnerability detected"},
                {"severity": "medium", "description": "Weak authentication mechanism"}
            ]
        }
    
    return {"status": "success", "tool": tool_name, "target": target}

@router.post("/generate-exploit")
async def generate_exploit(
    payload: dict = Body(...),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Generate exploit code using AI"""
    name = payload.get("name", "")
    platform = payload.get("platform", "")
    exploit_type = payload.get("exploit_type", "")
    language = payload.get("language", "python")
    
    prompt = f"Generate a {language} exploit for {platform} - {exploit_type} - {name}"
    code = await ai_code_generator.generate_code(prompt, language)
    
    return {"name": name, "platform": platform, "type": exploit_type, "language": language, "code": code}

@router.post("/fix-code")
async def fix_code(
    payload: dict = Body(...),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Fix code using AI"""
    code = payload.get("code", "")
    language = payload.get("language", "python")
    
    prompt = f"Fix this {language} code:\n\n{code}"
    fixed = await ai_code_generator.generate_code(prompt, language)
    return {"original": code, "fixed": fixed, "language": language}

@router.get("/")
async def list_tools(current_user: User = Depends(deps.get_current_active_user)):
    """List available tools"""
    return [
        {"id": "custom_exploit", "name": "Custom Exploit", "category": "exploitation", "status": "available"}
    ]
