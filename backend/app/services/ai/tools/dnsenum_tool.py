import json
from typing import List
from .base import BaseTool, ToolParameter, ToolResult

class DNSEnumTool(BaseTool):
    def get_description(self) -> str:
        return "DNS enumeration including A, MX, NS, TXT records, and zone transfer attempts."
    
    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="domain",
                type="string",
                description="Target domain to enumerate"
            ),
            ToolParameter(
                name="record_types",
                type="string",
                description="Comma-separated record types (default: A,MX,NS,TXT)",
                required=False
            )
        ]
    
    async def execute(self, domain: str, record_types: str = "A,MX,NS,TXT") -> ToolResult:
        try:
            self.validate_params(domain=domain)
            
            import dns.resolver
            import dns.zone
            
            types = [t.strip() for t in record_types.split(",")]
            results = {"domain": domain, "records": {}}
            
            for record_type in types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    results["records"][record_type] = [str(rdata) for rdata in answers]
                except Exception as e:
                    results["records"][record_type] = f"Error: {str(e)}"
            
            # Try zone transfer
            results["zone_transfer"] = await self._try_zone_transfer(domain)
            
            return ToolResult(
                success=True,
                output=json.dumps(results, indent=2),
                metadata={"record_types": len(types)}
            )
        
        except Exception as e:
            self.logger.error(f"DNS enumeration failed: {str(e)}")
            return ToolResult(success=False, output="", error=str(e))
    
    async def _try_zone_transfer(self, domain: str) -> dict:
        try:
            import dns.resolver
            import dns.zone
            
            ns_records = dns.resolver.resolve(domain, "NS")
            
            for ns in ns_records:
                ns_ip = str(ns)
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(ns_ip, domain, timeout=5))
                    return {
                        "vulnerable": True,
                        "nameserver": ns_ip,
                        "records_count": len(zone.nodes)
                    }
                except:
                    continue
            
            return {"vulnerable": False, "message": "Zone transfer not allowed"}
        except:
            return {"error": "Could not test zone transfer"}
