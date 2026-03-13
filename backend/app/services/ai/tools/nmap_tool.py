from app.services.kali_executor import kali_executor
from typing import List
from .base import BaseTool, ToolParameter, ToolResult
import json

class NmapTool(BaseTool):
    def get_description(self) -> str:
        return "Scan network targets for open ports, services, and OS detection using Nmap in Kali Linux"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="target",
                type="string",
                description="Target IP address, hostname, or CIDR range"
            ),
            ToolParameter(
                name="scan_type",
                type="string",
                description="Type of scan: quick, full, stealth, version, os",
                required=False,
                enum=["quick", "full", "stealth", "version", "os"]
            )
        ]
    
    async def execute(self, target: str, scan_type: str = "quick") -> ToolResult:
        try:
            scan_args = {
                "quick": "-sV -T4 -F",
                "full": "-sS -sV -p- -T4",
                "stealth": "-sS -T2 -f",
                "version": "-sV -T4",
                "os": "-O -T4"
            }
            
            args = scan_args.get(scan_type, "-sV -T4 -F")
            command = f"nmap {args} {target}"
            
            self.logger.info(f"Executing: {command}")
            result = await kali_executor.execute(command, timeout=600, sudo=True)
            
            return ToolResult(
                success=result['success'],
                output=result['output'],
                error=result['error']
            )
        except Exception as e:
            self.logger.error(f"Nmap failed: {e}")
            return ToolResult(success=False, output="", error=str(e))
