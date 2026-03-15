import asyncio
import paramiko
from typing import Dict, Optional
import os

# SSH connection settings - read from environment
KALI_HOST = os.getenv("KALI_SSH_HOST", "192.168.56.101")
KALI_USERNAME = os.getenv("KALI_SSH_USER", "hollow")
KALI_PASSWORD = os.getenv("KALI_SSH_PASS", "GH0s.N0ker")


class KaliExecutor:
    """Execute security tools on Kali Linux VM via SSH"""
    
    def __init__(self, host: str = None, username: str = None, password: str = None):
        self.host = host or KALI_HOST
        self.username = username or KALI_USERNAME
        self.password = password or KALI_PASSWORD
        self.timeout = 300
    
    async def execute(self, cmd: str, timeout: int = 300, sudo: bool = False) -> Dict:
        """Execute arbitrary command on Kali"""
        try:
            if sudo:
                cmd = f"sudo {cmd}"
                
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Use password authentication instead of key
            ssh.connect(self.host, username=self.username, password=self.password, timeout=10)
            
            stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
            output = stdout.read().decode()
            error = stderr.read().decode()
            exit_code = stdout.channel.recv_exit_status()
            
            ssh.close()
            
            return {
                "success": exit_code == 0,
                "output": output,
                "error": error,
                "exit_code": exit_code
            }
        except Exception as e:
            return {"success": False, "error": str(e), "output": "", "exit_code": -1}
    
    async def execute_command(self, cmd: str, timeout: int = 300) -> Dict:
        """Alias for execute() - used by reverse_engineering and advanced_web_tools services"""
        return await self.execute(cmd, timeout=timeout)
    
    async def execute_nmap(self, target: str, options: str = "-sV") -> Dict:
        """Execute nmap scan"""
        cmd = f"nmap {options} {target}"
        return await self.execute(cmd)
    
    async def execute_sqlmap(self, url: str, options: str = "--batch --risk=1 --level=1") -> Dict:
        """Execute sqlmap"""
        cmd = f"sqlmap -u '{url}' {options}"
        return await self.execute(cmd)
    
    async def execute_nikto(self, target: str) -> Dict:
        """Execute nikto web scanner"""
        cmd = f"nikto -h {target}"
        return await self.execute(cmd)
    
    async def execute_gobuster(self, url: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt") -> Dict:
        """Execute gobuster directory enumeration"""
        cmd = f"gobuster dir -u {url} -w {wordlist} -q"
        return await self.execute(cmd)
    
    async def execute_hydra(self, target: str, service: str, username: str = None, password_list: str = None) -> Dict:
        """Execute hydra brute force"""
        user_opt = f"-l {username}" if username else "-L /usr/share/wordlists/metasploit/unix_users.txt"
        pass_opt = f"-P {password_list}" if password_list else "-P /usr/share/wordlists/rockyou.txt"
        cmd = f"hydra {user_opt} {pass_opt} {target} {service}"
        return await self.execute(cmd)
    
    async def execute_john(self, hash_file: str, wordlist: str = None) -> Dict:
        """Execute john the ripper"""
        wordlist_opt = f"--wordlist={wordlist}" if wordlist else ""
        cmd = f"john {wordlist_opt} {hash_file}"
        return await self.execute(cmd)
    
    async def execute_hashcat(self, hash_file: str, mode: int = 0, wordlist: str = None) -> Dict:
        """Execute hashcat"""
        wordlist = wordlist or "/usr/share/wordlists/rockyou.txt"
        cmd = f"hashcat -m {mode} -a 0 {hash_file} {wordlist}"
        return await self.execute(cmd)
    
    async def execute_wpscan(self, url: str) -> Dict:
        """Execute WPScan"""
        cmd = f"wpscan --url {url} --enumerate u,p"
        return await self.execute(cmd)
    
    async def execute_dnsenum(self, domain: str) -> Dict:
        """Execute dnsenum"""
        cmd = f"dnsenum {domain}"
        return await self.execute(cmd)
    
    async def execute_theharvester(self, domain: str, source: str = "all") -> Dict:
        """Execute theHarvester"""
        cmd = f"theHarvester -d {domain} -b {source}"
        return await self.execute(cmd)
    
    async def execute_masscan(self, target: str, ports: str = "1-65535", rate: int = 1000) -> Dict:
        """Execute masscan"""
        cmd = f"masscan {target} -p{ports} --rate={rate}"
        return await self.execute(cmd)
    
    async def execute_metasploit(self, exploit: str, target: str, options: Dict = None) -> Dict:
        """Execute metasploit module"""
        opts = " ".join([f"set {k} {v}" for k, v in (options or {}).items()])
        cmd = f"msfconsole -q -x 'use {exploit}; {opts}; set RHOST {target}; run; exit'"
        return await self.execute(cmd)
    
    async def execute_searchsploit(self, query: str) -> Dict:
        """Search exploits"""
        cmd = f"searchsploit {query}"
        return await self.execute(cmd)
    
    async def execute_enum4linux(self, target: str) -> Dict:
        """Execute enum4linux"""
        cmd = f"enum4linux -a {target}"
        return await self.execute(cmd)
    
    async def execute_testssl(self, target: str) -> Dict:
        """Execute testssl.sh"""
        cmd = f"testssl.sh {target}"
        return await self.execute(cmd)

# Singleton instance
kali_executor = KaliExecutor()
