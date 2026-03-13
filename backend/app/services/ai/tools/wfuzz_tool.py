from app.services.kali_executor import kali_executor
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class WfuzzTool(BaseTool):
    def get_description(self) -> str:
        return "Web application fuzzer for parameters, directories, and headers using Wfuzz in Kali Linux"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="url", type="string", description="Target URL with FUZZ keyword"),
            ToolParameter(name="wordlist", type="string", description="Wordlist path", required=False),
            ToolParameter(name="filter", type="string", description="Filter by code (e.g., 200,301)", required=False)
        ]
    
    async def execute(self, url: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt", filter: str = "200,301,302") -> ToolResult:
        try:
            command = f"wfuzz -c -z file,{wordlist} --sc {filter} {url}"
            result = await kali_executor.execute(command, timeout=600)
            
            lines = result['output'].split('\n')
            found = len([l for l in lines if 'C=' in l])
            
            summary = f"""
=== WFUZZ RESULTS ===
Target: {url}
Found: {found} results

{result['output']}
"""
            return ToolResult(success=result['success'], output=summary, error=result['error'])
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))
