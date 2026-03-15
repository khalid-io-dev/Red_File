import requests
import socket
import hashlib
from typing import Dict, List
import re

class IOCAnalyzer:
    """Analyze Indicators of Compromise"""
    
    def __init__(self):
        self.timeout = 10
    
    async def analyze_ip(self, ip: str) -> Dict:
        """Analyze IP address"""
        result = {
            "ioc": ip,
            "type": "ip",
            "malicious": False,
            "risk_score": 0,
            "details": {}
        }
        
        try:
            # Geolocation
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                result["details"]["geolocation"] = {
                    "country": data.get("country"),
                    "region": data.get("regionName"),
                    "city": data.get("city"),
                    "isp": data.get("isp"),
                    "org": data.get("org"),
                    "as": data.get("as")
                }
            
            # Reverse DNS
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                result["details"]["hostname"] = hostname
            except:
                result["details"]["hostname"] = None
            
            # Check if IP is in known malicious ranges
            if self._is_suspicious_ip(ip):
                result["malicious"] = True
                result["risk_score"] = 80
                result["details"]["reason"] = "IP in suspicious range"
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    async def analyze_domain(self, domain: str) -> Dict:
        """Analyze domain"""
        result = {
            "ioc": domain,
            "type": "domain",
            "malicious": False,
            "risk_score": 0,
            "details": {}
        }
        
        try:
            # DNS resolution
            try:
                ip = socket.gethostbyname(domain)
                result["details"]["ip"] = ip
            except:
                result["details"]["ip"] = None
                result["risk_score"] += 20
                result["details"]["warnings"] = ["Domain does not resolve"]
            
            # Check domain age and registration
            result["details"]["suspicious_patterns"] = self._check_domain_patterns(domain)
            
            # Calculate risk score
            if result["details"]["suspicious_patterns"]:
                result["risk_score"] += len(result["details"]["suspicious_patterns"]) * 15
            
            if result["risk_score"] >= 50:
                result["malicious"] = True
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    async def analyze_hash(self, file_hash: str) -> Dict:
        """Analyze file hash"""
        result = {
            "ioc": file_hash,
            "type": "hash",
            "malicious": False,
            "risk_score": 0,
            "details": {}
        }
        
        # Identify hash type
        hash_len = len(file_hash)
        if hash_len == 32:
            result["details"]["hash_type"] = "MD5"
        elif hash_len == 40:
            result["details"]["hash_type"] = "SHA1"
        elif hash_len == 64:
            result["details"]["hash_type"] = "SHA256"
        else:
            result["details"]["hash_type"] = "Unknown"
            return result
        
        # Simulate VirusTotal check (requires API key in production)
        result["details"]["detection_rate"] = "0/70"
        result["details"]["last_analysis"] = "Not analyzed"
        
        return result
    
    async def analyze_url(self, url: str) -> Dict:
        """Analyze URL"""
        result = {
            "ioc": url,
            "type": "url",
            "malicious": False,
            "risk_score": 0,
            "details": {}
        }
        
        try:
            # Parse URL
            from urllib.parse import urlparse
            parsed = urlparse(url)
            
            result["details"]["scheme"] = parsed.scheme
            result["details"]["domain"] = parsed.netloc
            result["details"]["path"] = parsed.path
            
            # Check for suspicious patterns
            suspicious_patterns = []
            
            if parsed.scheme == "http":
                suspicious_patterns.append("Unencrypted HTTP")
                result["risk_score"] += 10
            
            if any(keyword in url.lower() for keyword in ["login", "admin", "password", "bank"]):
                suspicious_patterns.append("Sensitive keywords in URL")
                result["risk_score"] += 20
            
            if len(parsed.netloc) > 50:
                suspicious_patterns.append("Unusually long domain")
                result["risk_score"] += 15
            
            if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', parsed.netloc):
                suspicious_patterns.append("IP address instead of domain")
                result["risk_score"] += 25
            
            result["details"]["suspicious_patterns"] = suspicious_patterns
            
            if result["risk_score"] >= 50:
                result["malicious"] = True
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    async def batch_analyze(self, iocs: List[str]) -> List[Dict]:
        """Analyze multiple IOCs"""
        results = []
        
        for ioc in iocs:
            ioc_type = self._identify_ioc_type(ioc)
            
            if ioc_type == "ip":
                result = await self.analyze_ip(ioc)
            elif ioc_type == "domain":
                result = await self.analyze_domain(ioc)
            elif ioc_type == "hash":
                result = await self.analyze_hash(ioc)
            elif ioc_type == "url":
                result = await self.analyze_url(ioc)
            else:
                result = {"ioc": ioc, "type": "unknown", "error": "Unknown IOC type"}
            
            results.append(result)
        
        return results
    
    async def correlate_iocs(self, iocs: List[str]) -> Dict:
        """Find correlations between IOCs"""
        correlations = {
            "iocs": iocs,
            "relationships": [],
            "clusters": []
        }
        
        # Analyze all IOCs
        analyzed = await self.batch_analyze(iocs)
        
        # Find relationships
        for i, ioc1 in enumerate(analyzed):
            for ioc2 in analyzed[i+1:]:
                # Check if IPs resolve to same domain
                if ioc1["type"] == "ip" and ioc2["type"] == "domain":
                    if ioc1["details"].get("hostname") == ioc2["ioc"]:
                        correlations["relationships"].append({
                            "ioc1": ioc1["ioc"],
                            "ioc2": ioc2["ioc"],
                            "relationship": "IP resolves to domain"
                        })
                
                # Check if domains share same IP
                if ioc1["type"] == "domain" and ioc2["type"] == "domain":
                    if ioc1["details"].get("ip") == ioc2["details"].get("ip"):
                        correlations["relationships"].append({
                            "ioc1": ioc1["ioc"],
                            "ioc2": ioc2["ioc"],
                            "relationship": "Domains share same IP"
                        })
        
        return correlations
    
    # Helper methods
    
    def _identify_ioc_type(self, ioc: str) -> str:
        """Identify IOC type"""
        # IP address
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ioc):
            return "ip"
        
        # Hash (MD5, SHA1, SHA256)
        if re.match(r'^[a-fA-F0-9]{32}$', ioc):
            return "hash"
        if re.match(r'^[a-fA-F0-9]{40}$', ioc):
            return "hash"
        if re.match(r'^[a-fA-F0-9]{64}$', ioc):
            return "hash"
        
        # URL
        if ioc.startswith(('http://', 'https://', 'ftp://')):
            return "url"
        
        # Domain
        if '.' in ioc and not '/' in ioc:
            return "domain"
        
        return "unknown"
    
    def _is_suspicious_ip(self, ip: str) -> bool:
        """Check if IP is in suspicious range"""
        # Check for private IPs
        parts = [int(p) for p in ip.split('.')]
        
        # Private ranges
        if parts[0] == 10:
            return False
        if parts[0] == 172 and 16 <= parts[1] <= 31:
            return False
        if parts[0] == 192 and parts[1] == 168:
            return False
        
        # Known malicious ranges (example)
        suspicious_ranges = [
            (185, 220, 100, 0),  # Example range
            (45, 142, 120, 0)    # Example range
        ]
        
        for suspicious in suspicious_ranges:
            if parts[0] == suspicious[0] and parts[1] == suspicious[1]:
                return True
        
        return False
    
    def _check_domain_patterns(self, domain: str) -> List[str]:
        """Check for suspicious domain patterns"""
        patterns = []
        
        # Long domain
        if len(domain) > 50:
            patterns.append("Unusually long domain name")
        
        # Many subdomains
        if domain.count('.') > 3:
            patterns.append("Multiple subdomains")
        
        # Numbers in domain
        if any(char.isdigit() for char in domain):
            patterns.append("Contains numbers")
        
        # Suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top']
        if any(domain.endswith(tld) for tld in suspicious_tlds):
            patterns.append("Suspicious TLD")
        
        # Homograph attack (lookalike characters)
        if any(char in domain for char in ['ı', 'ł', 'ο', 'а']):
            patterns.append("Possible homograph attack")
        
        return patterns

# Singleton instance
ioc_analyzer = IOCAnalyzer()
