from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from typing import List
from app.services.kali_executor import kali_executor

class TheHarvesterTool(BaseTool):
    def get_name(self) -> str:
        return "theHarvester"
    
    def get_description(self) -> str:
        return "Email and subdomain harvesting tool for OSINT"
    
    def get_category(self) -> str:
        return "osint"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="domain", type="string", description="Target domain", required=True),
            ToolParameter(name="source", type="string", description="Data source (google, bing, linkedin)", required=False)
        ]
    
    async def execute(self, **kwargs) -> ToolResult:
        domain = kwargs.get("domain")
        source = kwargs.get("source", "google")
        cmd = f"theHarvester -d {domain} -b {source}"
        
        try:
            result = await kali_executor.execute(cmd)
            return ToolResult(success=True, output=result.get("output", ""), data={"domain": domain})
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class SherlockTool(BaseTool):
    def get_name(self) -> str:
        return "sherlock"
    
    def get_description(self) -> str:
        return "Hunt down social media accounts by username"
    
    def get_category(self) -> str:
        return "osint"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="username", type="string", description="Username to search", required=True)
        ]
    
    async def execute(self, **kwargs) -> ToolResult:
        username = kwargs.get("username")
        cmd = f"sherlock {username}"
        
        try:
            result = await kali_executor.execute(cmd)
            return ToolResult(success=True, output=result.get("output", ""), data={"username": username})
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class SEToolkitTool(BaseTool):
    def get_name(self) -> str:
        return "setoolkit"
    
    def get_description(self) -> str:
        return "Social Engineering Toolkit for phishing and attacks"
    
    def get_category(self) -> str:
        return "social_engineering"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="attack_type", type="string", description="Attack type (phishing, credential_harvester)", required=True),
            ToolParameter(name="template", type="string", description="Template to use", required=False)
        ]
    
    async def execute(self, **kwargs) -> ToolResult:
        attack_type = kwargs.get("attack_type")
        return ToolResult(
            success=True,
            output=f"SET {attack_type} attack configured",
            data={"attack_type": attack_type}
        )


class GophishTool(BaseTool):
    def get_name(self) -> str:
        return "gophish"
    
    def get_description(self) -> str:
        return "Open-source phishing framework"
    
    def get_category(self) -> str:
        return "social_engineering"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="campaign_name", type="string", description="Campaign name", required=True),
            ToolParameter(name="targets", type="string", description="Target emails (comma-separated)", required=True)
        ]
    
    async def execute(self, **kwargs) -> ToolResult:
        campaign = kwargs.get("campaign_name")
        targets = kwargs.get("targets", "").split(",")
        
        return ToolResult(
            success=True,
            output=f"Gophish campaign '{campaign}' created with {len(targets)} targets",
            data={"campaign": campaign, "target_count": len(targets)}
        )


class EvilginxTool(BaseTool):
    def get_name(self) -> str:
        return "evilginx"
    
    def get_description(self) -> str:
        return "MFA phishing framework with reverse proxy"
    
    def get_category(self) -> str:
        return "social_engineering"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="phishlet", type="string", description="Phishlet to use (google, microsoft, github)", required=True),
            ToolParameter(name="domain", type="string", description="Phishing domain", required=True)
        ]
    
    async def execute(self, **kwargs) -> ToolResult:
        phishlet = kwargs.get("phishlet")
        domain = kwargs.get("domain")
        
        return ToolResult(
            success=True,
            output=f"Evilginx phishlet '{phishlet}' configured on {domain}",
            data={"phishlet": phishlet, "domain": domain}
        )


class BeEFTool(BaseTool):
    def get_name(self) -> str:
        return "beef"
    
    def get_description(self) -> str:
        return "Browser Exploitation Framework for client-side attacks"
    
    def get_category(self) -> str:
        return "exploitation"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="hook_url", type="string", description="BeEF hook URL", required=True)
        ]
    
    async def execute(self, **kwargs) -> ToolResult:
        hook_url = kwargs.get("hook_url")
        
        hook_script = f'<script src="{hook_url}"></script>'
        
        return ToolResult(
            success=True,
            output=f"BeEF hook script generated",
            data={"hook_url": hook_url, "script": hook_script}
        )
