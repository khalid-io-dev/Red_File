import asyncio
import json
from typing import Dict, Any, List
from .base_agent import BaseAgent
from .ssh_client import ssh_client
from app.services.ai.agent import SecurityAgent

class ThreatHunterAgentAdvanced(BaseAgent):
    """Proactively hunts for threats in network traffic"""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.targets = ["192.168.56.0/24"]
        self.ai_agent = SecurityAgent()
        self.ai_agent.model = "huihui_ai/glm-4.7-flash-abliterated:q4_K"  # Better model
        self.network_hosts = []
        self.traffic_captures = []
        self.anomalies_detected = []
        self.monitoring = True
    
    async def execute_task(self) -> Dict[str, Any]:
        """Continuous network monitoring and threat hunting"""
        
        # Step 1: Discover network hosts
        if not self.network_hosts:
            await self.discover_network()
        
        # Step 2: Capture and analyze traffic
        result = await self.analyze_traffic()
        
        # Step 3: Hunt for IOCs
        await self.hunt_iocs()
        
        return result
    
    async def discover_network(self):
        """Discover all hosts in network"""
        self.log("🌐 Discovering network hosts...")
        
        target = self.targets[0]
        cmd = f"nmap -sn -T4 {target}"
        stdout, stderr, exit_code = await ssh_client.execute(cmd, timeout=60)
        
        if exit_code == 0:
            hosts = self.parse_hosts(stdout)
            self.network_hosts = hosts
            self.log(f"✅ Found {len(hosts)} hosts to monitor")
    
    async def analyze_traffic(self) -> Dict[str, Any]:
        """Capture and analyze network traffic"""
        self.log("📡 Analyzing network traffic...")
        
        # Use tcpdump to capture traffic
        cmd = "timeout 5 tcpdump -i any -c 100 -nn 2>/dev/null || echo 'No traffic'"
        stdout, stderr, exit_code = await ssh_client.execute(cmd, timeout=10)
        
        if "No traffic" not in stdout:
            # AI analyzes traffic patterns
            analysis = await self.ask_ai(
                f"Analyze this network traffic for threats and anomalies:\n{stdout[:1000]}\n"
                f"Look for: port scans, brute force, suspicious connections, data exfiltration"
            )
            
            self.log(f"🤖 AI Analysis: {analysis[:150]}...")
            
            # Detect anomalies
            if any(word in analysis.lower() for word in ['suspicious', 'threat', 'attack', 'anomaly']):
                self.log("⚠️ Threat detected in traffic!")
                self.anomalies_detected.append({
                    "timestamp": asyncio.get_event_loop().time(),
                    "analysis": analysis[:500]
                })
            else:
                self.log("✅ No threats detected")
            
            return {
                "traffic_analyzed": True,
                "threats_found": len(self.anomalies_detected),
                "ai_analysis": analysis[:300]
            }
        
        self.log("⚠️ No traffic captured")
        return {"traffic_analyzed": False}
    
    async def hunt_iocs(self):
        """Hunt for Indicators of Compromise"""
        if not self.network_hosts:
            return
        
        self.log("🔍 Hunting for IOCs...")
        
        # Check for suspicious ports on random host
        import random
        host = random.choice(self.network_hosts)
        
        cmd = f"nmap -p 1-1000 -T4 {host}"
        stdout, stderr, exit_code = await ssh_client.execute(cmd, timeout=30)
        
        if exit_code == 0:
            # AI evaluates if ports are suspicious
            ioc_check = await self.ask_ai(
                f"Are these open ports on {host} suspicious or indicate compromise?\n{stdout[:500]}"
            )
            
            self.log(f"🤖 IOC Check: {ioc_check[:100]}...")
    
    async def ask_ai(self, question: str) -> str:
        """Ask AI for threat analysis"""
        try:
            messages = [{"role": "user", "content": question}]
            response = ""
            async for chunk in self.ai_agent.chat(messages, stream=False):
                response += chunk
            return response
        except Exception as e:
            self.log(f"⚠️ AI error: {str(e)}")
            return "AI analysis unavailable"
    
    def parse_hosts(self, nmap_output: str) -> List[str]:
        hosts = []
        for line in nmap_output.split('\n'):
            if 'Nmap scan report for' in line:
                parts = line.split()
                if len(parts) >= 5:
                    host = parts[4].strip('()')
                    hosts.append(host)
        return hosts
