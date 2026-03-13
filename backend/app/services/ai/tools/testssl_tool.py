from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from app.services.kali_executor import kali_executor
from typing import List

class TestsslTool(BaseTool):
    def get_description(self) -> str:
        return "Testing TLS/SSL encryption"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="target", type="string", description="Target URL or IP", required=True),
            ToolParameter(name="severity", type="string", description="Severity level", required=False),
        ]
    
    async def execute(self, target: str, severity: str = "HIGH", **kwargs) -> ToolResult:
        cmd = f"testssl.sh --severity {severity} {target}"
        result = await kali_executor.execute(cmd, timeout=120)
        return ToolResult(success=True, output=result["stdout"], error=result["stderr"])
