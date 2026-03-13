from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from app.services.kali_executor import kali_executor
from typing import List

class HashcatTool(BaseTool):
    def get_description(self) -> str:
        return "Advanced password recovery using GPU"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="hash_file", type="string", description="Hash file path", required=True),
        ]
    
    async def execute(self, hash_file: str, **kwargs) -> ToolResult:
        cmd = f"hashcat -m 0 -a 0 {hash_file} /usr/share/wordlists/rockyou.txt --force"
        result = await kali_executor.execute(cmd, timeout=300)
        return ToolResult(success=True, output=result["stdout"], error=result["stderr"])
