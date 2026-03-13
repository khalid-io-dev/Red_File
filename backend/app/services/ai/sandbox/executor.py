import subprocess
import asyncio
from typing import AsyncGenerator, Optional, List
import logging

logger = logging.getLogger(__name__)

class CommandExecutor:
    def __init__(self, timeout: int = 300):
        self.timeout = timeout
    
    async def execute_sync(
        self,
        command: List[str],
        cwd: Optional[str] = None,
        env: Optional[dict] = None
    ) -> tuple[str, str, int]:
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
                env=env
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.timeout
            )
            
            return (
                stdout.decode('utf-8', errors='ignore'),
                stderr.decode('utf-8', errors='ignore'),
                process.returncode
            )
        except asyncio.TimeoutError:
            process.kill()
            return "", f"Timeout after {self.timeout}s", -1
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            return "", str(e), -1
