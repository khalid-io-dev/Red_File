import subprocess
import json
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class NucleiTool(BaseTool):
    def get_description(self) -> str:
        return "Fast vulnerability scanner using community templates. Detects CVEs, misconfigurations, and security issues."
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="target",
                type="string",
                description="Target URL or host to scan (e.g., https://example.com)"
            ),
            ToolParameter(
                name="severity",
                type="string",
                description="Filter by severity level",
                required=False,
                enum=["info", "low", "medium", "high", "critical"]
            ),
            ToolParameter(
                name="tags",
                type="string",
                description="Filter by tags (comma-separated, e.g., 'cve,xss,sqli')",
                required=False
            )
        ]
    
    async def execute(self, target: str, severity: str = None, tags: str = None) -> ToolResult:
        try:
            self.validate_params(target=target)
            
            cmd = [
                "nuclei",
                "-u", target,
                "-json",
                "-silent"
            ]
            
            if severity:
                cmd.extend(["-severity", severity])
            
            if tags:
                cmd.extend(["-tags", tags])
            
            self.logger.info(f"Running Nuclei: {' '.join(cmd)}")
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            findings = []
            for line in process.stdout.strip().split('\n'):
                if line:
                    try:
                        findings.append(json.loads(line))
                    except:
                        pass
            
            result = {
                "target": target,
                "findings_count": len(findings),
                "findings": findings[:50]
            }
            
            return ToolResult(
                success=True,
                output=json.dumps(result, indent=2),
                metadata={"findings_count": len(findings)}
            )
        
        except subprocess.TimeoutExpired:
            return ToolResult(success=False, output="", error="Nuclei timeout after 10 minutes")
        except FileNotFoundError:
            return ToolResult(success=False, output="", error="Nuclei not installed. Install from: https://github.com/projectdiscovery/nuclei")
        except Exception as e:
            self.logger.error(f"Nuclei failed: {str(e)}")
            return ToolResult(success=False, output="", error=str(e))
