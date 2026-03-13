import asyncio
import subprocess
import json
from typing import Dict, Any
from .base_agent import BaseAgent
from .ssh_client import ssh_client

class VulnScannerAgent(BaseAgent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.targets = ["192.168.56.0/24"]  # Default to network scan
        self.current_target_index = 0
        self.use_ssh = True
    
    async def execute_task(self) -> Dict[str, Any]:
        target = self.targets[self.current_target_index % len(self.targets)]
        self.log(f"🔍 Scanning target: {target}")
        
        # Try SSH first, fallback to local
        if self.use_ssh:
            result = await self.run_nmap_ssh(target)
            if result.get("error") == "SSH connection failed":
                self.use_ssh = False
                self.log("⚠️ SSH failed, switching to local execution")
                result = await self.run_nmap_local(target)
        else:
            result = await self.run_nmap_local(target)
        
        self.current_target_index += 1
        return result
    
    async def run_nmap_ssh(self, target: str) -> Dict[str, Any]:
        """Run nmap via SSH on Kali Linux"""
        try:
            self.log(f"📡 Connecting to Kali ({ssh_client.host})...")
            
            command = f"nmap -F -T4 {target}"
            stdout, stderr, exit_code = await asyncio.wait_for(
                ssh_client.execute(command, timeout=30),
                timeout=35
            )
            
            if exit_code == 0:
                open_ports = self.parse_nmap_output(stdout)
                self.log(f"✅ Found {len(open_ports)} open ports (Kali SSH)")
                
                return {
                    "target": target,
                    "open_ports": open_ports,
                    "timestamp": asyncio.get_event_loop().time(),
                    "source": "kali_ssh"
                }
            else:
                self.log(f"⚠️ SSH scan failed: {stderr}")
                return {"target": target, "error": "SSH scan failed"}
                
        except asyncio.TimeoutError:
            self.log("⏱️ Kali connection timeout - is VM running?")
            return {"target": target, "error": "Kali VM not reachable"}
        except Exception as e:
            self.log(f"❌ SSH Error: {str(e)[:50]}")
            return {"target": target, "error": "SSH connection failed"}
    
    async def run_nmap_local(self, target: str) -> Dict[str, Any]:
        """Run nmap locally"""
        try:
            self.log(f"📡 Running port scan locally...")
            
            process = await asyncio.create_subprocess_exec(
                'nmap', '-F', '-T4', target,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=30)
            
            if process.returncode == 0:
                output = stdout.decode()
                open_ports = self.parse_nmap_output(output)
                
                self.log(f"✅ Found {len(open_ports)} open ports (local)")
                
                return {
                    "target": target,
                    "open_ports": open_ports,
                    "timestamp": asyncio.get_event_loop().time(),
                    "source": "local"
                }
            else:
                self.log(f"⚠️ Local scan failed: {stderr.decode()}")
                return {"target": target, "error": "Scan failed"}
                
        except FileNotFoundError:
            self.log("⚠️ nmap not installed locally, using mock data")
            return await self.mock_scan(target)
        except asyncio.TimeoutError:
            self.log("⏱️ Scan timeout")
            return {"target": target, "error": "Timeout"}
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            return await self.mock_scan(target)
    
    def parse_nmap_output(self, output: str) -> list:
        open_ports = []
        for line in output.split('\n'):
            if '/tcp' in line and 'open' in line:
                parts = line.split()
                if len(parts) >= 3:
                    port = parts[0].split('/')[0]
                    service = parts[2] if len(parts) > 2 else 'unknown'
                    open_ports.append({"port": port, "service": service})
        return open_ports
    
    async def mock_scan(self, target: str) -> Dict[str, Any]:
        """Fallback mock data when nmap unavailable"""
        await asyncio.sleep(2)
        mock_ports = [
            {"port": "80", "service": "http"},
            {"port": "443", "service": "https"},
            {"port": "22", "service": "ssh"}
        ]
        self.log(f"✅ Found {len(mock_ports)} open ports (mock)")
        return {
            "target": target,
            "open_ports": mock_ports,
            "timestamp": asyncio.get_event_loop().time(),
            "source": "mock"
        }
