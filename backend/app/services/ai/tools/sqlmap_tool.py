from app.services.kali_executor import kali_executor
import json
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class SQLMapTool(BaseTool):
    def get_description(self) -> str:
        return "Test web applications for SQL injection vulnerabilities using sqlmap in Kali Linux"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="url",
                type="string",
                description="Target URL to test"
            ),
            ToolParameter(
                name="data",
                type="string",
                description="POST data",
                required=False
            )
        ]
    
    async def execute(self, url: str, data: str = None) -> ToolResult:
        try:
            command = f"sqlmap -u '{url}' --batch --random-agent --level=5 --risk=3"
            
            if data:
                command += f" --data='{data}'"
            
            self.logger.info(f"Executing: {command}")
            result = await kali_executor.execute(command, timeout=600)
            
            # Parse sqlmap output for vulnerabilities
            output = result['output']
            vulnerable = False
            vuln_type = "None"
            
            if 'is vulnerable' in output.lower():
                vulnerable = True
                if 'boolean-based blind' in output.lower():
                    vuln_type = "Boolean-based blind SQL injection"
                elif 'time-based blind' in output.lower():
                    vuln_type = "Time-based blind SQL injection"
                elif 'error-based' in output.lower():
                    vuln_type = "Error-based SQL injection"
                elif 'union query' in output.lower():
                    vuln_type = "UNION query SQL injection"
            
            # Create summary
            summary = f"""\n=== SQLMAP RESULTS ===
Target: {url}
Vulnerable: {'YES' if vulnerable else 'NO'}
Vulnerability Type: {vuln_type}

Full output length: {len(output)} characters
Key findings:
"""
            
            # Extract key lines
            for line in output.split('\n'):
                if any(keyword in line.lower() for keyword in ['vulnerable', 'injectable', 'parameter', 'payload']):
                    summary += f"  {line.strip()}\n"
            
            summary += "\n" + output
            
            return ToolResult(
                success=result['success'],
                output=summary,
                error=result['error']
            )
        except Exception as e:
            self.logger.error(f"SQLMap failed: {e}")
            return ToolResult(success=False, output="", error=str(e))
