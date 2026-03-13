from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from app.services.kali_executor import kali_executor
from typing import List

class JohnTool(BaseTool):
    def get_description(self) -> str:
        return "John the Ripper password cracker"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="hash_file", type="string", description="Hash file path", required=True),
            ToolParameter(name="wordlist", type="string", description="Wordlist path", required=False),
        ]
    
    async def execute(self, hash_file: str, wordlist: str = "/usr/share/wordlists/rockyou.txt", **kwargs) -> ToolResult:
        cmd = f"john {hash_file} --wordlist={wordlist}"
        result = await kali_executor.execute(cmd, timeout=300)
        return ToolResult(success=True, output=result["stdout"], error=result["stderr"])
