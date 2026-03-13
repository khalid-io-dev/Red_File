from app.services.kali_executor import kali_executor
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class TheHarvesterTool(BaseTool):
    def get_description(self) -> str:
        return "OSINT tool for gathering emails, subdomains, IPs, and URLs using TheHarvester in Kali Linux"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="domain",
                type="string",
                description="Target domain (e.g., example.com)"
            ),
            ToolParameter(
                name="source",
                type="string",
                description="Data source: google, bing, linkedin, twitter, all",
                required=False,
                enum=["google", "bing", "linkedin", "twitter", "all"]
            )
        ]
    
    async def execute(self, domain: str, source: str = "all") -> ToolResult:
        try:
            command = f"theHarvester -d {domain} -b {source} -l 500"
            
            self.logger.info(f"Executing: {command}")
            result = await kali_executor.execute(command, timeout=300)
            
            # Parse results
            output = result['output']
            emails = output.count('@')
            hosts = output.count('[*]')
            
            summary = f"""
=== THEHARVESTER OSINT RESULTS ===
Domain: {domain}
Source: {source}
Emails found: {emails}
Hosts found: {hosts}

{output}
"""
            
            return ToolResult(
                success=result['success'],
                output=summary,
                error=result['error']
            )
        except Exception as e:
            self.logger.error(f"TheHarvester failed: {e}")
            return ToolResult(success=False, output="", error=str(e))
