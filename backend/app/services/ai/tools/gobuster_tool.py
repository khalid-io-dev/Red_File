from app.services.kali_executor import kali_executor
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class GobusterTool(BaseTool):
    def get_description(self) -> str:
        return "Directory and file brute forcing on web servers using Gobuster in Kali Linux"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="url",
                type="string",
                description="Target URL (e.g., https://example.com)"
            ),
            ToolParameter(
                name="wordlist",
                type="string",
                description="Wordlist path",
                required=False
            ),
            ToolParameter(
                name="extensions",
                type="string",
                description="File extensions to search (e.g., php,html,txt)",
                required=False
            )
        ]
    
    async def execute(self, url: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt", extensions: str = "php,html,txt,js") -> ToolResult:
        try:
            command = f"gobuster dir -u {url} -w {wordlist} -x {extensions} -t 50 --no-error"
            
            self.logger.info(f"Executing: {command}")
            result = await kali_executor.execute(command, timeout=600)
            
            # Parse found directories
            output = result['output']
            found_count = output.count('Status: 200') + output.count('Status: 301') + output.count('Status: 302')
            
            summary = f"""
=== GOBUSTER DIRECTORY SCAN ===
Target: {url}
Found: {found_count} directories/files

{output}
"""
            
            return ToolResult(
                success=result['success'],
                output=summary,
                error=result['error']
            )
        except Exception as e:
            self.logger.error(f"Gobuster failed: {e}")
            return ToolResult(success=False, output="", error=str(e))
