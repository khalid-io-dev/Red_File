from app.services.kali_executor import kali_executor
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class CommixTool(BaseTool):
    def get_description(self) -> str:
        return "Command injection exploitation using Commix in Kali Linux"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="url", type="string", description="Target URL"),
            ToolParameter(name="data", type="string", description="POST data", required=False)
        ]
    
    async def execute(self, url: str, data: str = None) -> ToolResult:
        try:
            command = f"commix --url='{url}' --batch"
            if data:
                command += f" --data='{data}'"
            
            result = await kali_executor.execute(command, timeout=600)
            
            vulnerable = 'vulnerable' in result['output'].lower()
            
            summary = f"""
=== COMMIX COMMAND INJECTION ===
Target: {url}
Vulnerable: {'YES' if vulnerable else 'NO'}

{result['output']}
"""
            return ToolResult(success=result['success'], output=summary, error=result['error'])
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))
