from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from app.services.kali_executor import kali_executor
from typing import List

class Sublist3rTool(BaseTool):
    def get_description(self) -> str:
        return "Fast subdomains enumeration tool"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="domain", type="string", description="Target domain", required=True),
        ]
    
    async def execute(self, domain: str, **kwargs) -> ToolResult:
        cmd = f"sublist3r -d {domain}"
        result = await kali_executor.execute(cmd, timeout=180)
        return ToolResult(success=True, output=result["stdout"], error=result["stderr"])
