from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from app.services.kali_executor import kali_executor
from typing import List

class MetasploitTool(BaseTool):
    def get_description(self) -> str:
        return "Exploitation framework for penetration testing"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="target", type="string", description="Target IP", required=True),
            ToolParameter(name="exploit", type="string", description="Exploit module", required=True),
        ]
    
    async def execute(self, target: str, exploit: str, **kwargs) -> ToolResult:
        cmd = f"echo 'use {exploit}\nset RHOSTS {target}\ncheck\nexit' | msfconsole -q -x 'exit'"
        result = await kali_executor.execute(cmd, timeout=300)
        return ToolResult(success=True, output=result["stdout"], error=result["stderr"])
