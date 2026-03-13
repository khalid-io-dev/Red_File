import ssl
import socket
import json
from typing import List
from .base import BaseTool, ToolParameter, ToolResult
from datetime import datetime

class SSLAnalyzerTool(BaseTool):
    def get_description(self) -> str:
        return "Analyze SSL/TLS certificates, check for vulnerabilities, and verify security configurations."
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="target",
                type="string",
                description="Target hostname (e.g., example.com)"
            ),
            ToolParameter(
                name="port",
                type="string",
                description="Port number (default: 443)",
                required=False
            )
        ]
    
    async def execute(self, target: str, port: str = "443") -> ToolResult:
        try:
            self.validate_params(target=target)
            port_num = int(port)
            
            context = ssl.create_default_context()
            
            with socket.create_connection((target, port_num), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
                    
                    result = {
                        "target": target,
                        "port": port_num,
                        "certificate": {
                            "subject": dict(x[0] for x in cert.get("subject", [])),
                            "issuer": dict(x[0] for x in cert.get("issuer", [])),
                            "version": cert.get("version"),
                            "serial_number": cert.get("serialNumber"),
                            "not_before": cert.get("notBefore"),
                            "not_after": cert.get("notAfter"),
                            "san": cert.get("subjectAltName", [])
                        },
                        "tls_version": version,
                        "cipher_suite": {
                            "name": cipher[0] if cipher else "Unknown",
                            "protocol": cipher[1] if cipher else "Unknown",
                            "bits": cipher[2] if cipher else 0
                        },
                        "vulnerabilities": self._check_vulnerabilities(version, cipher)
                    }
                    
                    return ToolResult(
                        success=True,
                        output=json.dumps(result, indent=2),
                        metadata={"tls_version": version, "vulnerabilities": len(result["vulnerabilities"])}
                    )
        
        except Exception as e:
            self.logger.error(f"SSL analysis failed: {str(e)}")
            return ToolResult(success=False, output="", error=str(e))
    
    def _check_vulnerabilities(self, version: str, cipher: tuple) -> List[dict]:
        vulns = []
        
        if version in ["SSLv2", "SSLv3", "TLSv1", "TLSv1.1"]:
            vulns.append({
                "type": "Outdated TLS Version",
                "severity": "high",
                "description": f"{version} is deprecated and vulnerable"
            })
        
        if cipher and "RC4" in cipher[0]:
            vulns.append({
                "type": "Weak Cipher",
                "severity": "medium",
                "description": "RC4 cipher is cryptographically weak"
            })
        
        if cipher and cipher[2] < 128:
            vulns.append({
                "type": "Weak Encryption",
                "severity": "medium",
                "description": f"Cipher strength {cipher[2]} bits is below recommended 128 bits"
            })
        
        return vulns
