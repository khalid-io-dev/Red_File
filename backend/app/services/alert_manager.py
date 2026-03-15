"""
Alert Manager Service - Manage security alerts and notifications
"""
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import json

class AlertSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class AlertStatus(Enum):
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"

class AlertManager:
    """Manage security alerts and notifications"""
    
    def __init__(self):
        self.alerts = []
        self.rules = []
        self.notification_channels = []
        self.alert_counter = 0
    
    async def create_alert(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new security alert"""
        self.alert_counter += 1
        
        alert = {
            'id': f"ALT_{self.alert_counter:06d}",
            'title': alert_data.get('title'),
            'description': alert_data.get('description'),
            'severity': alert_data.get('severity', AlertSeverity.MEDIUM.value),
            'status': AlertStatus.NEW.value,
            'source': alert_data.get('source', 'SecureSight'),
            'category': alert_data.get('category', 'security'),
            'tags': alert_data.get('tags', []),
            'affected_assets': alert_data.get('affected_assets', []),
            'indicators': alert_data.get('indicators', {}),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'assigned_to': alert_data.get('assigned_to'),
            'priority': self._calculate_priority(alert_data.get('severity')),
            'metadata': alert_data.get('metadata', {})
        }
        
        self.alerts.append(alert)
        
        # Trigger notifications
        await self._send_notifications(alert)
        
        return alert
    
    async def get_alerts(self, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Get alerts with optional filters"""
        filtered = self.alerts
        
        if filters:
            if 'severity' in filters:
                filtered = [a for a in filtered if a['severity'] == filters['severity']]
            if 'status' in filters:
                filtered = [a for a in filtered if a['status'] == filters['status']]
            if 'category' in filters:
                filtered = [a for a in filtered if a['category'] == filters['category']]
            if 'assigned_to' in filters:
                filtered = [a for a in filtered if a['assigned_to'] == filters['assigned_to']]
        
        return sorted(filtered, key=lambda x: x['created_at'], reverse=True)
    
    async def update_alert(self, alert_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update alert"""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert.update(updates)
                alert['updated_at'] = datetime.utcnow().isoformat()
                return alert
        
        return {'error': 'Alert not found'}
    
    async def acknowledge_alert(self, alert_id: str, user: str) -> Dict[str, Any]:
        """Acknowledge alert"""
        return await self.update_alert(alert_id, {
            'status': AlertStatus.ACKNOWLEDGED.value,
            'acknowledged_by': user,
            'acknowledged_at': datetime.utcnow().isoformat()
        })
    
    async def resolve_alert(self, alert_id: str, resolution: str, user: str) -> Dict[str, Any]:
        """Resolve alert"""
        return await self.update_alert(alert_id, {
            'status': AlertStatus.RESOLVED.value,
            'resolution': resolution,
            'resolved_by': user,
            'resolved_at': datetime.utcnow().isoformat()
        })
    
    async def escalate_alert(self, alert_id: str, escalate_to: str, reason: str) -> Dict[str, Any]:
        """Escalate alert to higher priority"""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['escalated'] = True
                alert['escalated_to'] = escalate_to
                alert['escalation_reason'] = reason
                alert['escalated_at'] = datetime.utcnow().isoformat()
                
                # Increase priority
                if alert['severity'] == AlertSeverity.MEDIUM.value:
                    alert['severity'] = AlertSeverity.HIGH.value
                elif alert['severity'] == AlertSeverity.HIGH.value:
                    alert['severity'] = AlertSeverity.CRITICAL.value
                
                await self._send_notifications(alert, escalation=True)
                return alert
        
        return {'error': 'Alert not found'}
    
    async def create_alert_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create alert rule"""
        rule = {
            'id': f"RULE_{len(self.rules) + 1:04d}",
            'name': rule_data.get('name'),
            'description': rule_data.get('description'),
            'conditions': rule_data.get('conditions', []),
            'severity': rule_data.get('severity', AlertSeverity.MEDIUM.value),
            'actions': rule_data.get('actions', []),
            'enabled': rule_data.get('enabled', True),
            'created_at': datetime.utcnow().isoformat()
        }
        
        self.rules.append(rule)
        return rule
    
    async def evaluate_rules(self, event: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate event against alert rules"""
        triggered_alerts = []
        
        for rule in self.rules:
            if not rule['enabled']:
                continue
            
            if self._evaluate_conditions(event, rule['conditions']):
                alert = await self.create_alert({
                    'title': f"Rule triggered: {rule['name']}",
                    'description': rule['description'],
                    'severity': rule['severity'],
                    'source': 'Alert Rule',
                    'metadata': {'rule_id': rule['id'], 'event': event}
                })
                triggered_alerts.append(alert)
        
        return triggered_alerts
    
    async def add_notification_channel(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add notification channel"""
        channel = {
            'id': f"CH_{len(self.notification_channels) + 1:04d}",
            'type': channel_data.get('type'),  # email, slack, webhook, sms
            'name': channel_data.get('name'),
            'config': channel_data.get('config', {}),
            'enabled': channel_data.get('enabled', True),
            'severity_filter': channel_data.get('severity_filter', [])
        }
        
        self.notification_channels.append(channel)
        return channel
    
    async def send_notification(self, channel_id: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Send notification to specific channel"""
        for channel in self.notification_channels:
            if channel['id'] == channel_id and channel['enabled']:
                return await self._send_to_channel(channel, message)
        
        return {'error': 'Channel not found or disabled'}
    
    async def get_alert_statistics(self, time_range: str = '24h') -> Dict[str, Any]:
        """Get alert statistics"""
        now = datetime.utcnow()
        hours = int(time_range.replace('h', ''))
        cutoff = now - timedelta(hours=hours)
        
        recent_alerts = [
            a for a in self.alerts
            if datetime.fromisoformat(a['created_at']) > cutoff
        ]
        
        return {
            'total': len(recent_alerts),
            'by_severity': {
                'critical': len([a for a in recent_alerts if a['severity'] == 'critical']),
                'high': len([a for a in recent_alerts if a['severity'] == 'high']),
                'medium': len([a for a in recent_alerts if a['severity'] == 'medium']),
                'low': len([a for a in recent_alerts if a['severity'] == 'low'])
            },
            'by_status': {
                'new': len([a for a in recent_alerts if a['status'] == 'new']),
                'acknowledged': len([a for a in recent_alerts if a['status'] == 'acknowledged']),
                'in_progress': len([a for a in recent_alerts if a['status'] == 'in_progress']),
                'resolved': len([a for a in recent_alerts if a['status'] == 'resolved'])
            },
            'by_category': self._count_by_field(recent_alerts, 'category'),
            'time_range': time_range
        }
    
    async def get_alert_trends(self, days: int = 7) -> Dict[str, Any]:
        """Get alert trends over time"""
        trends = []
        now = datetime.utcnow()
        
        for i in range(days):
            day_start = now - timedelta(days=i+1)
            day_end = now - timedelta(days=i)
            
            day_alerts = [
                a for a in self.alerts
                if day_start < datetime.fromisoformat(a['created_at']) <= day_end
            ]
            
            trends.append({
                'date': day_start.strftime('%Y-%m-%d'),
                'total': len(day_alerts),
                'critical': len([a for a in day_alerts if a['severity'] == 'critical']),
                'high': len([a for a in day_alerts if a['severity'] == 'high'])
            })
        
        return {'trends': list(reversed(trends))}
    
    async def correlate_alerts(self, alert_ids: List[str]) -> Dict[str, Any]:
        """Correlate multiple alerts"""
        alerts = [a for a in self.alerts if a['id'] in alert_ids]
        
        if not alerts:
            return {'error': 'No alerts found'}
        
        # Find common patterns
        common_tags = set(alerts[0].get('tags', []))
        for alert in alerts[1:]:
            common_tags &= set(alert.get('tags', []))
        
        common_assets = set(alerts[0].get('affected_assets', []))
        for alert in alerts[1:]:
            common_assets &= set(alert.get('affected_assets', []))
        
        return {
            'correlated_alerts': len(alerts),
            'common_tags': list(common_tags),
            'common_assets': list(common_assets),
            'time_span': {
                'start': min(a['created_at'] for a in alerts),
                'end': max(a['created_at'] for a in alerts)
            },
            'severity_distribution': self._count_by_field(alerts, 'severity'),
            'recommendation': 'Consider creating incident from correlated alerts'
        }
    
    async def create_incident_from_alerts(self, alert_ids: List[str], incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create incident from multiple alerts"""
        alerts = [a for a in self.alerts if a['id'] in alert_ids]
        
        incident = {
            'id': f"INC_{datetime.utcnow().timestamp()}",
            'title': incident_data.get('title'),
            'description': incident_data.get('description'),
            'severity': max([a['severity'] for a in alerts], key=lambda x: ['low', 'medium', 'high', 'critical'].index(x)),
            'status': 'open',
            'alerts': alert_ids,
            'created_at': datetime.utcnow().isoformat(),
            'assigned_to': incident_data.get('assigned_to')
        }
        
        # Update alerts to reference incident
        for alert_id in alert_ids:
            await self.update_alert(alert_id, {'incident_id': incident['id']})
        
        return incident
    
    async def suppress_alert(self, alert_id: str, duration: int, reason: str) -> Dict[str, Any]:
        """Suppress alert for specified duration (minutes)"""
        return await self.update_alert(alert_id, {
            'suppressed': True,
            'suppressed_until': (datetime.utcnow() + timedelta(minutes=duration)).isoformat(),
            'suppression_reason': reason
        })
    
    async def get_top_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top priority alerts"""
        priority_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1, 'info': 0}
        
        sorted_alerts = sorted(
            [a for a in self.alerts if a['status'] == 'new'],
            key=lambda x: priority_order.get(x['severity'], 0),
            reverse=True
        )
        
        return sorted_alerts[:limit]
    
    def _calculate_priority(self, severity: str) -> int:
        """Calculate numeric priority from severity"""
        priority_map = {
            'critical': 1,
            'high': 2,
            'medium': 3,
            'low': 4,
            'info': 5
        }
        return priority_map.get(severity, 3)
    
    def _evaluate_conditions(self, event: Dict[str, Any], conditions: List[Dict]) -> bool:
        """Evaluate if event matches rule conditions"""
        for condition in conditions:
            field = condition.get('field')
            operator = condition.get('operator')
            value = condition.get('value')
            
            event_value = event.get(field)
            
            if operator == 'equals' and event_value != value:
                return False
            elif operator == 'contains' and value not in str(event_value):
                return False
            elif operator == 'greater_than' and not (event_value > value):
                return False
        
        return True
    
    async def _send_notifications(self, alert: Dict[str, Any], escalation: bool = False) -> None:
        """Send notifications for alert"""
        for channel in self.notification_channels:
            if not channel['enabled']:
                continue
            
            # Check severity filter
            if channel['severity_filter'] and alert['severity'] not in channel['severity_filter']:
                continue
            
            await self._send_to_channel(channel, {
                'alert': alert,
                'escalation': escalation
            })
    
    async def _send_to_channel(self, channel: Dict[str, Any], message: Dict[str, Any]) -> Dict[str, Any]:
        """Send message to notification channel"""
        # Simulated sending
        return {
            'status': 'sent',
            'channel': channel['name'],
            'type': channel['type'],
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _count_by_field(self, items: List[Dict], field: str) -> Dict[str, int]:
        """Count items by field value"""
        counts = {}
        for item in items:
            value = item.get(field, 'unknown')
            counts[value] = counts.get(value, 0) + 1
        return counts

# Singleton
alert_manager = AlertManager()
