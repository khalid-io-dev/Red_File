import asyncio
import json
from typing import Dict, Any, List
from .base_agent import BaseAgent
from .ssh_client import ssh_client
from app.services.ai.agent import SecurityAgent

class IntelligentVulnAgent(BaseAgent):
    """AI-powered autonomous vulnerability assessment agent"""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.targets = ["192.168.56.0/24"]
        self.ai_agent = SecurityAgent()
        self.discovered_hosts = []
        self.vulnerabilities = []
        self.current_phase = "reconnaissance"
        self.tools_used = []
    
    async def execute_task(self) -> Dict[str, Any]:
        """AI-driven task execution"""
        
        # Phase 1: Reconnaissance
        if self.current_phase == "reconnaissance":
            return await self.phase_reconnaissance()
        
        # Phase 2: Vulnerability Scanning
        elif self.current_phase == "vulnerability_scan":
            return await self.phase_vulnerability_scan()
        
        # Phase 3: Exploitation Analysis
        elif self.current_phase == "exploitation":
            return await self.phase_exploitation()
        
        # Phase 4: Reporting
        elif self.current_phase == "reporting":
            return await self.phase_reporting()
        
        return {}
    
    async def phase_reconnaissance(self) -> Dict[str, Any]:
        """Phase 1: Discover live hosts"""
        self.log("🎯 Phase 1: Reconnaissance - Discovering live hosts")
        
        target = self.targets[0]
        
        # Use AI to decide scan strategy
        ai_decision = await self.ask_ai(
            f"I need to discover live hosts on {target}. What nmap command should I use for fast host discovery?"
        )
        
        self.log(f"🤖 AI Decision: {ai_decision[:100]}...")
        
        # Execute host discovery
        cmd = f"nmap -sn -T4 {target}"
        self.log(f"📡 Executing: {cmd}")
        
        stdout, stderr, exit_code = await ssh_client.execute(cmd, timeout=60)
        
        if exit_code == 0:
            hosts = self.parse_live_hosts(stdout)
            self.discovered_hosts = hosts
            self.log(f"✅ Discovered {len(hosts)} live hosts")
            
            # AI decides next phase
            if len(hosts) > 0:
                self.current_phase = "vulnerability_scan"
                self.log("🔄 Moving to Phase 2: Vulnerability Scanning")
            
            return {
                "phase": "reconnaissance",
                "hosts_found": len(hosts),
                "hosts": hosts[:5],  # First 5
                "ai_decision": ai_decision[:200]
            }
        
        return {"phase": "reconnaissance", "error": stderr}
    
    async def phase_vulnerability_scan(self) -> Dict[str, Any]:
        """Phase 2: Deep scan on discovered hosts"""
        if not self.discovered_hosts:
            self.current_phase = "reporting"
            return {}
        
        # Pick next host to scan
        host = self.discovered_hosts[0]
        self.log(f"🔬 Phase 2: Deep scanning {host}")
        
        # AI decides what to scan for
        ai_decision = await self.ask_ai(
            f"I found host {host}. What nmap scan should I run to find vulnerabilities and services?"
        )
        
        self.log(f"🤖 AI suggests: {ai_decision[:100]}...")
        
        # Execute service detection
        cmd = f"nmap -sV -sC -T4 {host}"
        self.log(f"📡 Executing: {cmd}")
        
        stdout, stderr, exit_code = await ssh_client.execute(cmd, timeout=120)
        
        if exit_code == 0:
            services = self.parse_services(stdout)
            self.log(f"✅ Found {len(services)} services on {host}")
            
            # AI analyzes results
            analysis = await self.ask_ai(
                f"I found these services on {host}: {json.dumps(services)}. "
                f"What vulnerabilities should I check for? What tools should I use next?"
            )
            
            self.log(f"🤖 AI Analysis: {analysis[:150]}...")
            
            # Remove scanned host
            self.discovered_hosts.pop(0)
            
            # Move to exploitation if vulnerabilities found
            if len(services) > 0:
                self.vulnerabilities.append({
                    "host": host,
                    "services": services,
                    "ai_analysis": analysis
                })
                self.current_phase = "exploitation"
            
            return {
                "phase": "vulnerability_scan",
                "host": host,
                "services": services,
                "ai_analysis": analysis[:300]
            }
        
        return {"phase": "vulnerability_scan", "error": stderr}
    
    async def phase_exploitation(self) -> Dict[str, Any]:
        """Phase 3: AI-guided exploitation analysis"""
        if not self.vulnerabilities:
            self.current_phase = "reporting"
            return {}
        
        vuln = self.vulnerabilities[0]
        self.log(f"💥 Phase 3: Analyzing exploitation for {vuln['host']}")
        
        # AI decides exploitation strategy
        exploit_plan = await self.ask_ai(
            f"Host {vuln['host']} has these services: {json.dumps(vuln['services'])}. "
            f"What exploits should I try? What's the attack path? Use searchsploit or metasploit."
        )
        
        self.log(f"🤖 Exploit Plan: {exploit_plan[:200]}...")
        
        # Search for exploits
        for service in vuln['services'][:2]:  # Check first 2 services
            service_name = service.get('service', 'unknown')
            version = service.get('version', '')
            
            if service_name != 'unknown':
                cmd = f"searchsploit {service_name} {version}"
                self.log(f"🔍 Searching exploits: {cmd}")
                
                stdout, stderr, exit_code = await ssh_client.execute(cmd, timeout=30)
                
                if exit_code == 0 and stdout.strip():
                    self.log(f"💣 Found exploits for {service_name}")
                    vuln['exploits'] = stdout[:500]
        
        self.vulnerabilities.pop(0)
        
        # Move to reporting after exploitation
        if not self.vulnerabilities:
            self.current_phase = "reporting"
        
        return {
            "phase": "exploitation",
            "host": vuln['host'],
            "exploit_plan": exploit_plan[:300],
            "exploits_found": 'exploits' in vuln
        }
    
    async def phase_reporting(self) -> Dict[str, Any]:
        """Phase 4: AI generates report"""
        self.log("📊 Phase 4: Generating AI report")
        
        # AI generates comprehensive report
        report = await self.ask_ai(
            f"Generate a security assessment report. "
            f"I scanned {len(self.discovered_hosts) + len(self.vulnerabilities)} hosts. "
            f"Tools used: {', '.join(self.tools_used)}. "
            f"Summarize findings and recommendations."
        )
        
        self.log(f"📄 Report generated: {len(report)} chars")
        
        # Reset for next cycle
        self.current_phase = "reconnaissance"
        self.discovered_hosts = []
        self.vulnerabilities = []
        
        return {
            "phase": "reporting",
            "report": report[:500],
            "cycle_complete": True
        }
    
    async def ask_ai(self, question: str) -> str:
        """Ask AI agent for decision"""
        try:
            messages = [{"role": "user", "content": question}]
            response = ""
            async for chunk in self.ai_agent.chat(messages, stream=False):
                response += chunk
            return response
        except Exception as e:
            self.log(f"⚠️ AI error: {str(e)}")
            return "AI unavailable, using default strategy"
    
    def parse_live_hosts(self, nmap_output: str) -> List[str]:
        """Extract live hosts from nmap output"""
        hosts = []
        for line in nmap_output.split('\n'):
            if 'Nmap scan report for' in line:
                parts = line.split()
                if len(parts) >= 5:
                    host = parts[4].strip('()')
                    hosts.append(host)
        return hosts
    
    def parse_services(self, nmap_output: str) -> List[Dict]:
        """Extract services from nmap output"""
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
                        "version": version[:50]
                    })
        return services
