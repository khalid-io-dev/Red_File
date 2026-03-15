from typing import List, Dict, Any
import json
from collections import Counter

class VulnerabilityPredictor:
    def __init__(self):
        self.vulnerability_patterns = {
            "sql_injection": ["login", "search", "id", "user", "admin", "query"],
            "xss": ["comment", "message", "post", "input", "search"],
            "rce": ["upload", "file", "cmd", "exec", "system"],
            "lfi": ["file", "path", "page", "include", "load"],
            "ssrf": ["url", "proxy", "fetch", "redirect", "callback"],
        }
        
        self.port_vulnerabilities = {
            21: ["ftp_anonymous", "ftp_bounce"],
            22: ["ssh_weak_ciphers", "ssh_brute_force"],
            23: ["telnet_cleartext"],
            80: ["http_methods", "directory_listing"],
            443: ["ssl_weak_cipher", "ssl_expired_cert"],
            3306: ["mysql_default_creds", "mysql_remote_access"],
            3389: ["rdp_bluekeep", "rdp_brute_force"],
            5432: ["postgres_default_creds"],
            6379: ["redis_unauth"],
            27017: ["mongodb_unauth"],
        }
    
    def predict_vulnerabilities(self, target_data: Dict) -> List[Dict]:
        predictions = []
        
        # Analyze open ports
        if "ports" in target_data:
            for port in target_data["ports"]:
                port_num = port.get("port")
                if port_num in self.port_vulnerabilities:
                    for vuln in self.port_vulnerabilities[port_num]:
                        predictions.append({
                            "vulnerability": vuln,
                            "confidence": 0.7,
                            "port": port_num,
                            "severity": self._get_severity(vuln),
                            "recommended_tool": self._get_tool_for_vuln(vuln)
                        })
        
        # Analyze URLs/endpoints
        if "urls" in target_data:
            for url in target_data["urls"]:
                for vuln_type, keywords in self.vulnerability_patterns.items():
                    if any(kw in url.lower() for kw in keywords):
                        predictions.append({
                            "vulnerability": vuln_type,
                            "confidence": 0.6,
                            "location": url,
                            "severity": self._get_severity(vuln_type),
                            "recommended_tool": self._get_tool_for_vuln(vuln_type)
                        })
        
        # Analyze technologies
        if "technologies" in target_data:
            tech_vulns = self._predict_from_technologies(target_data["technologies"])
            predictions.extend(tech_vulns)
        
        return sorted(predictions, key=lambda x: x["confidence"], reverse=True)
    
    def calculate_risk_score(self, findings: List[Dict]) -> Dict:
        severity_weights = {
            "critical": 10,
            "high": 7,
            "medium": 4,
            "low": 1,
            "info": 0
        }
        
        total_score = sum(severity_weights.get(f.get("severity", "info"), 0) for f in findings)
        
        return {
            "total_score": total_score,
            "risk_level": self._calculate_risk_level(total_score),
            "severity_distribution": Counter(f.get("severity") for f in findings),
            "most_common_vulns": Counter(f.get("title") for f in findings).most_common(5)
        }
    
    def suggest_next_tools(self, current_findings: List[Dict], available_tools: List[str]) -> List[Dict]:
        suggestions = []
        
        # If SQL injection found, suggest sqlmap
        if any("sql" in f.get("title", "").lower() for f in current_findings):
            if "sqlmap" in available_tools:
                suggestions.append({
                    "tool": "sqlmap",
                    "reason": "SQL injection detected, deep exploitation recommended",
                    "priority": "high"
                })
        
        # If weak creds found, suggest privilege escalation
        if any("credential" in f.get("title", "").lower() for f in current_findings):
            if "metasploit" in available_tools:
                suggestions.append({
                    "tool": "metasploit",
                    "reason": "Valid credentials found, attempt exploitation",
                    "priority": "high"
                })
        
        # If open ports found, suggest service-specific tools
        if any("port" in f.get("title", "").lower() for f in current_findings):
            if "nmap" in available_tools:
                suggestions.append({
                    "tool": "nmap",
                    "reason": "Perform detailed service enumeration",
                    "priority": "medium"
                })
        
        return suggestions
    
    def _get_severity(self, vuln_type: str) -> str:
        critical = ["rce", "sql_injection", "rdp_bluekeep"]
        high = ["xss", "lfi", "ssrf", "ftp_bounce"]
        
        if any(c in vuln_type for c in critical):
            return "critical"
        elif any(h in vuln_type for h in high):
            return "high"
        else:
            return "medium"
    
    def _get_tool_for_vuln(self, vuln_type: str) -> str:
        tool_mapping = {
            "sql_injection": "sqlmap",
            "xss": "nuclei",
            "rce": "metasploit",
            "lfi": "wfuzz",
            "ssrf": "ffuf",
            "ftp": "hydra",
            "ssh": "hydra",
            "rdp": "crackmapexec",
        }
        
        for key, tool in tool_mapping.items():
            if key in vuln_type:
                return tool
        
        return "nmap"
    
    def _predict_from_technologies(self, technologies: List[str]) -> List[Dict]:
        predictions = []
        
        tech_vulns = {
            "wordpress": [("wp_plugin_vuln", 0.8, "wpscan")],
            "apache": [("apache_struts", 0.6, "metasploit")],
            "nginx": [("nginx_misconfig", 0.5, "nikto")],
            "php": [("php_rce", 0.7, "commix")],
            "mysql": [("mysql_injection", 0.7, "sqlmap")],
        }
        
        for tech in technologies:
            tech_lower = tech.lower()
            for key, vulns in tech_vulns.items():
                if key in tech_lower:
                    for vuln, conf, tool in vulns:
                        predictions.append({
                            "vulnerability": vuln,
                            "confidence": conf,
                            "technology": tech,
                            "severity": "high",
                            "recommended_tool": tool
                        })
        
        return predictions
    
    def _calculate_risk_level(self, score: int) -> str:
        if score >= 50:
            return "Critical"
        elif score >= 30:
            return "High"
        elif score >= 15:
            return "Medium"
        else:
            return "Low"

ml_predictor = VulnerabilityPredictor()
