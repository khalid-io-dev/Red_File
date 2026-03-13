from typing import Dict, Any, List
import re
import json

class ResultParser:
    @staticmethod
    def parse_nmap(output: str) -> Dict[str, Any]:
        ports = []
        for line in output.split('\n'):
            if '/tcp' in line or '/udp' in line:
                parts = line.split()
                if len(parts) >= 3:
                    ports.append({
                        'port': parts[0].split('/')[0],
                        'protocol': parts[0].split('/')[1] if '/' in parts[0] else 'tcp',
                        'state': parts[1],
                        'service': parts[2] if len(parts) > 2 else 'unknown',
                        'version': ' '.join(parts[3:]) if len(parts) > 3 else ''
                    })
        
        return {
            'open_ports': ports,
            'total_open': len(ports),
            'severity': 'Medium' if len(ports) > 10 else 'Low'
        }
    
    @staticmethod
    def parse_sqlmap(output: str) -> Dict[str, Any]:
        vulnerable = 'is vulnerable' in output.lower() or 'injectable' in output.lower()
        injection_type = None
        
        if 'boolean-based blind' in output.lower():
            injection_type = 'Boolean-based blind'
        elif 'time-based blind' in output.lower():
            injection_type = 'Time-based blind'
        elif 'error-based' in output.lower():
            injection_type = 'Error-based'
        elif 'union query' in output.lower():
            injection_type = 'UNION query'
        
        return {
            'vulnerable': vulnerable,
            'type': injection_type,
            'severity': 'Critical' if vulnerable else 'None',
            'exploitable': vulnerable
        }
    
    @staticmethod
    def parse_hydra(output: str) -> Dict[str, Any]:
        creds = []
        for line in output.split('\n'):
            if 'login:' in line and 'password:' in line:
                match = re.search(r'login:\s*(\S+)\s+password:\s*(\S+)', line)
                if match:
                    creds.append({
                        'username': match.group(1),
                        'password': match.group(2)
                    })
        
        return {
            'credentials_found': creds,
            'count': len(creds),
            'severity': 'Critical' if creds else 'None',
            'exploitable': len(creds) > 0
        }
    
    @staticmethod
    def parse_nikto(output: str) -> Dict[str, Any]:
        vulns = []
        for line in output.split('\n'):
            if 'OSVDB-' in line or '+ ' in line:
                vulns.append(line.strip())
        
        return {
            'vulnerabilities': vulns[:10],  # Top 10
            'total_vulns': len(vulns),
            'severity': 'High' if len(vulns) > 5 else 'Medium' if len(vulns) > 0 else 'Low'
        }
    
    @staticmethod
    def parse_gobuster(output: str) -> Dict[str, Any]:
        found = []
        for line in output.split('\n'):
            if 'Status: 200' in line or 'Status: 301' in line or 'Status: 302' in line:
                parts = line.split()
                if len(parts) >= 1:
                    found.append({
                        'path': parts[0],
                        'status': parts[parts.index('Status:') + 1] if 'Status:' in parts else 'unknown'
                    })
        
        return {
            'directories_found': found,
            'count': len(found),
            'severity': 'Medium' if any('admin' in f['path'].lower() or 'backup' in f['path'].lower() for f in found) else 'Low'
        }
    
    @staticmethod
    def parse_theharvester(output: str) -> Dict[str, Any]:
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', output)
        hosts = re.findall(r'\[[\*\+]\]\s+([\w\.-]+)', output)
        
        return {
            'emails': list(set(emails)),
            'hosts': list(set(hosts)),
            'email_count': len(set(emails)),
            'host_count': len(set(hosts)),
            'severity': 'Low'
        }
    
    @staticmethod
    def parse_wpscan(output: str) -> Dict[str, Any]:
        vulns = output.count('[!]')
        plugins = output.count('| Name:')
        
        return {
            'vulnerabilities': vulns,
            'plugins_found': plugins,
            'severity': 'High' if vulns > 5 else 'Medium' if vulns > 0 else 'Low',
            'wordpress_detected': 'WordPress' in output
        }
    
    @staticmethod
    def parse(tool_name: str, output: str) -> Dict[str, Any]:
        parsers = {
            'nmap': ResultParser.parse_nmap,
            'sqlmap': ResultParser.parse_sqlmap,
            'hydra': ResultParser.parse_hydra,
            'nikto': ResultParser.parse_nikto,
            'gobuster': ResultParser.parse_gobuster,
            'theharvester': ResultParser.parse_theharvester,
            'wpscan': ResultParser.parse_wpscan,
        }
        
        parser = parsers.get(tool_name)
        if parser:
            try:
                return parser(output)
            except Exception as e:
                return {'error': str(e), 'raw': output[:500]}
        
        return {'raw': output[:500]}

class ResultAggregator:
    def __init__(self):
        self.findings = []
        self.parser = ResultParser()
    
    def add_result(self, tool: str, output: str, success: bool):
        parsed = self.parser.parse(tool, output)
        
        self.findings.append({
            'tool': tool,
            'success': success,
            'parsed': parsed,
            'severity': parsed.get('severity', 'Unknown')
        })
    
    def get_summary(self) -> Dict[str, Any]:
        critical = [f for f in self.findings if f['severity'] == 'Critical']
        high = [f for f in self.findings if f['severity'] == 'High']
        medium = [f for f in self.findings if f['severity'] == 'Medium']
        low = [f for f in self.findings if f['severity'] == 'Low']
        
        exploitable = [f for f in self.findings if f['parsed'].get('exploitable', False)]
        
        return {
            'total_tools_run': len(self.findings),
            'successful_tools': len([f for f in self.findings if f['success']]),
            'severity_breakdown': {
                'critical': len(critical),
                'high': len(high),
                'medium': len(medium),
                'low': len(low)
            },
            'exploitable_findings': len(exploitable),
            'critical_findings': critical,
            'high_findings': high,
            'overall_risk': self._calculate_risk()
        }
    
    def _calculate_risk(self) -> str:
        critical = len([f for f in self.findings if f['severity'] == 'Critical'])
        high = len([f for f in self.findings if f['severity'] == 'High'])
        
        if critical > 0:
            return 'Critical'
        elif high > 2:
            return 'High'
        elif high > 0:
            return 'Medium'
        else:
            return 'Low'
    
    def get_recommendations(self) -> List[str]:
        recs = []
        
        for finding in self.findings:
            if finding['severity'] in ['Critical', 'High']:
                tool = finding['tool']
                parsed = finding['parsed']
                
                if tool == 'sqlmap' and parsed.get('vulnerable'):
                    recs.append(f"URGENT: SQL Injection found ({parsed.get('type')}). Implement parameterized queries immediately.")
                elif tool == 'hydra' and parsed.get('credentials_found'):
                    recs.append(f"URGENT: Weak credentials found. Enforce strong password policy and MFA.")
                elif tool == 'nikto' and parsed.get('total_vulns', 0) > 5:
                    recs.append(f"Multiple web server vulnerabilities detected. Update server software and apply security patches.")
        
        return recs[:5]  # Top 5 recommendations
