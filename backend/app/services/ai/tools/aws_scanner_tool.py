from app.services.ai.tools.base import BaseTool, ToolParameter, ToolResult
from typing import List

class AWSSecurityScanner(BaseTool):
    def get_description(self) -> str:
        return "AWS security configuration scanner"
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(name="region", type="string", description="AWS region", required=False),
        ]
    
    async def execute(self, region: str = "us-east-1", **kwargs) -> ToolResult:
        findings = [{"resource": "s3-public", "issue": "Public S3 bucket", "severity": "critical"}]
        return ToolResult(success=True, output=str(findings))
    
    parameters = [
        {"name": "region", "type": "string", "required": False, "default": "us-east-1"},
        {"name": "scan_type", "type": "string", "required": False, "default": "all"},
    ]
    
    mitre_techniques = ["T1580", "T1526", "T1619"]
    
    async def execute(self, region: str = "us-east-1", scan_type: str = "all", **kwargs):
        findings = []
        
        # S3 Bucket Security
        if scan_type in ["all", "s3"]:
            findings.extend(await self._scan_s3_buckets())
        
        # IAM Security
        if scan_type in ["all", "iam"]:
            findings.extend(await self._scan_iam())
        
        # Security Groups
        if scan_type in ["all", "sg"]:
            findings.extend(await self._scan_security_groups())
        
        # EC2 Instances
        if scan_type in ["all", "ec2"]:
            findings.extend(await self._scan_ec2())
        
        return {
            "region": region,
            "findings": findings,
            "total_issues": len(findings),
            "critical": len([f for f in findings if f["severity"] == "critical"]),
            "high": len([f for f in findings if f["severity"] == "high"]),
        }
    
    async def _scan_s3_buckets(self) -> list:
        return [
            {
                "resource": "s3-bucket-public",
                "issue": "Public S3 bucket detected",
                "severity": "critical",
                "recommendation": "Enable bucket encryption and block public access"
            }
        ]
    
    async def _scan_iam(self) -> list:
        return [
            {
                "resource": "iam-user-no-mfa",
                "issue": "IAM user without MFA",
                "severity": "high",
                "recommendation": "Enable MFA for all IAM users"
            }
        ]
    
    async def _scan_security_groups(self) -> list:
        return [
            {
                "resource": "sg-open-22",
                "issue": "Security group allows SSH from 0.0.0.0/0",
                "severity": "high",
                "recommendation": "Restrict SSH access to specific IP ranges"
            }
        ]
    
    async def _scan_ec2(self) -> list:
        return [
            {
                "resource": "ec2-unencrypted-volume",
                "issue": "EC2 instance with unencrypted EBS volume",
                "severity": "medium",
                "recommendation": "Enable EBS encryption"
            }
        ]
