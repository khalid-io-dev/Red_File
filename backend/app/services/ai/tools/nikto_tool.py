from app.services.kali_executor import kali_executor
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class NiktoTool(BaseTool):
    def get_description(self) -> str:
        return "Web server vulnerability scanner using Nikto in Kali Linux"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="host",
                type="string",
                description="Target host or URL"
            ),
            ToolParameter(
                name="port",
                type="string",
                description="Port to scan",
                required=False
            )
        ]
    
    async def execute(self, host: str, port: str = "80") -> ToolResult:
        try:
            command = f"nikto -h {host} -p {port} -C all"
            
            self.logger.info(f"Executing: {command}")
            result = await kali_executor.execute(command, timeout=600)
            
            # Parse vulnerabilities
            output = result['output']
            vuln_count = output.count('OSVDB-')
            
            summary = f"""
=== NIKTO WEB SCAN RESULTS ===
Target: {host}:{port}
Vulnerabilities found: {vuln_count}

{output}
"""
            
            return ToolResult(
                success=result['success'],
                output=summary,
                error=result['error']
            )
        except Exception as e:
            self.logger.error(f"Nikto failed: {e}")
            return ToolResult(success=False, output="", error=str(e))
