from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from typing import List, Dict, Any

class WiresharkTool(BaseTool):
    name = "wireshark"
    
    def get_description(self) -> str:
        return "Network protocol analyzer for packet capture and analysis"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="interface", type="string", description="Network interface to capture", required=True),
            ToolParameter(name="filter", type="string", description="Capture filter (BPF syntax)", required=False),
            ToolParameter(name="duration", type="integer", description="Capture duration in seconds", required=False),
            ToolParameter(name="output_file", type="string", description="Output pcap file", required=False)
        ]
    
    async def execute(self, **kwargs) -> ToolResult:
        interface = kwargs.get("interface", "eth0")
        filter_expr = kwargs.get("filter", "")
        duration = kwargs.get("duration", 60)
        output = kwargs.get("output_file", "/tmp/capture.pcap")
        
        cmd = f"tshark -i {interface} -a duration:{duration} -w {output}"
        if filter_expr:
            cmd += f" -f '{filter_expr}'"
        
        result = await self.executor.execute_command(cmd)
        
        if result["success"]:
            stats_cmd = f"capinfos {output}"
            stats = await self.executor.execute_command(stats_cmd)
            return ToolResult(success=True, output=f"Capture saved to {output}\n{stats['output']}")
        
        return ToolResult(success=False, error=result.get("error"))
