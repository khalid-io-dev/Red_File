from .base_agent import BaseAgent
from typing import Dict, Any
import re

class NetworkAgent(BaseAgent):
    def __init__(self):
        super().__init__("Network", [
            'nmap', 'portscan', 'hydra', 'dnsenum', 'ssl_analyzer'
        ])
    
    async def execute(self, target_ip: str) -> Dict[str, Any]:
        results = {'agent': self.name, 'target': target_ip, 'phases': {}}
        
        # Phase 1: Port Scanning
        results['phases']['portscan'] = await self.run_tool('nmap', {
            'target': target_ip,
            'scan_type': 'version'
        })
        
        # Phase 2: Service Enumeration (parallel)
        results['phases']['enum'] = await self.parallel_run([
            ('dnsenum', {'domain': target_ip, 'record_types': 'A,MX,NS,TXT'}),
            ('ssl_analyzer', {'target': target_ip}),
        ])
        
        # Phase 3: Brute Force on discovered services
        services = self._extract_services(results['phases']['portscan']['output'])
        results['phases']['brute_force'] = {}
        
        for service in services:
            if service in ['ssh', 'ftp', 'mysql', 'postgres']:
                results['phases']['brute_force'][service] = await self.run_tool('hydra', {
                    'target': target_ip,
                    'service': service,
                    'username': 'admin'
                })
        
        return results
    
    def _extract_services(self, nmap_output: str) -> list:
        services = []
        for line in nmap_output.split('\n'):
            if 'open' in line.lower():
                if 'ssh' in line.lower():
                    services.append('ssh')
                elif 'ftp' in line.lower():
                    services.append('ftp')
                elif 'mysql' in line.lower():
                    services.append('mysql')
                elif 'postgres' in line.lower():
                    services.append('postgres')
        return list(set(services))
