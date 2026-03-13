import asyncio
from typing import Dict, Any
from .base_agent import BaseAgent
from .ssh_client import ssh_client
from app.services.ai.agent import SecurityAgent

class ThreatHunterV2(BaseAgent):
    """Agent 2: Threat Hunter - Monitors network traffic for threats"""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.ai_agent = SecurityAgent()
        self.ai_agent.model = "huihui_ai/glm-4.7-flash-abliterated:q4_K"
        self.interface = None
        self.network_ip = None
    
    async def execute_task(self) -> Dict[str, Any]:
        """Main execution - continuous traffic monitoring"""
        
        # Detect network interface once
        if not self.interface:
            await self.detect_network()
        
        # Capture and analyze traffic
        return await self.capture_and_analyze()
    
    async def detect_network(self):
        """Auto-detect network interface"""
        self.log("=" * 60)
        self.log("🌐 DETECTING NETWORK INTERFACE")
        self.log("=" * 60)
        
        cmd = "ip -4 addr show | grep -v 127.0.0.1 | grep inet"
        stdout, _, exit_code = await ssh_client.execute(cmd, timeout=10)
        
        if exit_code == 0 and stdout.strip():
            lines = stdout.strip().split('\n')
            for line in lines:
                if 'inet' in line:
                    parts = line.split()
                    self.network_ip = parts[1].split('/')[0]
                    
                    # Get interface name
                    cmd2 = f"ip addr show | grep -B 2 {self.network_ip} | head -1 | awk '{{print $2}}' | tr -d ':'"
                    stdout2, _, exit_code2 = await ssh_client.execute(cmd2, timeout=10)
                    
                    if exit_code2 == 0:
                        self.interface = stdout2.strip()
                        break
        
        if self.interface:
            self.log(f"✅ Interface: {self.interface}")
            self.log(f"✅ IP Address: {self.network_ip}")
        else:
            self.log("⚠️ Using default interface: eth0")
            self.interface = "eth0"
        
        self.log("=" * 60)
    
    async def capture_and_analyze(self) -> Dict[str, Any]:
        """Capture traffic and analyze for threats"""
        
        self.log("=" * 60)
        self.log("📡 CAPTURING NETWORK TRAFFIC")
        self.log("=" * 60)
        self.log(f"Interface: {self.interface}")
        self.log(f"Duration: 10 seconds")
        self.log(f"Command: tcpdump -i {self.interface} -c 500 -nn")
        
        cmd = f"timeout 10 tcpdump -i {self.interface} -c 500 -nn 2>&1"
        stdout, stderr, exit_code = await ssh_client.execute(cmd, timeout=15)
        
        if stdout and len(stdout) > 100:
            self.log(f"✅ Captured {len(stdout.split(chr(10)))} packets")
            
            # Parse traffic
            stats = self.parse_traffic(stdout)
            
            self.log("=" * 60)
            self.log("📊 TRAFFIC STATISTICS")
            self.log("=" * 60)
            self.log(f"Total packets: {stats['total_packets']}")
            self.log(f"TCP: {stats['tcp']} | UDP: {stats['udp']} | ICMP: {stats['icmp']}")
            
            if stats['top_talkers']:
                self.log("=" * 60)
                self.log("👥 TOP TALKERS:")
                for ip, count in list(stats['top_talkers'].items())[:5]:
                    self.log(f"  {ip:15} - {count} packets")
            
            # AI Analysis
            self.log("=" * 60)
            self.log("🤖 AI THREAT ANALYSIS")
            self.log("=" * 60)
            
            analysis = await self.ask_ai(
                f"Analyze this network traffic for threats and anomalies:\\n"
                f"Total packets: {stats['total_packets']}\\n"
                f"TCP: {stats['tcp']}, UDP: {stats['udp']}, ICMP: {stats['icmp']}\\n"
                f"Top talkers: {list(stats['top_talkers'].items())[:5]}\\n"
                f"Sample traffic: {stdout[:1000]}\\n"
                f"Look for: port scans, brute force, DDoS, suspicious connections"
            )
            
            self.log(analysis[:400])
            
            # Check for threats
            if any(word in analysis.lower() for word in ['threat', 'attack', 'suspicious', 'scan', 'anomaly']):
                self.log("=" * 60)
                self.log("⚠️  POTENTIAL THREAT DETECTED!")
                self.log("=" * 60)
            else:
                self.log("=" * 60)
                self.log("✅ No threats detected")
                self.log("=" * 60)
            
            self.log("⏳ Next capture in 30 seconds...")
            
            return {
                "interface": self.interface,
                "stats": stats,
                "ai_analysis": analysis[:500],
                "threats_detected": 'threat' in analysis.lower()
            }
        
        self.log("⚠️ No traffic captured")
        return {"status": "no_traffic"}
    
    def parse_traffic(self, tcpdump_output: str) -> Dict[str, Any]:
        """Parse tcpdump output"""
        lines = tcpdump_output.split('\n')
        
        stats = {
            "total_packets": 0,
            "tcp": 0,
            "udp": 0,
            "icmp": 0,
            "top_talkers": {}
        }
        
        for line in lines:
            if not line.strip() or 'listening on' in line or 'captured' in line:
                continue
            
            stats["total_packets"] += 1
            
            # Count protocols
            if ' > ' in line:
                if 'tcp' in line.lower():
                    stats["tcp"] += 1
                elif 'udp' in line.lower():
                    stats["udp"] += 1
                elif 'icmp' in line.lower():
                    stats["icmp"] += 1
                
                # Extract source IP
                parts = line.split()
                if len(parts) > 2:
                    src = parts[2].split('.')[0:4]
                    if len(src) == 4:
                        src_ip = '.'.join(src)
                        stats["top_talkers"][src_ip] = stats["top_talkers"].get(src_ip, 0) + 1
        
        return stats
    
    async def ask_ai(self, question: str) -> str:
        """Ask AI for threat analysis"""
        try:
            messages = [{"role": "user", "content": question}]
            response = ""
            async for chunk in self.ai_agent.chat(messages, stream=False):
                response += chunk
            return response
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}"
    
    async def run(self):
        """Override run to use 30-second intervals"""
        self.is_running = True
        self.log("🚀 Agent started")
        
        while self.is_running:
            try:
                result = await self.execute_task()
                if result:
                    self.results.append(result)
                await asyncio.sleep(30)  # 30 seconds for traffic monitoring
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log(f"❌ Error: {str(e)}")
                await asyncio.sleep(10)
        
        self.log("⏸️ Agent stopped")
