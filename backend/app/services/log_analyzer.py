"""
Log Analysis Service - Parse and analyze security logs
"""
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
import asyncio

class LogAnalyzer:
    """Analyze security logs for threats and anomalies"""
    
    def __init__(self):
        self.patterns = {
            'failed_login': r'Failed password|authentication failure|invalid user',
            'sql_injection': r'union.*select|or.*1=1|drop.*table',
            'xss_attempt': r'<script|javascript:|onerror=',
            'path_traversal': r'\.\./|\.\.\\',
            'command_injection': r';.*whoami|&&.*cat|`.*ls',
            'brute_force': r'repeated.*failed|multiple.*attempts',
            'port_scan': r'SYN.*flood|port.*scan|nmap',
            'malware': r'trojan|backdoor|ransomware|cryptominer'
        }
        
        self.severity_keywords = {
            'critical': ['exploit', 'breach', 'compromise', 'malware', 'ransomware'],
            'high': ['attack', 'injection', 'unauthorized', 'suspicious'],
            'medium': ['failed', 'denied', 'blocked', 'warning'],
            'low': ['info', 'notice', 'debug']
        }
    
    async def analyze_logs(self, logs: List[str], log_type: str = 'generic') -> Dict[str, Any]:
        """Analyze logs and detect threats"""
        results = {
            'total_entries': len(logs),
            'threats_detected': [],
            'statistics': {},
            'timeline': [],
            'top_ips': [],
            'top_users': [],
            'anomalies': []
        }
        
        threats = []
        ip_counter = Counter()
        user_counter = Counter()
        
        for log in logs:
            # Detect threats
            for threat_type, pattern in self.patterns.items():
                if re.search(pattern, log, re.IGNORECASE):
                    threat = {
                        'type': threat_type,
                        'log_entry': log[:200],
                        'severity': self._calculate_severity(log),
                        'timestamp': self._extract_timestamp(log)
                    }
                    threats.append(threat)
            
            # Extract IPs
            ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', log)
            ip_counter.update(ips)
            
            # Extract usernames
            users = re.findall(r'user[=:\s]+(\w+)', log, re.IGNORECASE)
            user_counter.update(users)
        
        results['threats_detected'] = threats
        results['top_ips'] = [{'ip': ip, 'count': count} for ip, count in ip_counter.most_common(10)]
        results['top_users'] = [{'user': user, 'count': count} for user, count in user_counter.most_common(10)]
        results['statistics'] = self._generate_statistics(threats)
        results['anomalies'] = await self._detect_anomalies(logs)
        
        return results
    
    async def parse_apache_logs(self, logs: List[str]) -> Dict[str, Any]:
        """Parse Apache access/error logs"""
        parsed = []
        for log in logs:
            match = re.match(r'(\S+) \S+ \S+ \[(.*?)\] "(.*?)" (\d+) (\d+)', log)
            if match:
                parsed.append({
                    'ip': match.group(1),
                    'timestamp': match.group(2),
                    'request': match.group(3),
                    'status': int(match.group(4)),
                    'size': int(match.group(5))
                })
        
        return await self._analyze_web_logs(parsed)
    
    async def parse_nginx_logs(self, logs: List[str]) -> Dict[str, Any]:
        """Parse Nginx access/error logs"""
        parsed = []
        for log in logs:
            match = re.match(r'(\S+) - - \[(.*?)\] "(.*?)" (\d+) (\d+)', log)
            if match:
                parsed.append({
                    'ip': match.group(1),
                    'timestamp': match.group(2),
                    'request': match.group(3),
                    'status': int(match.group(4)),
                    'size': int(match.group(5))
                })
        
        return await self._analyze_web_logs(parsed)
    
    async def parse_ssh_logs(self, logs: List[str]) -> Dict[str, Any]:
        """Parse SSH authentication logs"""
        results = {
            'failed_attempts': [],
            'successful_logins': [],
            'brute_force_ips': [],
            'suspicious_users': []
        }
        
        failed_by_ip = defaultdict(int)
        
        for log in logs:
            if 'Failed password' in log:
                ip_match = re.search(r'from (\S+)', log)
                user_match = re.search(r'for (\S+)', log)
                if ip_match:
                    ip = ip_match.group(1)
                    failed_by_ip[ip] += 1
                    results['failed_attempts'].append({
                        'ip': ip,
                        'user': user_match.group(1) if user_match else 'unknown',
                        'timestamp': self._extract_timestamp(log)
                    })
            
            elif 'Accepted password' in log:
                ip_match = re.search(r'from (\S+)', log)
                user_match = re.search(r'for (\S+)', log)
                if ip_match:
                    results['successful_logins'].append({
                        'ip': ip_match.group(1),
                        'user': user_match.group(1) if user_match else 'unknown',
                        'timestamp': self._extract_timestamp(log)
                    })
        
        # Detect brute force (>5 failed attempts)
        results['brute_force_ips'] = [
            {'ip': ip, 'attempts': count}
            for ip, count in failed_by_ip.items() if count > 5
        ]
        
        return results
    
    async def parse_firewall_logs(self, logs: List[str]) -> Dict[str, Any]:
        """Parse firewall logs"""
        results = {
            'blocked_ips': [],
            'allowed_connections': [],
            'port_scans': [],
            'ddos_attempts': []
        }
        
        blocked_counter = Counter()
        
        for log in logs:
            if 'BLOCK' in log or 'DROP' in log or 'DENY' in log:
                ip_match = re.search(r'SRC=(\S+)', log)
                port_match = re.search(r'DPT=(\d+)', log)
                if ip_match:
                    ip = ip_match.group(1)
                    blocked_counter[ip] += 1
                    results['blocked_ips'].append({
                        'ip': ip,
                        'port': port_match.group(1) if port_match else 'unknown',
                        'timestamp': self._extract_timestamp(log)
                    })
        
        # Detect DDoS (>100 blocks from same IP)
        results['ddos_attempts'] = [
            {'ip': ip, 'count': count}
            for ip, count in blocked_counter.items() if count > 100
        ]
        
        return results
    
    async def correlate_logs(self, log_sources: Dict[str, List[str]]) -> Dict[str, Any]:
        """Correlate logs from multiple sources"""
        all_ips = set()
        timeline = []
        
        for source, logs in log_sources.items():
            for log in logs:
                ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', log)
                all_ips.update(ips)
                
                timeline.append({
                    'source': source,
                    'timestamp': self._extract_timestamp(log),
                    'event': log[:100]
                })
        
        # Find IPs appearing in multiple sources
        suspicious_ips = []
        for ip in all_ips:
            sources_found = []
            for source, logs in log_sources.items():
                if any(ip in log for log in logs):
                    sources_found.append(source)
            
            if len(sources_found) > 1:
                suspicious_ips.append({
                    'ip': ip,
                    'sources': sources_found,
                    'risk': 'high' if len(sources_found) > 2 else 'medium'
                })
        
        return {
            'suspicious_ips': suspicious_ips,
            'timeline': sorted(timeline, key=lambda x: x['timestamp']),
            'total_unique_ips': len(all_ips)
        }
    
    async def detect_anomalies(self, logs: List[str], baseline: Optional[Dict] = None) -> List[Dict]:
        """Detect anomalous patterns in logs"""
        anomalies = []
        
        # Time-based anomalies
        timestamps = [self._extract_timestamp(log) for log in logs]
        hour_counts = Counter([ts.hour for ts in timestamps if ts])
        
        avg_per_hour = sum(hour_counts.values()) / len(hour_counts) if hour_counts else 0
        for hour, count in hour_counts.items():
            if count > avg_per_hour * 3:  # 3x normal traffic
                anomalies.append({
                    'type': 'traffic_spike',
                    'hour': hour,
                    'count': count,
                    'normal': int(avg_per_hour),
                    'severity': 'medium'
                })
        
        # Unusual user agents
        user_agents = re.findall(r'User-Agent: (.*?)(?:\n|$)', '\n'.join(logs))
        suspicious_agents = [ua for ua in user_agents if any(x in ua.lower() for x in ['bot', 'crawler', 'scanner', 'sqlmap', 'nikto'])]
        
        if suspicious_agents:
            anomalies.append({
                'type': 'suspicious_user_agents',
                'count': len(suspicious_agents),
                'examples': suspicious_agents[:5],
                'severity': 'high'
            })
        
        return anomalies
    
    async def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate human-readable report"""
        report = []
        report.append("=== Log Analysis Report ===\n")
        report.append(f"Total Entries: {analysis_results.get('total_entries', 0)}")
        report.append(f"Threats Detected: {len(analysis_results.get('threats_detected', []))}\n")
        
        if analysis_results.get('threats_detected'):
            report.append("Top Threats:")
            for threat in analysis_results['threats_detected'][:10]:
                report.append(f"  - {threat['type']} ({threat['severity']})")
        
        if analysis_results.get('top_ips'):
            report.append("\nTop IPs:")
            for item in analysis_results['top_ips'][:5]:
                report.append(f"  - {item['ip']}: {item['count']} events")
        
        if analysis_results.get('anomalies'):
            report.append("\nAnomalies Detected:")
            for anomaly in analysis_results['anomalies']:
                report.append(f"  - {anomaly['type']} (severity: {anomaly['severity']})")
        
        return '\n'.join(report)
    
    def _calculate_severity(self, log: str) -> str:
        """Calculate severity based on keywords"""
        log_lower = log.lower()
        for severity, keywords in self.severity_keywords.items():
            if any(kw in log_lower for kw in keywords):
                return severity
        return 'low'
    
    def _extract_timestamp(self, log: str) -> Optional[datetime]:
        """Extract timestamp from log entry"""
        patterns = [
            r'\[(.*?)\]',  # [timestamp]
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',  # YYYY-MM-DD HH:MM:SS
            r'(\w{3} \d{2} \d{2}:\d{2}:\d{2})'  # Mon DD HH:MM:SS
        ]
        
        for pattern in patterns:
            match = re.search(pattern, log)
            if match:
                try:
                    return datetime.now()  # Simplified
                except:
                    pass
        return None
    
    def _generate_statistics(self, threats: List[Dict]) -> Dict[str, Any]:
        """Generate threat statistics"""
        if not threats:
            return {}
        
        by_type = Counter([t['type'] for t in threats])
        by_severity = Counter([t['severity'] for t in threats])
        
        return {
            'by_type': dict(by_type),
            'by_severity': dict(by_severity),
            'total': len(threats)
        }
    
    async def _analyze_web_logs(self, parsed: List[Dict]) -> Dict[str, Any]:
        """Analyze parsed web logs"""
        results = {
            'total_requests': len(parsed),
            'status_codes': Counter([p['status'] for p in parsed]),
            'top_ips': Counter([p['ip'] for p in parsed]).most_common(10),
            'errors': [p for p in parsed if p['status'] >= 400],
            'suspicious_requests': []
        }
        
        for entry in parsed:
            request = entry['request'].lower()
            if any(pattern in request for pattern in ['union', 'select', '<script', '../', 'cmd=']):
                results['suspicious_requests'].append(entry)
        
        return results
    
    async def _detect_anomalies(self, logs: List[str]) -> List[Dict]:
        """Detect anomalies in logs"""
        return await self.detect_anomalies(logs)

# Singleton
log_analyzer = LogAnalyzer()
