from .base_agent import BaseAgent
from .web_agent import WebExploitAgent
from .network_agent import NetworkAgent
from typing import Dict, Any
import re

class MasterAgent(BaseAgent):
    def __init__(self):
        super().__init__("Master", [])
        self.web_agent = WebExploitAgent()
        self.network_agent = NetworkAgent()
    
    async def execute(self, target: str) -> Dict[str, Any]:
        target_type = self._detect_target_type(target)
        
        if target_type == 'url':
            return await self.web_agent.execute(target)
        elif target_type == 'ip':
            return await self.network_agent.execute(target)
        else:
            # Try both
            results = {
                'web': await self.web_agent.execute(f"http://{target}"),
                'network': await self.network_agent.execute(target)
            }
            return results
    
    def _detect_target_type(self, target: str) -> str:
        if target.startswith('http://') or target.startswith('https://'):
            return 'url'
        
        # Check if IP address
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ip_pattern, target):
            return 'ip'
        
        # Domain name
        return 'domain'
