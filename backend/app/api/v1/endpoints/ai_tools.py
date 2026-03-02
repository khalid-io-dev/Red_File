from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app.models.user import User
from app.services.ai.tools import registry
from pydantic import BaseModel
from typing import Dict, Any, Optional

router = APIRouter()

class ToolExecuteRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

@router.get("/")
async def list_tools(
    current_user: User = Depends(deps.get_current_user)
):
    tools = registry.get_all_tools()
    return {
        "total": len(tools),
        "tools": [
            {
                "name": tool.name,
                "description": tool.get_description(),
                "parameters": [
                    {
                        "name": p.name,
                        "type": p.type,
                        "description": p.description,
                        "required": p.required,
                        "enum": p.enum
                    }
                    for p in tool.get_parameters()
                ]
            }
            for tool in tools
        ]
    }

@router.post("/execute")
async def execute_tool(
    request: ToolExecuteRequest,
    current_user: User = Depends(deps.get_current_user)
):
    tool = registry.get_tool(request.tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool {request.tool_name} not found")
    
    try:
        result = await tool.execute(**request.arguments)
        return {
            "tool": request.tool_name,
            "success": result.success,
            "output": result.output,
            "error": result.error,
            "metadata": result.metadata
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def tools_health(
    current_user: User = Depends(deps.get_current_user)
):
    from app.services.ai.sandbox.docker_sandbox import DockerSandbox
    
    sandbox = DockerSandbox()
    
    return {
        "tools_count": len(registry.get_all_tools()),
        "docker_available": sandbox.is_available(),
        "tools": [tool.name for tool in registry.get_all_tools()]
    }
