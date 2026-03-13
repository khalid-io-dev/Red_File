from app.services.kali_executor import kali_executor
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class FFufTool(BaseTool):
    def get_description(self) -> str:
        return "Fast web fuzzer using FFuf in Kali Linux"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="url", type="string", description="Target URL with FUZZ keyword"),
            ToolParameter(name="wordlist", type="string", description="Wordlist path", required=False)
        ]
    
    async def execute(self, url: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt") -> ToolResult:
        try:
            command = f"ffuf -u {url} -w {wordlist} -mc 200,301,302,403 -t 50"
            result = await kali_executor.execute(command, timeout=600)
            
            found = result['output'].count('Status:')
            
            summary = f"""
=== FFUF FUZZING RESULTS ===
Target: {url}
Results found: {found}

{result['output']}
"""
            return ToolResult(success=result['success'], output=summary, error=result['error'])
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))
