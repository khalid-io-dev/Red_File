from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from typing import List

class AircrackTool(BaseTool):
    name = "aircrack"
    
    def get_description(self) -> str:
        return "WiFi security auditing and WEP/WPA/WPA2 cracking"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="mode", type="string", description="Mode: scan, crack", required=True, enum=["scan", "crack"]),
            ToolParameter(name="interface", type="string", description="Wireless interface", required=True),
            ToolParameter(name="bssid", type="string", description="Target BSSID", required=False),
            ToolParameter(name="wordlist", type="string", description="Wordlist for cracking", required=False)
        ]
    
    async def execute(self, **kwargs) -> ToolResult:
        mode = kwargs.get("mode")
        interface = kwargs.get("interface")
        
        if mode == "scan":
            cmd = f"airodump-ng {interface} --output-format csv --write /tmp/scan"
            result = await self.executor.execute_command(cmd, timeout=30)
            return ToolResult(success=result["success"], output=result.get("output"), error=result.get("error"))
        
        elif mode == "crack":
            bssid = kwargs.get("bssid")
            wordlist = kwargs.get("wordlist", "/usr/share/wordlists/rockyou.txt")
            cmd = f"aircrack-ng -b {bssid} -w {wordlist} /tmp/scan*.cap"
            result = await self.executor.execute_command(cmd, timeout=300)
            return ToolResult(success=result["success"], output=result.get("output"), error=result.get("error"))
        
        return ToolResult(success=False, error="Invalid mode")
