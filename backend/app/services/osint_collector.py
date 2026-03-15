import asyncio
import subprocess
import re
import socket
from typing import List, Dict, Optional
import whois
import dns.resolver
import requests

class OSINTCollector:
    """OSINT collection service for reconnaissance"""
    
    def __init__(self):
        self.timeout = 30
        
    async def harvest_emails(self, domain: str) -> List[str]:
        """Harvest emails from domain using theHarvester"""
        try:
            cmd = f"theHarvester -d {domain} -b all -l 100"
            result = await self._execute_command(cmd)
            
            # Extract emails using regex
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', result)
            return list(set(emails))
        except Exception as e:
            return []
    
    async def whois_lookup(self, domain: str) -> Dict:
        """Perform WHOIS lookup"""
        try:
            w = whois.whois(domain)
            return {
                "domain": domain,
                "registrar": w.registrar,
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date),
                "name_servers": w.name_servers,
                "status": w.status,
                "emails": w.emails,
                "org": w.org,
                "address": w.address,
                "city": w.city,
                "state": w.state,
                "country": w.country
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def subdomain_enum(self, domain: str) -> List[str]:
        """Enumerate subdomains using multiple methods"""
        subdomains = set()
        
        # Method 1: DNS brute force with common subdomains
        common_subs = ['www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'test', 'api', 'staging']
        for sub in common_subs:
            try:
                full_domain = f"{sub}.{domain}"
                socket.gethostbyname(full_domain)
                subdomains.add(full_domain)
            except:
                pass
        
        # Method 2: Use sublist3r if available
        try:
            cmd = f"sublist3r -d {domain} -n"
            result = await self._execute_command(cmd)
            found = re.findall(r'([a-zA-Z0-9.-]+\.' + re.escape(domain) + ')', result)
            subdomains.update(found)
        except:
            pass
        
        return list(subdomains)
    
    async def find_social_profiles(self, name: str) -> List[Dict]:
        """Find social media profiles using Sherlock"""
        try:
            cmd = f"sherlock {name} --timeout 10"
            result = await self._execute_command(cmd)
            
            profiles = []
            lines = result.split('\n')
            for line in lines:
                if 'http' in line:
                    match = re.search(r'(https?://[^\s]+)', line)
                    if match:
                        url = match.group(1)
                        platform = url.split('/')[2].replace('www.', '')
                        profiles.append({
                            "platform": platform,
                            "url": url,
                            "username": name
                        })
            
            return profiles
        except Exception as e:
            return []
    
    async def get_ip_info(self, target: str) -> Dict:
        """Get IP information"""
        try:
            # Resolve domain to IP if needed
            if not self._is_ip(target):
                ip = socket.gethostbyname(target)
            else:
                ip = target
            
            # Get geolocation info
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = response.json()
            
            return {
                "ip": ip,
                "country": data.get("country"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "isp": data.get("isp"),
                "org": data.get("org"),
                "as": data.get("as"),
                "lat": data.get("lat"),
                "lon": data.get("lon")
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def gather_full_osint(self, target: str) -> Dict:
        """Gather comprehensive OSINT on target"""
        results = {
            "target": target,
            "emails": [],
            "subdomains": [],
            "whois": {},
            "ip_info": {},
            "dns_records": {}
        }
        
        # Determine if target is domain or email
        if '@' in target:
            domain = target.split('@')[1]
            results["emails"] = [target]
        else:
            domain = target
            results["emails"] = await self.harvest_emails(domain)
        
        # Gather all OSINT
        results["whois"] = await self.whois_lookup(domain)
        results["subdomains"] = await self.subdomain_enum(domain)
        results["ip_info"] = await self.get_ip_info(domain)
        results["dns_records"] = await self._get_dns_records(domain)
        
        return results
    
    async def _get_dns_records(self, domain: str) -> Dict:
        """Get DNS records"""
        records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(rdata) for rdata in answers]
            except:
                records[record_type] = []
        
        return records
    
    async def _execute_command(self, cmd: str) -> str:
        """Execute shell command asynchronously"""
        try:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.timeout
            )
            return stdout.decode()
        except asyncio.TimeoutError:
            return ""
        except Exception as e:
            return ""
    
    def _is_ip(self, target: str) -> bool:
        """Check if target is IP address"""
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        return bool(re.match(pattern, target))

# Singleton instance
osint_collector = OSINTCollector()
