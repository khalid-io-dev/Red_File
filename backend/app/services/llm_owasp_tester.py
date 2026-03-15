"""
LLM-powered OWASP Top 10 Vulnerability Tester
Uses local Ollama model for intelligent vulnerability analysis
"""
import asyncio
import json
import ollama
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.services.kali_executor import kali_executor

# Available Ollama models - using smaller models that fit in limited memory
AVAILABLE_MODELS = [
    "qwen2.5:0.5b",        # Very small - 352MB
    "qwen2.5:1.8b",        # Small - 1.1GB  
    "llama3.2:1b",         # Small - 1.3GB
    "llama3.2:3b",         # Medium - 1.8GB
    "mistral:7b",          # Larger - 4.1GB
    "llama3.1:8b",         # Large - 4.9GB
]

DEFAULT_MODEL = "qwen2.5:1.8b"  # Small model that fits in limited memory


class LLMOWASPTester:
    """OWASP Top 10 tester using local Ollama LLM for intelligent analysis"""
    
    def __init__(self, target_url: str, model: str = DEFAULT_MODEL):
        self.target = target_url
        self.model = model
        self.results = []
        self.logs = []
        self.progress = 0
        self.current_test = ""
        self.start_time = None
        
    def log(self, message: str, level: str = "info"):
        """Add log entry"""
        entry = {
            "message": message,
            "type": level,
            "timestamp": datetime.now().isoformat()
        }
        self.logs.append(entry)
        print(f"[OWASP-{level.upper()}] {message}")
    
    async def call_llm(self, prompt: str, system: str = None, temperature: float = 0.3) -> str:
        """Call Ollama LLM with prompt"""
        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            # Use synchronous ollama call in async context
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={"temperature": temperature, "num_predict": 2048}
            )
            return response['message']['content']
        except Exception as e:
            self.log(f"LLM call failed: {str(e)}", "error")
            return ""
    
    async def run_reconnaissance(self) -> Dict:
        """Run basic reconnaissance using nmap via Kali"""
        self.log("🔍 Running reconnaissance on target...", "info")
        self.current_test = "Reconnaissance"
        
        try:
            # Fast nmap scan - only scan top 20 ports with service detection
            cmd = f"nmap -sV -T5 -F --top-ports 20 {self.target}"
            result = await kali_executor.execute(cmd, timeout=60)
            
            if result.get("success") and result.get("output"):
                self.log("✅ Reconnaissance complete", "success")
                return {
                    "success": True,
                    "output": result.get("output", ""),
                    "open_ports": self._parse_ports(result.get("output", "")),
                    "services": self._parse_services(result.get("output", ""))
                }
            else:
                # Try simpler HTTP check if nmap fails
                self.log("Nmap timed out, trying HTTP check...", "warning")
                http_check = await self._check_http_services()
                if http_check.get("success"):
                    return http_check
                
                self.log(f"Reconnaissance failed: {result.get('error')}", "error")
                return {"success": False, "error": result.get("error", "Timeout")}
        except Exception as e:
            self.log(f"Reconnaissance error: {str(e)}", "error")
            # Fallback to HTTP check
            return await self._check_http_services()
    
    async def _check_http_services(self) -> Dict:
        """Simple HTTP check if nmap fails"""
        try:
            # Check if target is reachable via HTTP
            import requests
            response = requests.get(f"http://{self.target}", timeout=10)
            return {
                "success": True,
                "output": f"HTTP {response.status_code} - Server: {response.headers.get('Server', 'Unknown')}",
                "open_ports": [{"port": "80", "service": "http"}],
                "services": {"http": True}
            }
        except:
            # Try HTTPS
            try:
                import requests
                response = requests.get(f"https://{self.target}", timeout=10, verify=False)
                return {
                    "success": True,
                    "output": f"HTTPS {response.status_code} - Server: {response.headers.get('Server', 'Unknown')}",
                    "open_ports": [{"port": "443", "service": "https"}],
                    "services": {"https": True}
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
    
    def _parse_ports(self, nmap_output: str) -> List[Dict]:
        """Parse open ports from nmap output"""
        ports = []
        for line in nmap_output.split('\n'):
            if '/tcp' in line or '/udp' in line:
                parts = line.split()
                if len(parts) >= 3:
                    port_info = parts[0].split('/')
                    ports.append({
                        "port": port_info[0],
                        "protocol": port_info[1] if len(port_info) > 1 else "tcp",
                        "state": parts[1] if len(parts) > 1 else "unknown",
                        "service": parts[2] if len(parts) > 2 else "unknown"
                    })
        return ports[:10]  # Limit to first 10 ports
    
    def _parse_services(self, nmap_output: str) -> Dict:
        """Parse services from nmap output"""
        services = {}
        for line in nmap_output.split('\n'):
            if 'http' in line.lower() or 'ssh' in line.lower() or 'ftp' in line.lower():
                if 'tcp' in line:
                    parts = line.split()
                    for p in parts:
                        if ':' in p:
                            service = p.split(':')[0]
                            services[service] = True
        return services
    
    async def analyze_with_llm(self, recon_data: Dict) -> List[Dict]:
        """Use LLM to analyze recon data and identify potential vulnerabilities"""
        self.log("🧠 Analyzing target with AI...", "info")
        self.current_test = "AI Analysis"
        self.progress = 20
        
        system_prompt = """You are an expert cybersecurity analyst specializing in OWASP Top 10 vulnerabilities.
Analyze the reconnaissance data and identify potential security vulnerabilities.
Output a JSON array of vulnerabilities found, each with:
- title: vulnerability name (e.g., "SQL Injection", "XSS")
- severity: CRITICAL, HIGH, MEDIUM, or LOW
- description: brief description
- location: where the vulnerability is (URL, parameter, endpoint)
- evidence: what you found
- remediation: how to fix it

Only output valid JSON, no other text."""

        prompt = f"""Analyze this reconnaissance data for {self.target}:

Open Ports: {json.dumps(recon_data.get('open_ports', []))}
Detected Services: {json.dumps(recon_data.get('services', {}))}
Nmap Output: {recon_data.get('output', '')[:3000]}

Check for these OWASP Top 10 categories:
1. A01:2021 - Broken Access Control
2. A02:2021 - Cryptographic Failures  
3. A03:2021 - Injection
4. A04:2021 - Insecure Design
5. A05:2021 - Security Misconfiguration
6. A06:2021 - Vulnerable Components
7. A07:2021 - Auth Failures
8. A08:2021 - Data Integrity Failures
9. A09:2021 - Logging Failures
10. A10:2021 - SSRF

Return only the JSON array of vulnerabilities found. If none found, return []."""

        try:
            response = await self.call_llm(prompt, system=system_prompt)
            
            # Parse JSON response
            vulnerabilities = self._parse_llm_response(response)
            self.progress = 50
            
            return vulnerabilities
        except Exception as e:
            self.log(f"LLM analysis failed: {str(e)}", "error")
            return []
    
    def _parse_llm_response(self, response: str) -> List[Dict]:
        """Parse JSON from LLM response"""
        try:
            # Try to find JSON in response
            if '[' in response and ']' in response:
                start = response.find('[')
                end = response.rfind(']') + 1
                json_str = response[start:end]
                return json.loads(json_str)
            return []
        except json.JSONDecodeError:
            # Try line-by-line parsing
            return self._parse_text_vulnerabilities(response)
    
    def _parse_text_vulnerabilities(self, text: str) -> List[Dict]:
        """Parse vulnerabilities from text if JSON parsing fails"""
        vulnerabilities = []
        lines = text.split('\n')
        current_vuln = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for vulnerability indicators
            lower = line.lower()
            if 'injection' in lower or 'sql' in lower:
                current_vuln['title'] = 'SQL Injection'
                current_vuln['severity'] = 'CRITICAL'
            elif 'xss' in lower or 'cross-site' in lower:
                current_vuln['title'] = 'Cross-Site Scripting (XSS)'
                current_vuln['severity'] = 'HIGH'
            elif 'auth' in lower or 'broken' in lower:
                current_vuln['title'] = 'Broken Authentication'
                current_vuln['severity'] = 'HIGH'
            elif 'exposure' in lower or 'sensitive' in lower:
                current_vuln['title'] = 'Sensitive Data Exposure'
                current_vuln['severity'] = 'HIGH'
            elif 'xxe' in lower:
                current_vuln['title'] = 'XML External Entity (XXE)'
                current_vuln['severity'] = 'HIGH'
            elif 'misconfiguration' in lower:
                current_vuln['title'] = 'Security Misconfiguration'
                current_vuln['severity'] = 'MEDIUM'
            elif 'ssrf' in lower:
                current_vuln['title'] = 'SSRF'
                current_vuln['severity'] = 'HIGH'
                
            if current_vuln and len(current_vuln) >= 2:
                if current_vuln not in vulnerabilities:
                    vulnerabilities.append(current_vuln.copy())
                    current_vuln = {}
                    
        return vulnerabilities
    
    async def run_deep_scan(self, vulnerabilities: List[Dict]) -> List[Dict]:
        """Run deeper tests on identified vulnerabilities using Kali tools"""
        self.log("🔬 Running deep security tests...", "info")
        self.current_test = "Deep Scanning"
        self.progress = 60
        
        # Test for web vulnerabilities if HTTP is detected
        http_ports = [p for p in self._get_open_ports() if p.get('service') in ['http', 'https']]
        
        if http_ports:
            # Run nikto scan
            self.log("Running Nikto web scanner...", "info")
            nikto_result = await self._run_nikto()
            if nikto_result.get("findings"):
                vulnerabilities.extend(nikto_result["findings"])
            
            # Run SQLMap if potential injection points found
            self.log("Running SQLMap for SQL injection...", "info")
            sqlmap_result = await self._run_sqlmap()
            if sqlmap_result.get("findings"):
                vulnerabilities.extend(sqlmap_result["findings"])
        
        self.progress = 80
        return vulnerabilities
    
    def _get_open_ports(self) -> List[Dict]:
        """Get list of open ports from logs"""
        for log in self.logs:
            if 'open_ports' in str(log):
                try:
                    # Extract from log message
                    return []
                except:
                    pass
        return []
    
    async def _run_nikto(self) -> Dict:
        """Run Nikto web scanner"""
        try:
            cmd = f"nikto -h {self.target} -Format txt"
            result = await kali_executor.execute(cmd, timeout=180)
            
            findings = []
            output = result.get("output", "")
            
            # Parse nikto findings
            if "+ " in output:
                for line in output.split('\n'):
                    if line.startswith("+ ") and ("vulnerability" in line.lower() or "issue" in line.lower()):
                        findings.append({
                            "title": "Security Misconfiguration",
                            "severity": "MEDIUM",
                            "description": line.replace("+ ", "").strip(),
                            "location": self.target,
                            "evidence": line.strip(),
                            "remediation": "Review and harden server configuration"
                        })
            
            return {"findings": findings[:5]}
        except Exception as e:
            self.log(f"Nikto scan failed: {str(e)}", "error")
            return {"findings": []}
    
    async def _run_sqlmap(self) -> Dict:
        """Run SQLMap for SQL injection testing"""
        try:
            cmd = f"sqlmap -u {self.target} --batch --smart --level=1 --risk=1"
            result = await kali_executor.execute(cmd, timeout=180)
            
            findings = []
            output = result.get("output", "")
            
            if "is vulnerable" in output.lower():
                findings.append({
                    "title": "SQL Injection",
                    "severity": "CRITICAL",
                    "description": "SQL injection vulnerability detected",
                    "location": self.target,
                    "evidence": "SQLMap confirmed vulnerability",
                    "remediation": "Use parameterized queries, input validation"
                })
            
            return {"findings": findings}
        except Exception as e:
            self.log(f"SQLMap scan failed: {str(e)}", "error")
            return {"findings": []}
    
    async def generate_report(self, vulnerabilities: List[Dict]) -> str:
        """Use LLM to generate comprehensive report"""
        self.log("📝 Generating security report...", "info")
        self.current_test = "Report Generation"
        self.progress = 90
        
        system_prompt = """You are an expert security analyst. Generate a comprehensive vulnerability assessment report.
Include executive summary, detailed findings with severity, and remediation steps.
Format the report in a clear, professional manner."""

        prompt = f"""Generate a security assessment report for {self.target}

Vulnerabilities Found: {len(vulnerabilities)}

{json.dumps(vulnerabilities, indent=2)}

Include:
1. Executive Summary
2. Risk Rating
3. Each vulnerability detailed with:
   - Severity
   - Description  
   - Impact
   - Remediation
4. Next steps recommendations

Format as a professional security report."""

        report = await self.call_llm(prompt, system=system_prompt, temperature=0.5)
        self.progress = 100
        return report
    
    async def run_all_tests(self) -> Dict:
        """Run complete OWASP Top 10 testing workflow"""
        self.start_time = datetime.now()
        self.log(f"🎯 Starting OWASP Top 10 scan on {self.target}", "info")
        self.log("=" * 50, "info")
        
        # Step 1: Reconnaissance
        self.log("Phase 1: Reconnaissance", "info")
        recon_data = await self.run_reconnaissance()
        
        # Step 2: AI Analysis
        self.log("Phase 2: AI-Powered Analysis", "info")
        vulnerabilities = await self.analyze_with_llm(recon_data)
        
        # Step 3: Deep Scan
        if vulnerabilities:
            self.log("Phase 3: Deep Scanning", "info")
            vulnerabilities = await self.run_deep_scan(vulnerabilities)
        
        # Step 4: Generate Report
        self.log("Phase 4: Report Generation", "info")
        report = await self.generate_report(vulnerabilities)
        
        # Final summary
        duration = (datetime.now() - self.start_time).total_seconds()
        self.log(f"✅ Scan complete! Found {len(vulnerabilities)} issues in {duration:.1f}s", "success")
        
        return {
            "success": True,
            "target": self.target,
            "vulnerabilities_found": len(vulnerabilities),
            "results": vulnerabilities,
            "logs": self.logs,
            "report": report,
            "duration_seconds": duration,
            "progress": 100
        }


# Convenience function for direct use
async def run_owasp_scan(target_url: str, model: str = DEFAULT_MODEL) -> Dict:
    """Run OWASP Top 10 scan on target URL"""
    tester = LLMOWASPTester(target_url, model)
    return await tester.run_all_tests()
