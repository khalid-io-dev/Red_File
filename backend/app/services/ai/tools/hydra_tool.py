from app.services.kali_executor import kali_executor
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class HydraTool(BaseTool):
    def get_description(self) -> str:
        return "Brute force attack on network services (SSH, FTP, HTTP, SMB, RDP, etc) using Hydra in Kali Linux"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="target",
                type="string",
                description="Target IP or hostname"
            ),
            ToolParameter(
                name="service",
                type="string",
                description="Service to attack: ssh, ftp, http-post-form, smb, rdp, mysql, postgres",
                enum=["ssh", "ftp", "http-post-form", "smb", "rdp", "mysql", "postgres"]
            ),
            ToolParameter(
                name="username",
                type="string",
                description="Username to test"
            ),
            ToolParameter(
                name="wordlist",
                type="string",
                description="Password wordlist path",
                required=False
            )
        ]
    
    async def execute(self, target: str, service: str, username: str, wordlist: str = "/usr/share/wordlists/rockyou.txt") -> ToolResult:
        try:
            command = f"hydra -l {username} -P {wordlist} -t 4 {target} {service}"
            
            self.logger.info(f"Executing: {command}")
            result = await kali_executor.execute(command, timeout=600)
            
            # Parse for successful credentials
            output = result['output']
            success_found = 'login:' in output and 'password:' in output
            
            summary = f"""
=== HYDRA BRUTE FORCE RESULTS ===
Target: {target}
Service: {service}
Username: {username}
Success: {'YES - Credentials found!' if success_found else 'NO'}

{output}
"""
            
            return ToolResult(
                success=result['success'],
                output=summary,
                error=result['error']
            )
        except Exception as e:
            self.logger.error(f"Hydra failed: {e}")
            return ToolResult(success=False, output="", error=str(e))
