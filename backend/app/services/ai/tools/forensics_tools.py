from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from app.services.kali_executor import kali_executor
from typing import List

class VolatilityTool(BaseTool):
    name = "volatility"
    def get_description(self) -> str:
        return "Memory forensics framework for analyzing RAM dumps"
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="memory_dump", type="string", description="Path to memory dump file", required=True),
            ToolParameter(name="profile", type="string", description="OS profile", required=True),
            ToolParameter(name="plugin", type="string", description="Plugin to run", required=True)
        ]
    async def execute(self, **kwargs) -> ToolResult:
        dump = kwargs.get("memory_dump")
        profile = kwargs.get("profile")
        plugin = kwargs.get("plugin")
        cmd = f"volatility -f {dump} --profile={profile} {plugin}"
        result = await kali_executor.execute(cmd)
        return ToolResult(success=result["success"], output=result.get("output"), error=result.get("error"))

class AutopsyTool(BaseTool):
    name = "autopsy"
    def get_description(self) -> str:
        return "Digital forensics platform for disk image analysis"
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="image_file", type="string", description="Disk image file", required=True),
            ToolParameter(name="case_name", type="string", description="Case name", required=True)
        ]
    async def execute(self, **kwargs) -> ToolResult:
        return ToolResult(success=True, output="Autopsy GUI tool - use web interface")

class SnortTool(BaseTool):
    name = "snort"
    def get_description(self) -> str:
        return "Network intrusion detection and prevention system"
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="interface", type="string", description="Network interface", required=True),
            ToolParameter(name="config", type="string", description="Config file path", required=False)
        ]
    async def execute(self, **kwargs) -> ToolResult:
        interface = kwargs.get("interface")
        config = kwargs.get("config", "/etc/snort/snort.conf")
        cmd = f"snort -i {interface} -c {config} -A console"
        result = await kali_executor.execute(cmd, timeout=60)
        return ToolResult(success=result["success"], output=result.get("output"), error=result.get("error"))

class YaraTool(BaseTool):
    name = "yara"
    def get_description(self) -> str:
        return "Malware pattern matching and classification"
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="rules_file", type="string", description="YARA rules file", required=True),
            ToolParameter(name="target", type="string", description="File or directory to scan", required=True)
        ]
    async def execute(self, **kwargs) -> ToolResult:
        rules = kwargs.get("rules_file")
        target = kwargs.get("target")
        cmd = f"yara {rules} {target}"
        result = await kali_executor.execute(cmd)
        return ToolResult(success=result["success"], output=result.get("output"), error=result.get("error"))

class CuckooTool(BaseTool):
    name = "cuckoo"
    def get_description(self) -> str:
        return "Automated malware analysis sandbox"
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="file_path", type="string", description="Malware sample path", required=True),
            ToolParameter(name="timeout", type="integer", description="Analysis timeout", required=False)
        ]
    async def execute(self, **kwargs) -> ToolResult:
        file_path = kwargs.get("file_path")
        cmd = f"cuckoo submit {file_path}"
        result = await kali_executor.execute(cmd)
        return ToolResult(success=result["success"], output=result.get("output"), error=result.get("error"))

class Radare2Tool(BaseTool):
    name = "radare2"
    def get_description(self) -> str:
        return "Reverse engineering framework for binary analysis"
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="binary", type="string", description="Binary file to analyze", required=True),
            ToolParameter(name="command", type="string", description="r2 command to execute", required=True)
        ]
    async def execute(self, **kwargs) -> ToolResult:
        binary = kwargs.get("binary")
        command = kwargs.get("command")
        cmd = f"r2 -q -c '{command}' {binary}"
        result = await kali_executor.execute(cmd)
        return ToolResult(success=result["success"], output=result.get("output"), error=result.get("error"))

class FridaTool(BaseTool):
    name = "frida"
    def get_description(self) -> str:
        return "Dynamic instrumentation toolkit for apps"
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="process", type="string", description="Process name or PID", required=True),
            ToolParameter(name="script", type="string", description="Frida script to inject", required=True)
        ]
    async def execute(self, **kwargs) -> ToolResult:
        process = kwargs.get("process")
        script = kwargs.get("script")
        cmd = f"frida -n {process} -l {script}"
        result = await kali_executor.execute(cmd)
        return ToolResult(success=result["success"], output=result.get("output"), error=result.get("error"))

class BinwalkTool(BaseTool):
    name = "binwalk"
    def get_description(self) -> str:
        return "Firmware analysis and extraction tool"
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="firmware_file", type="string", description="Firmware file to analyze", required=True),
            ToolParameter(name="extract", type="boolean", description="Extract found files", required=False)
        ]
    async def execute(self, **kwargs) -> ToolResult:
        firmware = kwargs.get("firmware_file")
        extract = kwargs.get("extract", False)
        cmd = f"binwalk {'-e' if extract else ''} {firmware}"
        result = await kali_executor.execute(cmd)
        return ToolResult(success=result["success"], output=result.get("output"), error=result.get("error"))

class LynisTool(BaseTool):
    name = "lynis"
    def get_description(self) -> str:
        return "Security auditing tool for Unix/Linux systems"
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="mode", type="string", description="Audit mode", required=False, enum=["system", "quick"])
        ]
    async def execute(self, **kwargs) -> ToolResult:
        mode = kwargs.get("mode", "system")
        cmd = f"lynis audit {mode}"
        result = await kali_executor.execute(cmd)
        return ToolResult(success=result["success"], output=result.get("output"), error=result.get("error"))

class OpenVASTool(BaseTool):
    name = "openvas"
    def get_description(self) -> str:
        return "Comprehensive vulnerability scanner"
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="target", type="string", description="Target IP or hostname", required=True),
            ToolParameter(name="scan_config", type="string", description="Scan configuration", required=False)
        ]
    async def execute(self, **kwargs) -> ToolResult:
        target = kwargs.get("target")
        cmd = f"gvm-cli socket --xml '<create_target><name>{target}</name><hosts>{target}</hosts></create_target>'"
        result = await kali_executor.execute(cmd)
        return ToolResult(success=result["success"], output=result.get("output"), error=result.get("error"))

class SuricataTool(BaseTool):
    name = "suricata"
    def get_description(self) -> str:
        return "High performance IDS/IPS and network security monitoring"
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="interface", type="string", description="Network interface", required=True),
            ToolParameter(name="rules_path", type="string", description="Rules directory", required=False)
        ]
    async def execute(self, **kwargs) -> ToolResult:
        interface = kwargs.get("interface")
        rules = kwargs.get("rules_path", "/etc/suricata/rules")
        cmd = f"suricata -i {interface} -S {rules}"
        result = await kali_executor.execute(cmd, timeout=60)
        return ToolResult(success=result["success"], output=result.get("output"), error=result.get("error"))
