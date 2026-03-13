from typing import Dict, Type, List
from .base import BaseTool
from .nmap_tool import NmapTool
from .sqlmap_tool import SQLMapTool
from .nuclei_tool import NucleiTool
from .nikto_tool import NiktoTool
from .sql_injection_exploit import SQLInjectionExploitTool
from .custom_exploit import CustomExploitTool
from .webrecon_tool import WebReconTool
from .portscan_tool import PortScanTool
from .ssl_analyzer_tool import SSLAnalyzerTool
from .dnsenum_tool import DNSEnumTool
from .hydra_tool import HydraTool
from .gobuster_tool import GobusterTool
from .theharvester_tool import TheHarvesterTool
from .wpscan_tool import WPScanTool
from .wfuzz_tool import WfuzzTool
from .masscan_tool import MasscanTool
from .commix_tool import CommixTool
from .ffuf_tool import FFufTool
from .enum4linux_tool import Enum4linuxTool
from .testssl_tool import TestsslTool
from .amass_tool import AmassTool
from .john_tool import JohnTool
from .responder_tool import ResponderTool
from .searchsploit_tool import SearchsploitTool
from .sublist3r_tool import Sublist3rTool
from .crackmapexec_tool import CrackMapExecTool
from .sherlock_tool import SherlockTool
from .metasploit_tool import MetasploitTool
from .hashcat_tool import HashcatTool
from .aws_scanner_tool import AWSSecurityScanner
from .azure_scanner_tool import AzureSecurityScanner
from .gcp_scanner_tool import GCPSecurityScanner
from .docker_scanner_tool import DockerSecurityScanner
from .k8s_scanner_tool import KubernetesSecurityScanner
from .wireshark_tool import WiresharkTool
from .aircrack_tool import AircrackTool
from .forensics_tools import (VolatilityTool, AutopsyTool, SnortTool, YaraTool, 
                              CuckooTool, Radare2Tool, FridaTool, BinwalkTool, 
                              LynisTool, OpenVASTool, SuricataTool)
from .msfvenom_tool import MsfvenomTool
from .offensive_tools import (TheHarvesterTool as TheHarvesterOSINT, SherlockTool as SherlockOSINT,
                              SEToolkitTool, GophishTool, EvilginxTool, BeEFTool)

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        # Network & Port Scanning
        self.register(NmapTool())
        self.register(PortScanTool())
        self.register(MasscanTool())
        
        # Web Application Testing
        self.register(SQLMapTool())
        self.register(NucleiTool())
        self.register(NiktoTool())
        self.register(WebReconTool())
        self.register(GobusterTool())
        self.register(WPScanTool())
        self.register(CustomExploitTool())
        self.register(SQLInjectionExploitTool())
        self.register(WfuzzTool())
        self.register(FFufTool())
        self.register(CommixTool())
        
        # Brute Force & Password Attacks
        self.register(HydraTool())
        
        # OSINT & Reconnaissance
        self.register(TheHarvesterTool())
        self.register(DNSEnumTool())
        self.register(SSLAnalyzerTool())
        
        # SMB/Windows Enumeration
        self.register(Enum4linuxTool())
        
        # New Tools - Week 2
        self.register(TestsslTool())
        self.register(AmassTool())
        self.register(JohnTool())
        self.register(ResponderTool())
        self.register(SearchsploitTool())
        self.register(Sublist3rTool())
        self.register(CrackMapExecTool())
        self.register(SherlockTool())
        self.register(MetasploitTool())
        self.register(HashcatTool())
        
        self.register(AWSSecurityScanner())
        self.register(AzureSecurityScanner())
        self.register(GCPSecurityScanner())
        self.register(DockerSecurityScanner())
        self.register(KubernetesSecurityScanner())
        
        # Forensics & Advanced Tools - Month 3
        self.register(WiresharkTool())
        self.register(AircrackTool())
        self.register(VolatilityTool())
        self.register(AutopsyTool())
        self.register(SnortTool())
        self.register(YaraTool())
        self.register(CuckooTool())
        self.register(Radare2Tool())
        self.register(FridaTool())
        self.register(BinwalkTool())
        self.register(LynisTool())
        self.register(OpenVASTool())
        self.register(SuricataTool())
        
        # Offensive Security Tools
        self.register(MsfvenomTool())
        self.register(SEToolkitTool())
        self.register(GophishTool())
        self.register(EvilginxTool())
        self.register(BeEFTool())
    
    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool
    
    def get_tool(self, name: str) -> BaseTool:
        return self._tools.get(name)
    
    def get_all_tools(self) -> List[BaseTool]:
        return list(self._tools.values())
    
    def get_ollama_tools(self) -> List[Dict]:
        return [tool.to_ollama_tool() for tool in self._tools.values()]

registry = ToolRegistry()
