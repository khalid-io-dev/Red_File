import socket
import json
from typing import List
from .base import BaseTool, ToolParameter, ToolResult
from concurrent.futures import ThreadPoolExecutor

class PortScanTool(BaseTool):
    def get_description(self) -> str:
        return "Fast TCP port scanner with service detection. Scans common or custom port ranges."
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="target",
                type="string",
                description="Target IP or hostname"
            ),
            ToolParameter(
                name="ports",
                type="string",
                description="Port range (e.g., '1-1000' or '80,443,8080')",
                required=False
            ),
            ToolParameter(
                name="timeout",
                type="string",
                description="Connection timeout in seconds (default: 1)",
                required=False
            )
        ]
    
    async def execute(self, target: str, ports: str = "1-1000", timeout: str = "1") -> ToolResult:
        try:
            self.validate_params(target=target)
            
            port_list = self._parse_ports(ports)
            timeout_val = float(timeout)
            
            open_ports = []
            
            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = [executor.submit(self._scan_port, target, port, timeout_val) for port in port_list]
                for future in futures:
                    result = future.result()
                    if result:
                        open_ports.append(result)
            
            output = {
                "target": target,
                "open_ports": sorted(open_ports, key=lambda x: x["port"]),
                "total_scanned": len(port_list),
                "total_open": len(open_ports)
            }
            
            return ToolResult(
                success=True,
                output=json.dumps(output, indent=2),
                metadata={"open_ports": len(open_ports)}
            )
        
        except Exception as e:
            self.logger.error(f"Port scan failed: {str(e)}")
            return ToolResult(success=False, output="", error=str(e))
    
    def _parse_ports(self, ports: str) -> List[int]:
        if "-" in ports:
            start, end = map(int, ports.split("-"))
            return list(range(start, end + 1))
        else:
            return [int(p.strip()) for p in ports.split(",")]
    
    def _scan_port(self, target: str, port: int, timeout: float) -> dict:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                service = self._get_service(port)
                return {"port": port, "state": "open", "service": service}
        except:
            pass
        return None
    
    def _get_service(self, port: int) -> str:
        services = {
            21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
            80: "http", 110: "pop3", 143: "imap", 443: "https", 445: "smb",
            3306: "mysql", 3389: "rdp", 5432: "postgresql", 6379: "redis",
            8080: "http-proxy", 8443: "https-alt", 27017: "mongodb"
        }
        return services.get(port, "unknown")
