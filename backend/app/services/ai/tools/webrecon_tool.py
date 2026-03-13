import subprocess
import json
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class WebReconTool(BaseTool):
    def get_description(self) -> str:
        return "Web reconnaissance including subdomain enumeration, directory discovery, and technology detection."
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="target",
                type="string",
                description="Target domain (e.g., example.com)"
            ),
            ToolParameter(
                name="recon_type",
                type="string",
                description="Type of reconnaissance",
                enum=["subdomains", "directories", "tech_stack", "all"]
            )
        ]
    
    async def execute(self, target: str, recon_type: str = "all") -> ToolResult:
        try:
            self.validate_params(target=target, recon_type=recon_type)
            
            results = {}
            
            if recon_type in ["subdomains", "all"]:
                results["subdomains"] = await self._find_subdomains(target)
            
            if recon_type in ["directories", "all"]:
                results["directories"] = await self._find_directories(target)
            
            if recon_type in ["tech_stack", "all"]:
                results["tech_stack"] = await self._detect_tech(target)
            
            return ToolResult(
                success=True,
                output=json.dumps(results, indent=2),
                metadata={"target": target, "recon_type": recon_type}
            )
        
        except Exception as e:
            self.logger.error(f"Web recon failed: {str(e)}")
            return ToolResult(success=False, output="", error=str(e))
    
    async def _find_subdomains(self, target: str) -> List[str]:
        import dns.resolver
        subdomains = []
        common = ["www", "mail", "ftp", "admin", "api", "dev", "staging", "test"]
        
        for sub in common:
            try:
                dns.resolver.resolve(f"{sub}.{target}", "A")
                subdomains.append(f"{sub}.{target}")
            except:
                pass
        
        return subdomains
    
    async def _find_directories(self, target: str) -> List[str]:
        import requests
        dirs = []
        common = ["/admin", "/api", "/login", "/dashboard", "/uploads", "/.git", "/.env"]
        
        for path in common:
            try:
                url = f"http://{target}{path}"
                r = requests.get(url, timeout=3, allow_redirects=False)
                if r.status_code in [200, 301, 302, 403]:
                    dirs.append({"path": path, "status": r.status_code})
            except:
                pass
        
        return dirs
    
    async def _detect_tech(self, target: str) -> dict:
        import requests
        try:
            r = requests.get(f"http://{target}", timeout=5)
            return {
                "server": r.headers.get("Server", "Unknown"),
                "powered_by": r.headers.get("X-Powered-By", "Unknown"),
                "status_code": r.status_code
            }
        except:
            return {"error": "Could not detect technology"}
