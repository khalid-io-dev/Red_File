from app.services.kali_executor import kali_executor
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class WPScanTool(BaseTool):
    def get_description(self) -> str:
        return "WordPress vulnerability scanner using WPScan in Kali Linux"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="url",
                type="string",
                description="WordPress site URL"
            ),
            ToolParameter(
                name="enumerate",
                type="string",
                description="What to enumerate: p (plugins), t (themes), u (users), all",
                required=False,
                enum=["p", "t", "u", "all"]
            )
        ]
    
    async def execute(self, url: str, enumerate: str = "all") -> ToolResult:
        try:
            command = f"wpscan --url {url} --enumerate {enumerate} --random-user-agent"
            
            self.logger.info(f"Executing: {command}")
            result = await kali_executor.execute(command, timeout=600)
            
            # Parse results
            output = result['output']
            vulns = output.count('[!]')
            plugins = output.count('| Name:')
            
            summary = f"""
=== WPSCAN RESULTS ===
Target: {url}
Vulnerabilities: {vulns}
Plugins/Themes found: {plugins}

{output}
"""
            
            return ToolResult(
                success=result['success'],
                output=summary,
                error=result['error']
            )
        except Exception as e:
            self.logger.error(f"WPScan failed: {e}")
            return ToolResult(success=False, output="", error=str(e))
