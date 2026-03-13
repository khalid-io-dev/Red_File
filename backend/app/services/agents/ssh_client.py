import asyncio
import asyncssh
from typing import Optional, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

class SSHClient:
    def __init__(self):
        self.host = os.getenv("KALI_SSH_HOST", "192.168.56.101").strip("'\"")
        self.port = int(os.getenv("KALI_SSH_PORT", "22"))
        self.username = os.getenv("KALI_SSH_USER", "hollow").strip("'\"")
        self.password = os.getenv("KALI_SSH_PASS", "").strip("'\"")
        self.key_path = os.getenv("KALI_SSH_KEY", "").strip("'\"")
        self._conn = None
        
        print(f"SSH Config: {self.username}@{self.host}:{self.port}")
    
    async def connect(self):
        """Establish SSH connection"""
        if self._conn:
            return self._conn
        
        try:
            if self.key_path and os.path.exists(self.key_path):
                print(f"Connecting with SSH key: {self.key_path}")
                self._conn = await asyncssh.connect(
                    self.host,
                    port=self.port,
                    username=self.username,
                    client_keys=[self.key_path],
                    known_hosts=None
                )
            elif self.password:
                print(f"Connecting with password to {self.host}")
                self._conn = await asyncssh.connect(
                    self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    known_hosts=None
                )
            else:
                raise Exception("No SSH credentials configured")
            
            print("[OK] SSH connected to", self.host)
            return self._conn
        except Exception as e:
            print(f"[ERROR] SSH connection failed: {e}")
            return None
    
    async def execute(self, command: str, timeout: int = 30) -> Tuple[str, str, int]:
        """Execute command on remote host"""
        conn = await self.connect()
        if not conn:
            return "", "SSH connection failed", 1
        
        try:
            result = await asyncio.wait_for(
                conn.run(command),
                timeout=timeout
            )
            return result.stdout, result.stderr, result.exit_status
        except asyncio.TimeoutError:
            return "", "Command timeout", 1
        except Exception as e:
            return "", str(e), 1
    
    async def close(self):
        """Close SSH connection"""
        if self._conn:
            self._conn.close()
            await self._conn.wait_closed()
            self._conn = None

# Global SSH client
ssh_client = SSHClient()
