import asyncio
from typing import Dict, Any, List
from .base_agent import BaseAgent
from .ssh_client import ssh_client
from app.services.ai.agent import SecurityAgent

class VulnerabilityScanner(BaseAgent):
    """Agent 1: Vulnerability Scanner - Scans specific targets for vulnerabilities"""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.target = None  # Will be set by user
        self.ai_agent = SecurityAgent()
        self.ai_agent.model = "huihui_ai/glm-4.7-flash-abliterated:q4_K"
        self.discovered_hosts = []
        self.waiting_for_target = False
    
    async def execute_task(self) -> Dict[str, Any]:
        """Main execution loop"""
        
        # Check if we have a target
        if not self.target:
            self.log("⚠️ No target set")
            return await self.discover_and_wait()
        
        # We have a target, scan it
        self.log(f"🎯 Target set: {self.target}")
        return await self.scan_target()
    
    async def discover_and_wait(self) -> Dict[str, Any]:
        """Discover hosts and wait for user to select target"""
        
        if not self.discovered_hosts:
            self.log("=" * 60)
            self.log("⚠️  NO TARGET SPECIFIED")
            self.log("=" * 60)
            self.log("🔍 Detecting host machine network...")
            
            # Get host network via backend API (runs on Windows host)
            import requests
            try:
                resp = requests.get('http://localhost:8000/api/v1/network/network-info', timeout=5)
                data = resp.json()
                scan_range = data.get('network_range', '192.168.1.0/24')
                self.log(f"🌐 Host network detected: {scan_range}")
            except Exception as e:
                self.log(f"⚠️ API detection failed: {e}")
                # Fallback: Use default Windows network range
                scan_range = "192.168.8.0/24"
                self.log(f"🌐 Using default Windows network: {scan_range}")
            
            self.log(f"📡 Scanning network: {scan_range}")
            self.log(f"⏳ Command: nmap -sn -T4 {scan_range}")
            
            cmd = f"nmap -sn -T4 {scan_range}"
            stdout, stderr, exit_code = await ssh_client.execute(cmd, timeout=90)
            
            if exit_code == 0:
                hosts = self.parse_discovered_hosts(stdout)
                self.discovered_hosts = hosts
                
                self.log("=" * 60)
                self.log(f"✅ DISCOVERED {len(hosts)} LIVE HOSTS:")
                self.log("=" * 60)
                
                for i, host in enumerate(hosts, 1):
                    self.log(f"  {i}. {host['ip']:15} - {host['hostname']}")
                
                self.log("=" * 60)
                self.log("⏸️  WAITING FOR USER TO SELECT TARGET")
                self.log("💡 Enter target IP in the input field and click Start")
                self.log("=" * 60)
                
                self.waiting_for_target = True
                
                return {
                    "status": "waiting_for_target",
                    "hosts": hosts,
                    "message": "Select a target IP to scan"
                }
        
        # Already discovered, still waiting
        self.log("⏸️  Still waiting for target selection...")
        return {"status": "waiting_for_target", "hosts": self.discovered_hosts}
    
    async def scan_target(self) -> Dict[str, Any]:
        """Perform deep vulnerability scan on target"""
        
        self.log("=" * 60)
        self.log(f"🎯 TARGET: {self.target}")
        self.log("=" * 60)
        self.log("🔬 PHASE 1: Service Detection")
        self.log(f"⏳ Command: nmap -sV -sC -T4 {self.target}")
        
        cmd = f"nmap -sV -sC -T4 {self.target}"
        stdout, stderr, exit_code = await ssh_client.execute(cmd, timeout=180)
        
        if exit_code == 0:
            services = self.parse_services(stdout)
            
            self.log("=" * 60)
            self.log(f"✅ FOUND {len(services)} SERVICES:")
            self.log("=" * 60)
            
            for svc in services:
                self.log(f"  Port {svc['port']:5} | {svc['service']:15} | {svc['version']}")
            
            # AI Analysis
            self.log("=" * 60)
            self.log("🤖 AI VULNERABILITY ANALYSIS")
            self.log("=" * 60)
            
            services_str = ', '.join([f"{s['port']}: {s['service']} {s['version']}" for s in services])
            
            analysis = await self.ask_ai(
                f"Analyze these services for vulnerabilities:\n"
                f"Services: {services_str}\n"
                f"List specific CVEs, exploitation difficulty, and impact."
            )
            
            self.log(analysis[:500])
            
            # Vulnerability scan
            self.log("=" * 60)
            self.log("🔬 PHASE 2: Vulnerability Scanning")
            self.log(f"⏳ Command: nmap --script vuln -T4 {self.target}")
            
            cmd = f"nmap --script vuln -T4 {self.target}"
            stdout, stderr, exit_code = await ssh_client.execute(cmd, timeout=240)
            
            vulns = []  # Initialize here
            if exit_code == 0:
                vulns = self.parse_vulnerabilities(stdout)
                
                self.log("=" * 60)
                self.log(f"✅ VULNERABILITY SCAN COMPLETE")
                self.log(f"📊 Found {len(vulns)} potential vulnerabilities")
                self.log("=" * 60)
                
                for vuln in vulns[:5]:  # Top 5
                    self.log(f"  ⚠️  {vuln}")
            else:
                self.log(f"⚠️ Vulnerability scan failed: {stderr[:200]}")
            
            self.log("=" * 60)
            self.log("✅ SCAN COMPLETE - Waiting 60 seconds before next scan")
            self.log("=" * 60)
            
            return {
                "target": self.target,
                "services": services,
                "vulnerabilities": vulns[:10],
                "ai_analysis": analysis[:500]
            }
        
        self.log(f"❌ Scan failed: {stderr}")
        return {"error": stderr}
    
    def parse_discovered_hosts(self, nmap_output: str) -> List[Dict]:
        """Parse nmap host discovery output"""
        hosts = []
        lines = nmap_output.split('\n')
        
        for line in lines:
            if 'Nmap scan report for' in line:
                parts = line.split()
                if len(parts) >= 5:
                    hostname = parts[4]
                    ip = parts[5].strip('()') if len(parts) > 5 else hostname
                    
                    # If hostname is IP, swap them
                    if hostname.replace('.', '').isdigit():
                        ip, hostname = hostname, 'Unknown'
                    
                    hosts.append({"ip": ip, "hostname": hostname})
        
        return hosts
    
    def parse_services(self, nmap_output: str) -> List[Dict]:
        """Parse nmap service detection output"""
        services = []
        for line in nmap_output.split('\n'):
            if '/tcp' in line and 'open' in line:
                parts = line.split()
                if len(parts) >= 3:
                    port = parts[0].split('/')[0]
                    service = parts[2] if len(parts) > 2 else 'unknown'
                    version = ' '.join(parts[3:]) if len(parts) > 3 else ''
                    services.append({
                        "port": port,
                        "service": service,
                        "version": version[:80]
                    })
        return services
    
    def parse_vulnerabilities(self, nmap_output: str) -> List[str]:
        """Parse vulnerability scan output"""
        vulns = []
        for line in nmap_output.split('\n'):
            if 'VULNERABLE' in line or 'CVE-' in line:
                vulns.append(line.strip())
        return vulns
    
    async def ask_ai(self, question: str) -> str:
        """Ask AI for analysis"""
        try:
            messages = [{"role": "user", "content": question}]
            response = ""
            async for chunk in self.ai_agent.chat(messages, stream=False):
                response += chunk
            return response
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}"
