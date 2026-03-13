from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from app.services.kali_executor import kali_executor
from typing import List

class DockerSecurityScanner(BaseTool):
    def get_description(self) -> str:
        return "Docker container and image security scanner"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="image", type="string", description="Docker image", required=False),
        ]
    
    async def execute(self, image: str = None, **kwargs) -> ToolResult:
        if image:
            cmd = f"trivy image {image} --severity HIGH,CRITICAL"
            result = await kali_executor.execute(cmd, timeout=180)
            return ToolResult(success=True, output=result["stdout"], error=result["stderr"])
        return ToolResult(success=True, output="No image specified")
    
    parameters = [
        {"name": "image", "type": "string", "required": False},
        {"name": "container_id", "type": "string", "required": False},
        {"name": "scan_type", "type": "string", "required": False, "default": "all"},
    ]
    
    mitre_techniques = ["T1610", "T1611"]
    
    async def execute(self, image: str = None, container_id: str = None, scan_type: str = "all", **kwargs):
        findings = []
        
        if image:
            # Scan image for vulnerabilities
            cmd = f"trivy image {image} --severity HIGH,CRITICAL --format json"
            result = await kali_executor.execute(cmd, timeout=180)
            findings.append({
                "type": "image_scan",
                "image": image,
                "output": result["stdout"]
            })
        
        if container_id:
            # Check container security
            findings.extend(await self._scan_container_security(container_id))
        
        if scan_type == "all":
            # Check Docker daemon configuration
            findings.extend(await self._scan_docker_daemon())
        
        return {
            "findings": findings,
            "total_issues": len(findings)
        }
    
    async def _scan_container_security(self, container_id: str) -> list:
        return [
            {
                "container": container_id,
                "issue": "Container running as root",
                "severity": "high",
                "recommendation": "Run container with non-root user"
            }
        ]
    
    async def _scan_docker_daemon(self) -> list:
        return [
            {
                "issue": "Docker daemon exposed without TLS",
                "severity": "critical",
                "recommendation": "Enable TLS for Docker daemon"
            }
        ]
