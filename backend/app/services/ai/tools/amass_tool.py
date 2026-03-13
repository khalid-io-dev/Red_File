from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from app.services.kali_executor import kali_executor
from typing import List

class AmassTool(BaseTool):
    def get_description(self) -> str:
        return "In-depth attack surface mapping and asset discovery"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="domain", type="string", description="Target domain", required=True),
            ToolParameter(name="passive", type="boolean", description="Passive mode", required=False),
        ]
    
    async def execute(self, domain: str, passive: bool = False, **kwargs) -> ToolResult:
        cmd = f"amass enum {'--passive' if passive else ''} -d {domain}"
        result = await kali_executor.execute(cmd, timeout=300)
        return ToolResult(success=True, output=result["stdout"], error=result["stderr"])
