from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from typing import List

class GCPSecurityScanner(BaseTool):
    def get_description(self) -> str:
        return "GCP security scanner"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="project_id", type="string", description="GCP project", required=False),
        ]
    
    async def execute(self, project_id: str = None, **kwargs) -> ToolResult:
        findings = [{"resource": "gcs-public", "issue": "Public bucket", "severity": "critical"}]
        return ToolResult(success=True, output=str(findings))
    
    parameters = [
        {"name": "project_id", "type": "string", "required": False},
        {"name": "scan_type", "type": "string", "required": False, "default": "all"},
    ]
    
    mitre_techniques = ["T1580", "T1526", "T1619"]
    
    async def execute(self, project_id: str = None, scan_type: str = "all", **kwargs):
        findings = []
        
        if scan_type in ["all", "storage"]:
            findings.append({
                "resource": "gcs-public",
                "issue": "GCS bucket public",
                "severity": "critical",
                "recommendation": "Remove allUsers"
            })
        
        return {"findings": findings, "total": len(findings)}
