import socket
import subprocess
import ipaddress
from typing import List, Dict
import asyncio
import struct

class NetworkScanner:
    """Network security scanner"""
    
    def __init__(self):
        self.timeout = 5
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]
    
    async def port_scan(self, target: str, ports: str = "1-1000") -> List[Dict]:
        """Scan ports on target"""
        results = []
        
        try:
            # Parse port range
            if '-' in ports:
                start, end = map(int, ports.split('-'))
                port_list = range(start, end + 1)
            else:
                port_list = [int(p) for p in ports.split(',')]
            
            # Scan ports
            for port in port_list:
                if await self._check_port(target, port):
                    service = self._get_service_name(port)
                    results.append({
                        "port": port,
                        "state": "open",
                        "service": service
                    })
        
        except Exception as e:
            results.append({"error": str(e)})
        
        return results
    
    async def service_detection(self, target: str) -> List[Dict]:
        """Detect services on open ports"""
        results = []
        
        try:
            # Scan common ports first
            for port in self.common_ports:
                if await self._check_port(target, port):
                    banner = await self._grab_banner(target, port)
                    service = self._identify_service(port, banner)
                    
                    results.append({
                        "port": port,
                        "service": service["name"],
                        "version": service["version"],
                        "banner": banner
                    })
        
        except Exception as e:
            results.append({"error": str(e)})
        
        return results
    
    async def os_detection(self, target: str) -> Dict:
        """Detect operating system"""
        result = {
            "target": target,
            "os": "Unknown",
            "confidence": 0,
            "details": {}
        }
        
        try:
            # TTL-based OS detection
            ttl = await self._get_ttl(target)
            
            if ttl:
                if ttl <= 64:
                    result["os"] = "Linux/Unix"
                    result["confidence"] = 70
                elif ttl <= 128:
                    result["os"] = "Windows"
                    result["confidence"] = 70
                elif ttl <= 255:
                    result["os"] = "Cisco/Network Device"
                    result["confidence"] = 60
                
                result["details"]["ttl"] = ttl
            
            # Check for specific services
            services = await self.service_detection(target)
            for service in services:
                if "error" not in service:
                    if "microsoft" in service.get("banner", "").lower():
                        result["os"] = "Windows"
                        result["confidence"] = 90
                    elif "linux" in service.get("banner", "").lower():
                        result["os"] = "Linux"
                        result["confidence"] = 90
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    async def vulnerability_scan(self, target: str) -> List[Dict]:
        """Scan for common vulnerabilities"""
        findings = []
        
        try:
            # Check for open ports with known vulnerabilities
            services = await self.service_detection(target)
            
            for service in services:
                if "error" in service:
                    continue
                
                port = service["port"]
                service_name = service["service"]
                
                # Check for vulnerable services
                if port == 21 and "ftp" in service_name.lower():
                    findings.append({
                        "port": port,
                        "service": service_name,
                        "vulnerability": "Anonymous FTP",
                        "severity": "Medium",
                        "description": "FTP service may allow anonymous access"
                    })
                
                elif port == 23:
                    findings.append({
                        "port": port,
                        "service": service_name,
                        "vulnerability": "Telnet Enabled",
                        "severity": "High",
                        "description": "Telnet transmits data in cleartext"
                    })
                
                elif port == 445:
                    findings.append({
                        "port": port,
                        "service": service_name,
                        "vulnerability": "SMB Exposed",
                        "severity": "High",
                        "description": "SMB service exposed to network"
                    })
                
                elif port == 3389:
                    findings.append({
                        "port": port,
                        "service": service_name,
                        "vulnerability": "RDP Exposed",
                        "severity": "High",
                        "description": "Remote Desktop Protocol exposed"
                    })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    async def network_discovery(self, subnet: str) -> List[str]:
        """Discover live hosts in subnet"""
        live_hosts = []
        
        try:
            network = ipaddress.ip_network(subnet, strict=False)
            
            # Limit to /24 or smaller for performance
            if network.num_addresses > 256:
                return [{"error": "Subnet too large, use /24 or smaller"}]
            
            # Ping sweep
            for ip in network.hosts():
                if await self._ping_host(str(ip)):
                    live_hosts.append(str(ip))
        
        except Exception as e:
            live_hosts.append({"error": str(e)})
        
        return live_hosts
    
    async def trace_route(self, target: str) -> List[str]:
        """Trace route to target"""
        hops = []
        
        try:
            # Use system traceroute
            result = subprocess.run(
                ['tracert' if subprocess.os.name == 'nt' else 'traceroute', target],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            lines = result.stdout.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('Tracing'):
                    hops.append(line.strip())
        
        except Exception as e:
            hops.append(f"Error: {str(e)}")
        
        return hops
    
    async def arp_scan(self, interface: str = None) -> List[Dict]:
        """ARP scan for local network"""
        results = []
        
        try:
            cmd = ['arp', '-a']
            if interface:
                cmd.extend(['-i', interface])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            lines = result.stdout.split('\n')
            for line in lines:
                if '(' in line and ')' in line:
                    # Parse ARP output
                    parts = line.split()
                    if len(parts) >= 4:
                        results.append({
                            "ip": parts[1].strip('()'),
                            "mac": parts[3],
                            "type": parts[4] if len(parts) > 4 else "dynamic"
                        })
        
        except Exception as e:
            results.append({"error": str(e)})
        
        return results
    
    # Helper methods
    
    async def _check_port(self, target: str, port: int) -> bool:
        """Check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            return result == 0
        except:
            return False
    
    async def _grab_banner(self, target: str, port: int) -> str:
        """Grab service banner"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((target, port))
            
            # Send HTTP request for web services
            if port in [80, 8080, 443, 8443]:
                sock.send(b'GET / HTTP/1.1\r\nHost: ' + target.encode() + b'\r\n\r\n')
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            return banner
        except:
            return ""
    
    def _identify_service(self, port: int, banner: str) -> Dict:
        """Identify service from port and banner"""
        service = {"name": "unknown", "version": ""}
        
        # Port-based identification
        port_services = {
            21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
            53: "dns", 80: "http", 110: "pop3", 143: "imap",
            443: "https", 445: "smb", 3306: "mysql", 3389: "rdp",
            5432: "postgresql", 8080: "http-proxy", 8443: "https-alt"
        }
        
        service["name"] = port_services.get(port, "unknown")
        
        # Banner-based version detection
        if banner:
            if "Apache" in banner:
                service["name"] = "apache"
                version_match = banner.split("Apache/")[1].split()[0] if "Apache/" in banner else ""
                service["version"] = version_match
            elif "nginx" in banner:
                service["name"] = "nginx"
                version_match = banner.split("nginx/")[1].split()[0] if "nginx/" in banner else ""
                service["version"] = version_match
            elif "OpenSSH" in banner:
                service["name"] = "ssh"
                version_match = banner.split("OpenSSH_")[1].split()[0] if "OpenSSH_" in banner else ""
                service["version"] = version_match
        
        return service
    
    def _get_service_name(self, port: int) -> str:
        """Get service name for port"""
        try:
            return socket.getservbyport(port)
        except:
            return "unknown"
    
    async def _get_ttl(self, target: str) -> int:
        """Get TTL from ping"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', target] if subprocess.os.name != 'nt' else ['ping', '-n', '1', target],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Parse TTL from output
            for line in result.stdout.split('\n'):
                if 'ttl=' in line.lower():
                    ttl_str = line.lower().split('ttl=')[1].split()[0]
                    return int(ttl_str)
        except:
            pass
        
        return 0
    
    async def _ping_host(self, ip: str) -> bool:
        """Ping host to check if alive"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '1', ip] if subprocess.os.name != 'nt' else ['ping', '-n', '1', '-w', '1000', ip],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False

# Singleton instance
network_scanner = NetworkScanner()
