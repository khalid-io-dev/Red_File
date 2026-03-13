import json
from typing import Dict, Any

class ToolResultParser:
    @staticmethod
    def parse(tool_name: str, output: str) -> Dict[str, Any]:
        try:
            data = json.loads(output)
            
            if tool_name == "portscan":
                return {
                    "open_ports": data.get("open_ports", []),
                    "total_open": data.get("total_open", 0),
                    "summary": f"Found {data.get('total_open', 0)} open ports"
                }
            elif tool_name == "sslanalyzer":
                vulns = data.get("vulnerabilities", [])
                return {
                    "tls_version": data.get("tls_version"),
                    "vulnerabilities": vulns,
                    "summary": f"TLS {data.get('tls_version')}, {len(vulns)} vulnerabilities"
                }
            elif tool_name == "dnsenum":
                records = data.get("records", {})
                return {
                    "records": records,
                    "summary": f"Found {len(records)} DNS record types"
                }
            elif tool_name == "webrecon":
                return {
                    "subdomains": data.get("subdomains", []),
                    "directories": data.get("directories", []),
                    "summary": f"Found {len(data.get('subdomains', []))} subdomains"
                }
            else:
                return {"summary": "Tool executed successfully", "data": data}
        except:
            return {"summary": "Tool executed", "raw": output[:200]}
