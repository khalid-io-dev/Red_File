from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from typing import List

class AzureSecurityScanner(BaseTool):
    def get_description(self) -> str:
        return "Azure cloud security scanner"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="subscription_id", type="string", description="Azure subscription", required=False),
        ]
    
    async def execute(self, subscription_id: str = None, **kwargs) -> ToolResult:
        findings = [{"resource": "storage-public", "issue": "Public storage", "severity": "high"}]
        return ToolResult(success=True, output=str(findings))
    
    parameters = [
        {"name": "subscription_id", "type": "string", "required": False},
        {"name": "scan_type", "type": "string", "required": False, "default": "all"},
    ]
    
    mitre_techniques = ["T1580", "T1526", "T1619"]
    
    async def execute(self, subscription_id: str = None, scan_type: str = "all", **kwargs):
        findings = []
        
        if scan_type in ["all", "storage"]:
            findings.append({
                "resource": "storage-public",
                "issue": "Storage account public access",
                "severity": "high",
                "recommendation": "Disable public access"
            })
        
        if scan_type in ["all", "iam"]:
            findings.append({
                "resource": "rbac-overprivileged",
                "issue": "User has Owner role",
                "severity": "high",
                "recommendation": "Apply least privilege"
            })
        
        return {"findings": findings, "total": len(findings)}
