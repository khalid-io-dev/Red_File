from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from app.services.kali_executor import kali_executor
from typing import List

class SherlockTool(BaseTool):
    def get_description(self) -> str:
        return "Hunt down social media accounts by username"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="username", type="string", description="Username to search", required=True),
        ]
    
    async def execute(self, username: str, **kwargs) -> ToolResult:
        cmd = f"sherlock {username} --timeout 60 --print-found"
        result = await kali_executor.execute(cmd, timeout=90)
        return ToolResult(success=True, output=result["stdout"], error=result["stderr"])
