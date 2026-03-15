from typing import Dict, List
from datetime import datetime

class IDSIPSManager:
    """Manage Snort and Suricata IDS/IPS"""
    
    def __init__(self):
        self.snort_rules_path = "/etc/snort/rules"
        self.suricata_rules_path = "/etc/suricata/rules"
    
    async def get_snort_alerts(self, limit: int = 100) -> Dict:
        """Get Snort alerts"""
        
        # Simulated alerts
        alerts = [
            {"timestamp": datetime.utcnow().isoformat(), "priority": "high", "signature": "SQL Injection Attempt", "src_ip": "1.2.3.4", "dst_ip": "10.0.0.1"},
            {"timestamp": datetime.utcnow().isoformat(), "priority": "medium", "signature": "Port Scan Detected", "src_ip": "5.6.7.8", "dst_ip": "10.0.0.1"}
        ]
        
        return {
            "ids": "snort",
            "alerts": alerts[:limit],
            "total_alerts": len(alerts),
            "high_priority": len([a for a in alerts if a["priority"] == "high"])
        }
    
    async def get_suricata_alerts(self, limit: int = 100) -> Dict:
        """Get Suricata alerts"""
        
        # Simulated alerts
        alerts = [
            {"timestamp": datetime.utcnow().isoformat(), "severity": "critical", "alert": "Malware Download Detected", "src_ip": "9.10.11.12", "dst_ip": "10.0.0.2"},
            {"timestamp": datetime.utcnow().isoformat(), "severity": "warning", "alert": "Suspicious DNS Query", "src_ip": "13.14.15.16", "dst_ip": "8.8.8.8"}
        ]
        
        return {
            "ids": "suricata",
            "alerts": alerts[:limit],
            "total_alerts": len(alerts),
            "critical": len([a for a in alerts if a["severity"] == "critical"])
        }
    
    async def manage_snort_rules(self, action: str, rule: str = None) -> Dict:
        """Manage Snort rules"""
        
        if action == "list":
            return {"rules": ["alert tcp any any -> any 80", "alert icmp any any -> any any"]}
        elif action == "add" and rule:
            return {"status": "added", "rule": rule}
        elif action == "delete" and rule:
            return {"status": "deleted", "rule": rule}
        
        return {"error": "Invalid action"}
    
    async def manage_suricata_rules(self, action: str, rule: str = None) -> Dict:
        """Manage Suricata rules"""
        
        if action == "list":
            return {"rules": ["alert http any any -> any any", "alert tls any any -> any any"]}
        elif action == "add" and rule:
            return {"status": "added", "rule": rule}
        elif action == "delete" and rule:
            return {"status": "deleted", "rule": rule}
        
        return {"error": "Invalid action"}
    
    async def get_combined_alerts(self) -> Dict:
        """Get combined alerts from all IDS/IPS"""
        
        snort = await self.get_snort_alerts()
        suricata = await self.get_suricata_alerts()
        
        all_alerts = snort["alerts"] + suricata["alerts"]
        
        return {
            "total_alerts": len(all_alerts),
            "snort_alerts": snort["total_alerts"],
            "suricata_alerts": suricata["total_alerts"],
            "high_priority_count": snort.get("high_priority", 0) + suricata.get("critical", 0),
            "recent_alerts": sorted(all_alerts, key=lambda x: x["timestamp"], reverse=True)[:50]
        }

ids_ips_manager = IDSIPSManager()
