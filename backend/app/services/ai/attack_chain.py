from typing import List, Dict, Any, Optional
from app.services.ai.tools import registry
import asyncio
import logging

logger = logging.getLogger(__name__)

class AttackPhase:
    def __init__(self, name: str, tools: List[tuple], depends_on: List[str] = None, parallel: bool = True):
        self.name = name
        self.tools = tools  # List of (tool_name, params_dict)
        self.depends_on = depends_on or []
        self.parallel = parallel
        self.results = {}
        self.completed = False

class AttackChain:
    def __init__(self, target: str):
        self.target = target
        self.phases: List[AttackPhase] = []
        self.results = {}
        self.metadata = {'target': target, 'phases_completed': 0, 'total_tools_run': 0}
    
    def add_phase(self, name: str, tools: List[tuple], depends_on: List[str] = None, parallel: bool = True):
        phase = AttackPhase(name, tools, depends_on, parallel)
        self.phases.append(phase)
        return self
    
    async def execute(self) -> Dict[str, Any]:
        for phase in self.phases:
            if not self._dependencies_met(phase):
                logger.warning(f"Skipping phase {phase.name} - dependencies not met")
                continue
            
            logger.info(f"Executing phase: {phase.name}")
            phase.results = await self._execute_phase(phase)
            phase.completed = True
            
            self.results[phase.name] = phase.results
            self.metadata['phases_completed'] += 1
            self.metadata['total_tools_run'] += len(phase.tools)
        
        return {
            'target': self.target,
            'results': self.results,
            'metadata': self.metadata
        }
    
    def _dependencies_met(self, phase: AttackPhase) -> bool:
        for dep in phase.depends_on:
            dep_phase = next((p for p in self.phases if p.name == dep), None)
            if not dep_phase or not dep_phase.completed:
                return False
        return True
    
    async def _execute_phase(self, phase: AttackPhase) -> Dict[str, Any]:
        if phase.parallel:
            return await self._execute_parallel(phase.tools)
        else:
            return await self._execute_sequential(phase.tools)
    
    async def _execute_parallel(self, tools: List[tuple]) -> Dict[str, Any]:
        results = {}
        
        async def run_tool(tool_name, params):
            tool = registry.get_tool(tool_name)
            if not tool:
                return tool_name, {'success': False, 'error': 'Tool not found'}
            
            try:
                result = await tool.execute(**params)
                return tool_name, {'success': result.success, 'output': result.output, 'error': result.error}
            except Exception as e:
                return tool_name, {'success': False, 'error': str(e)}
        
        tasks = [run_tool(tool_name, params) for tool_name, params in tools]
        completed = await asyncio.gather(*tasks, return_exceptions=True)
        
        for item in completed:
            if isinstance(item, Exception):
                continue
            tool_name, result = item
            results[tool_name] = result
        
        return results
    
    async def _execute_sequential(self, tools: List[tuple]) -> Dict[str, Any]:
        results = {}
        
        for tool_name, params in tools:
            tool = registry.get_tool(tool_name)
            if not tool:
                results[tool_name] = {'success': False, 'error': 'Tool not found'}
                continue
            
            try:
                result = await tool.execute(**params)
                results[tool_name] = {'success': result.success, 'output': result.output, 'error': result.error}
            except Exception as e:
                results[tool_name] = {'success': False, 'error': str(e)}
        
        return results

# Predefined attack chains
class WebAttackChain(AttackChain):
    def __init__(self, target_url: str):
        super().__init__(target_url)
        domain = target_url.replace('https://', '').replace('http://', '').split('/')[0]
        
        self.add_phase('recon', [
            ('webrecon', {'target': domain, 'recon_type': 'all'}),
            ('dnsenum', {'domain': domain, 'record_types': 'A,MX,NS,TXT'}),
            ('theharvester', {'domain': domain, 'source': 'all'}),
        ], parallel=True)
        
        self.add_phase('scan', [
            ('nikto', {'host': target_url}),
            ('nuclei', {'target': target_url, 'severity': 'critical,high,medium'}),
            ('gobuster', {'url': target_url}),
        ], depends_on=['recon'], parallel=True)
        
        self.add_phase('exploit', [
            ('sqlmap', {'url': target_url}),
            ('custom_exploit', {'target': target_url, 'exploit_type': 'xss'}),
        ], depends_on=['scan'], parallel=True)

class NetworkAttackChain(AttackChain):
    def __init__(self, target_ip: str):
        super().__init__(target_ip)
        
        self.add_phase('discovery', [
            ('nmap', {'target': target_ip, 'scan_type': 'quick'}),
        ], parallel=False)
        
        self.add_phase('enum', [
            ('nmap', {'target': target_ip, 'scan_type': 'version'}),
            ('dnsenum', {'domain': target_ip, 'record_types': 'A,PTR'}),
        ], depends_on=['discovery'], parallel=True)
        
        self.add_phase('exploit', [
            ('hydra', {'target': target_ip, 'service': 'ssh', 'username': 'admin'}),
        ], depends_on=['enum'], parallel=False)
