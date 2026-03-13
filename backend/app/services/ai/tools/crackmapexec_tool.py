from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from app.services.kali_executor import kali_executor
from typing import List

class CrackMapExecTool(BaseTool):
    def get_description(self) -> str:
        return "Swiss army knife for pentesting networks"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="target", type="string", description="Target IP or range", required=True),
        ]
    
    async def execute(self, target: str, **kwargs) -> ToolResult:
        cmd = f"crackmapexec smb {target}"
        result = await kali_executor.execute(cmd, timeout=120)
        return ToolResult(success=True, output=result["stdout"], error=result["stderr"])
