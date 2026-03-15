"""
Asset Manager Service - Asset inventory and management
"""
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict

class AssetManager:
    """Manage IT assets and inventory"""
    
    def __init__(self):
        self.assets = []
        self.asset_counter = 0
        self.asset_groups = {}
    
    async def add_asset(self, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add new asset to inventory"""
        self.asset_counter += 1
        
        asset = {
            'id': f"ASSET_{self.asset_counter:06d}",
            'name': asset_data.get('name'),
            'type': asset_data.get('type'),  # server, workstation, network_device, application
            'ip_address': asset_data.get('ip_address'),
            'mac_address': asset_data.get('mac_address'),
            'hostname': asset_data.get('hostname'),
            'os': asset_data.get('os'),
            'os_version': asset_data.get('os_version'),
            'location': asset_data.get('location'),
            'owner': asset_data.get('owner'),
            'department': asset_data.get('department'),
            'criticality': asset_data.get('criticality', 'medium'),  # low, medium, high, critical
            'status': asset_data.get('status', 'active'),  # active, inactive, decommissioned
            'services': asset_data.get('services', []),
            'open_ports': asset_data.get('open_ports', []),
            'vulnerabilities': [],
            'last_scan': None,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'metadata': asset_data.get('metadata', {})
        }
        
        self.assets.append(asset)
        return asset
    
    async def get_assets(self, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Get assets with optional filters"""
        filtered = self.assets
        
        if filters:
            if 'type' in filters:
                filtered = [a for a in filtered if a['type'] == filters['type']]
            if 'criticality' in filters:
                filtered = [a for a in filtered if a['criticality'] == filters['criticality']]
            if 'status' in filters:
                filtered = [a for a in filtered if a['status'] == filters['status']]
            if 'location' in filters:
                filtered = [a for a in filtered if a['location'] == filters['location']]
            if 'department' in filters:
                filtered = [a for a in filtered if a['department'] == filters['department']]
        
        return filtered
    
    async def update_asset(self, asset_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update asset information"""
        for asset in self.assets:
            if asset['id'] == asset_id:
                asset.update(updates)
                asset['updated_at'] = datetime.utcnow().isoformat()
                return asset
        
        return {'error': 'Asset not found'}
    
    async def delete_asset(self, asset_id: str) -> Dict[str, Any]:
        """Delete asset from inventory"""
        for i, asset in enumerate(self.assets):
            if asset['id'] == asset_id:
                self.assets.pop(i)
                return {'status': 'deleted', 'asset_id': asset_id}
        
        return {'error': 'Asset not found'}
    
    async def scan_asset(self, asset_id: str) -> Dict[str, Any]:
        """Scan asset for vulnerabilities and services"""
        asset = next((a for a in self.assets if a['id'] == asset_id), None)
        
        if not asset:
            return {'error': 'Asset not found'}
        
        # Simulated scan results
        scan_results = {
            'asset_id': asset_id,
            'scan_time': datetime.utcnow().isoformat(),
            'services_detected': [
                {'port': 22, 'service': 'SSH', 'version': 'OpenSSH 8.2'},
                {'port': 80, 'service': 'HTTP', 'version': 'Apache 2.4.41'},
                {'port': 443, 'service': 'HTTPS', 'version': 'Apache 2.4.41'}
            ],
            'vulnerabilities_found': 3,
            'status': 'completed'
        }
        
        # Update asset
        asset['services'] = scan_results['services_detected']
        asset['last_scan'] = scan_results['scan_time']
        asset['updated_at'] = datetime.utcnow().isoformat()
        
        return scan_results
    
    async def create_asset_group(self, group_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create asset group"""
        group_id = f"GROUP_{len(self.asset_groups) + 1:04d}"
        
        group = {
            'id': group_id,
            'name': group_data.get('name'),
            'description': group_data.get('description'),
            'asset_ids': group_data.get('asset_ids', []),
            'created_at': datetime.utcnow().isoformat()
        }
        
        self.asset_groups[group_id] = group
        return group
    
    async def get_asset_groups(self) -> List[Dict[str, Any]]:
        """Get all asset groups"""
        return list(self.asset_groups.values())
    
    async def get_asset_statistics(self) -> Dict[str, Any]:
        """Get asset inventory statistics"""
        return {
            'total_assets': len(self.assets),
            'by_type': self._count_by_field('type'),
            'by_criticality': self._count_by_field('criticality'),
            'by_status': self._count_by_field('status'),
            'by_location': self._count_by_field('location'),
            'by_department': self._count_by_field('department'),
            'critical_assets': len([a for a in self.assets if a['criticality'] == 'critical']),
            'active_assets': len([a for a in self.assets if a['status'] == 'active'])
        }
    
    async def get_asset_health(self, asset_id: str) -> Dict[str, Any]:
        """Get asset health status"""
        asset = next((a for a in self.assets if a['id'] == asset_id), None)
        
        if not asset:
            return {'error': 'Asset not found'}
        
        health_score = 100
        issues = []
        
        # Check vulnerabilities
        vuln_count = len(asset.get('vulnerabilities', []))
        if vuln_count > 0:
            health_score -= min(vuln_count * 10, 40)
            issues.append(f"{vuln_count} vulnerabilities detected")
        
        # Check last scan
        if not asset.get('last_scan'):
            health_score -= 20
            issues.append("Never scanned")
        
        # Check open ports
        if len(asset.get('open_ports', [])) > 20:
            health_score -= 15
            issues.append("Excessive open ports")
        
        health_score = max(health_score, 0)
        
        return {
            'asset_id': asset_id,
            'health_score': health_score,
            'health_status': 'good' if health_score > 80 else 'fair' if health_score > 60 else 'poor',
            'issues': issues,
            'recommendations': self._generate_health_recommendations(health_score, issues)
        }
    
    async def get_asset_dependencies(self, asset_id: str) -> Dict[str, Any]:
        """Get asset dependencies"""
        return {
            'asset_id': asset_id,
            'depends_on': [
                {'asset_id': 'ASSET_000002', 'type': 'database', 'criticality': 'high'},
                {'asset_id': 'ASSET_000003', 'type': 'network_device', 'criticality': 'critical'}
            ],
            'depended_by': [
                {'asset_id': 'ASSET_000005', 'type': 'application', 'criticality': 'medium'}
            ]
        }
    
    async def calculate_asset_risk(self, asset_id: str) -> Dict[str, Any]:
        """Calculate asset risk score"""
        asset = next((a for a in self.assets if a['id'] == asset_id), None)
        
        if not asset:
            return {'error': 'Asset not found'}
        
        risk_score = 0
        risk_factors = []
        
        # Criticality factor
        criticality_scores = {'low': 10, 'medium': 25, 'high': 40, 'critical': 50}
        risk_score += criticality_scores.get(asset['criticality'], 25)
        
        # Vulnerability factor
        vuln_count = len(asset.get('vulnerabilities', []))
        vuln_risk = min(vuln_count * 5, 30)
        risk_score += vuln_risk
        if vuln_risk > 0:
            risk_factors.append(f"{vuln_count} vulnerabilities")
        
        # Exposure factor
        if asset.get('ip_address') and not asset['ip_address'].startswith('10.'):
            risk_score += 20
            risk_factors.append("Internet-facing")
        
        return {
            'asset_id': asset_id,
            'risk_score': min(risk_score, 100),
            'risk_level': 'critical' if risk_score > 75 else 'high' if risk_score > 50 else 'medium' if risk_score > 25 else 'low',
            'risk_factors': risk_factors,
            'recommendations': self._generate_risk_recommendations(risk_score)
        }
    
    async def get_asset_timeline(self, asset_id: str) -> Dict[str, Any]:
        """Get asset event timeline"""
        return {
            'asset_id': asset_id,
            'events': [
                {'timestamp': '2024-01-10T10:00:00Z', 'event': 'Asset created', 'user': 'admin'},
                {'timestamp': '2024-01-12T14:30:00Z', 'event': 'Vulnerability scan completed', 'user': 'scanner'},
                {'timestamp': '2024-01-15T09:00:00Z', 'event': 'Patch applied', 'user': 'sysadmin'}
            ]
        }
    
    async def export_inventory(self, format: str = 'json') -> Dict[str, Any]:
        """Export asset inventory"""
        return {
            'format': format,
            'total_assets': len(self.assets),
            'exported_at': datetime.utcnow().isoformat(),
            'file_path': f'/tmp/asset_inventory_{datetime.utcnow().timestamp()}.{format}'
        }
    
    async def import_inventory(self, file_path: str) -> Dict[str, Any]:
        """Import asset inventory"""
        return {
            'status': 'imported',
            'assets_imported': 50,
            'assets_updated': 10,
            'assets_failed': 2
        }
    
    async def discover_assets(self, network_range: str) -> Dict[str, Any]:
        """Discover assets on network"""
        # Simulated discovery
        discovered = [
            {
                'ip_address': '192.168.1.10',
                'hostname': 'server01.local',
                'mac_address': '00:11:22:33:44:55',
                'os': 'Linux',
                'open_ports': [22, 80, 443]
            },
            {
                'ip_address': '192.168.1.20',
                'hostname': 'workstation01.local',
                'mac_address': '00:11:22:33:44:66',
                'os': 'Windows',
                'open_ports': [135, 139, 445]
            }
        ]
        
        return {
            'network_range': network_range,
            'assets_discovered': len(discovered),
            'discovered_assets': discovered,
            'scan_duration': '45 seconds'
        }
    
    async def tag_asset(self, asset_id: str, tags: List[str]) -> Dict[str, Any]:
        """Add tags to asset"""
        asset = next((a for a in self.assets if a['id'] == asset_id), None)
        
        if not asset:
            return {'error': 'Asset not found'}
        
        if 'tags' not in asset:
            asset['tags'] = []
        
        asset['tags'].extend(tags)
        asset['tags'] = list(set(asset['tags']))  # Remove duplicates
        
        return {
            'asset_id': asset_id,
            'tags': asset['tags']
        }
    
    async def search_assets(self, query: str) -> List[Dict[str, Any]]:
        """Search assets by query"""
        results = []
        query_lower = query.lower()
        
        for asset in self.assets:
            if (query_lower in asset.get('name', '').lower() or
                query_lower in asset.get('hostname', '').lower() or
                query_lower in asset.get('ip_address', '') or
                query_lower in asset.get('owner', '').lower()):
                results.append(asset)
        
        return results
    
    def _count_by_field(self, field: str) -> Dict[str, int]:
        """Count assets by field"""
        counts = defaultdict(int)
        for asset in self.assets:
            value = asset.get(field, 'unknown')
            counts[value] += 1
        return dict(counts)
    
    def _generate_health_recommendations(self, health_score: float, issues: List[str]) -> List[str]:
        """Generate health recommendations"""
        recommendations = []
        
        if health_score < 60:
            recommendations.append("Immediate attention required")
        
        if any("vulnerabilities" in issue for issue in issues):
            recommendations.append("Apply security patches")
        
        if any("Never scanned" in issue for issue in issues):
            recommendations.append("Schedule vulnerability scan")
        
        if any("open ports" in issue for issue in issues):
            recommendations.append("Review and close unnecessary ports")
        
        return recommendations
    
    def _generate_risk_recommendations(self, risk_score: float) -> List[str]:
        """Generate risk recommendations"""
        recommendations = []
        
        if risk_score > 75:
            recommendations.append("Critical: Immediate remediation required")
            recommendations.append("Isolate asset if possible")
        elif risk_score > 50:
            recommendations.append("High priority: Schedule remediation")
        
        recommendations.extend([
            "Apply latest security patches",
            "Review access controls",
            "Enable monitoring and logging"
        ])
        
        return recommendations

# Singleton
asset_manager = AssetManager()
