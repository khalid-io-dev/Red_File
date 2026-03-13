from abc import ABC, abstractmethod
import asyncio
from typing import Dict, Any, List
from datetime import datetime

class BaseAgent(ABC):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.is_running = False
        self.logs: List[str] = []
        self.results: List[Dict[str, Any]] = []
    
    def log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(f"[{self.agent_id}] {log_entry}")
    
    @abstractmethod
    async def execute_task(self) -> Dict[str, Any]:
        """Execute single agent task"""
        pass
    
    async def run(self):
        """Main agent loop"""
        self.is_running = True
        self.log(f"🚀 Agent started")
        
        # Set interval based on agent type
        if self.agent_id == "vuln-scanner":
            interval = 60
        elif self.agent_id == "threat-hunter":
            interval = 30
        elif self.agent_id == "exploit-gen":
            interval = 120
        elif self.agent_id == "report-writer":
            interval = 300
        else:
            interval = 60
        
        while self.is_running:
            try:
                result = await self.execute_task()
                if result:
                    self.results.append(result)
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log(f"❌ Error: {str(e)}")
                await asyncio.sleep(10)
        
        self.log(f"⏸️ Agent stopped")
    
    def stop(self):
        self.is_running = False
    
    def get_logs(self, limit: int = 10) -> List[str]:
        return self.logs[-limit:]
    
    def get_results(self) -> List[Dict[str, Any]]:
        return self.results
