import asyncio
from typing import Dict, Optional
from .vuln_scanner_v2 import VulnerabilityScanner
from .threat_hunter_v2 import ThreatHunterV2
from .exploit_generator_agent import ExploitGeneratorAgent
from .report_writer_agent import ReportWriterAgent
from .base_agent import BaseAgent

class AgentManager:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.tasks: Dict[str, asyncio.Task] = {}
    
    def create_agent(self, agent_id: str) -> BaseAgent:
        if agent_id == "vuln-scanner":
            return VulnerabilityScanner(agent_id)
        elif agent_id == "threat-hunter":
            return ThreatHunterV2(agent_id)
        elif agent_id == "exploit-gen":
            return ExploitGeneratorAgent(agent_id)
        elif agent_id == "report-writer":
            return ReportWriterAgent(agent_id)
        else:
            return VulnerabilityScanner(agent_id)
    
    async def start_agent(self, agent_id: str, target: str = None) -> bool:
        # Stop existing agent if running
        if agent_id in self.tasks and not self.tasks[agent_id].done():
            print(f"Stopping existing agent {agent_id}...")
            await self.stop_agent(agent_id)
            await asyncio.sleep(0.5)  # Give it time to stop
        
        # Create new agent instance
        agent = self.create_agent(agent_id)
        
        # Set custom target if provided (only for agents that need it)
        if target and target.strip() and hasattr(agent, 'target'):
            agent.target = target.strip()
            agent.discovered_hosts = []  # Reset discovery
            agent.waiting_for_target = False  # Reset waiting state
            print(f"✅ Agent {agent_id} starting with target: {target.strip()}")
        elif hasattr(agent, 'target'):
            print(f"⚠️ Agent {agent_id} starting without target (will discover hosts)")
        else:
            print(f"ℹ️ Agent {agent_id} starting (no target needed)")
        
        self.agents[agent_id] = agent
        
        task = asyncio.create_task(agent.run())
        self.tasks[agent_id] = task
        
        return True
    
    async def stop_agent(self, agent_id: str) -> bool:
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        agent.stop()
        
        if agent_id in self.tasks:
            task = self.tasks[agent_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.tasks[agent_id]
        
        return True
    
    def get_agent_logs(self, agent_id: str, limit: int = 10) -> list:
        if agent_id in self.agents:
            return self.agents[agent_id].get_logs(limit)
        return []
    
    def get_agent_results(self, agent_id: str) -> list:
        if agent_id in self.agents:
            return self.agents[agent_id].get_results()
        return []
    
    def is_agent_running(self, agent_id: str) -> bool:
        return agent_id in self.tasks and not self.tasks[agent_id].done()

# Global instance
agent_manager = AgentManager()
