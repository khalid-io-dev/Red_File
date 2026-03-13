from app.services.kali_executor import kali_executor
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class MasscanTool(BaseTool):
    def get_description(self) -> str:
        return "Ultra-fast port scanner using Masscan in Kali Linux"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="target", type="string", description="Target IP or CIDR range"),
            ToolParameter(name="ports", type="string", description="Port range (e.g., 1-65535)", required=False),
            ToolParameter(name="rate", type="string", description="Packets per second", required=False)
        ]
    
    async def execute(self, target: str, ports: str = "1-10000", rate: str = "1000") -> ToolResult:
        try:
            command = f"masscan {target} -p{ports} --rate={rate}"
            result = await kali_executor.execute(command, timeout=600, sudo=True)
            
            open_ports = result['output'].count('open')
            
            summary = f"""
=== MASSCAN RESULTS ===
Target: {target}
Ports scanned: {ports}
Open ports: {open_ports}

{result['output']}
"""
            return ToolResult(success=result['success'], output=summary, error=result['error'])
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))
