from app.services.kali_executor import kali_executor
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class Enum4linuxTool(BaseTool):
    def get_description(self) -> str:
        return "SMB/Windows enumeration using Enum4linux in Kali Linux"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="target", type="string", description="Target IP address")
        ]
    
    async def execute(self, target: str) -> ToolResult:
        try:
            command = f"enum4linux -a {target}"
            result = await kali_executor.execute(command, timeout=300)
            
            users = result['output'].count('user:')
            shares = result['output'].count('Sharename')
            
            summary = f"""
=== ENUM4LINUX SMB ENUMERATION ===
Target: {target}
Users found: {users}
Shares found: {shares}

{result['output'][:2000]}
"""
            return ToolResult(success=result['success'], output=summary, error=result['error'])
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))
