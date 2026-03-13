from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from app.services.kali_executor import kali_executor
from typing import List

class ResponderTool(BaseTool):
    def get_description(self) -> str:
        return "LLMNR, NBT-NS and MDNS poisoner"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="interface", type="string", description="Network interface", required=True),
        ]
    
    async def execute(self, interface: str, **kwargs) -> ToolResult:
        cmd = f"responder -I {interface} -w -v"
        result = await kali_executor.execute(cmd, timeout=60)
        return ToolResult(success=True, output=result["stdout"], error=result["stderr"])
