from typing import List, Dict, Any
from .llm_service import OllamaLLMService
from .prompts.system import REPORT_GENERATOR_PROMPT
import json

class ReportGenerator:
    def __init__(self, model: str = "deepseek-coder:latest"):
        self.llm = OllamaLLMService(model)
    
    async def generate_executive_summary(
        self,
        scan_data: Dict[str, Any],
        findings: List[Dict[str, Any]]
    ) -> str:
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for f in findings:
            sev = f.get("severity", "info").lower()
            if sev in severity_counts:
                severity_counts[sev] += 1
        
        prompt = f"""Generate an executive summary for this security scan:

Target: {scan_data.get('target')}
Scan Type: {scan_data.get('scan_type')}
Total Findings: {len(findings)}

Severity Breakdown:
- Critical: {severity_counts['critical']}
- High: {severity_counts['high']}
- Medium: {severity_counts['medium']}
- Low: {severity_counts['low']}

Top Findings:
{json.dumps(findings[:5], indent=2)}

Provide a concise executive summary (3-4 paragraphs) covering:
1. Overall security posture
2. Critical risks requiring immediate attention
3. Recommended next steps"""
        
        return await self.llm.generate(prompt, system=REPORT_GENERATOR_PROMPT, max_tokens=1024)
    
    async def generate_technical_details(
        self,
        findings: List[Dict[str, Any]]
    ) -> str:
        prompt = f"""Generate detailed technical analysis for these findings:

{json.dumps(findings, indent=2)}

For each finding, provide:
1. Technical description
2. Exploitation steps
3. Business impact
4. Remediation guidance"""
        
        return await self.llm.generate(prompt, system=REPORT_GENERATOR_PROMPT, max_tokens=2048)
    
    async def generate_remediation_plan(
        self,
        findings: List[Dict[str, Any]]
    ) -> str:
        prompt = f"""Create a prioritized remediation plan for these findings:

{json.dumps(findings, indent=2)}

Provide:
1. Priority order (by risk)
2. Estimated effort for each
3. Dependencies between fixes
4. Quick wins vs long-term fixes"""
        
        return await self.llm.generate(prompt, system=REPORT_GENERATOR_PROMPT, max_tokens=1024)
