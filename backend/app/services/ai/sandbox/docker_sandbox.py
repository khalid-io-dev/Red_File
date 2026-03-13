import docker
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DockerSandbox:
    def __init__(self, image: str = "kalilinux/kali-rolling"):
        try:
            self.client = docker.from_env()
            self.image = image
            self.container = None
        except Exception as e:
            logger.warning(f"Docker not available: {str(e)}")
            self.client = None
    
    def is_available(self) -> bool:
        return self.client is not None
    
    async def create_container(
        self,
        command: str,
        network_mode: str = "bridge",
        mem_limit: str = "512m",
        cpu_quota: int = 50000
    ) -> Optional[str]:
        if not self.client:
            return None
        
        try:
            self.container = self.client.containers.run(
                self.image,
                command=command,
                detach=True,
                network_mode=network_mode,
                mem_limit=mem_limit,
                cpu_quota=cpu_quota,
                remove=True
            )
            return self.container.id
        except Exception as e:
            logger.error(f"Container creation failed: {str(e)}")
            return None
    
    async def execute_command(self, command: str) -> tuple[str, int]:
        if not self.container:
            return "No container available", -1
        
        try:
            result = self.container.exec_run(command)
            return result.output.decode('utf-8', errors='ignore'), result.exit_code
        except Exception as e:
            logger.error(f"Command execution failed: {str(e)}")
            return str(e), -1
    
    async def stop(self):
        if self.container:
            try:
                self.container.stop()
                self.container = None
            except Exception as e:
                logger.error(f"Container stop failed: {str(e)}")
    
    async def cleanup(self):
        await self.stop()
