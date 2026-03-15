"""
Incident Response Service - Manage security incidents and response workflows
"""
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import json

class IncidentSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class IncidentStatus(Enum):
    NEW = "new"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    ERADICATED = "eradicated"
    RECOVERED = "recovered"
    CLOSED = "closed"

class IncidentCategory(Enum):
    MALWARE = "malware"
    PHISHING = "phishing"
    DATA_BREACH = "data_breach"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    DENIAL_OF_SERVICE = "denial_of_service"
    INSIDER_THREAT = "insider_threat"
    RANSOMWARE = "ransomware"
    APT = "apt"

class IncidentResponder:
    """Manage security incidents and response workflows"""
    
    def __init__(self):
        self.incidents = []
        self.playbooks = []
        self.incident_counter = 0
    
    async def create_incident(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new security incident"""
        self.incident_counter += 1
        
        incident = {
            'id': f"INC_{self.incident_counter:06d}",
            'title': incident_data.get('title'),
            'description': incident_data.get('description'),
            'severity': incident_data.get('severity', IncidentSeverity.MEDIUM.value),
            'status': IncidentStatus.NEW.value,
            'category': incident_data.get('category', IncidentCategory.UNAUTHORIZED_ACCESS.value),
            'affected_systems': incident_data.get('affected_systems', []),
            'affected_users': incident_data.get('affected_users', []),
            'indicators': incident_data.get('indicators', {}),
            'timeline': [{
                'timestamp': datetime.utcnow().isoformat(),
                'event': 'Incident created',
                'user': incident_data.get('reporter')
            }],
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'detected_at': incident_data.get('detected_at', datetime.utcnow().isoformat()),
            'reported_by': incident_data.get('reporter'),
            'assigned_to': incident_data.get('assigned_to'),
            'team': incident_data.get('team', []),
            'containment_actions': [],
            'eradication_actions': [],
            'recovery_actions': [],
            'lessons_learned': [],
            'estimated_impact': incident_data.get('estimated_impact', {}),
            'actual_impact': {},
            'root_cause': None,
            'metadata': incident_data.get('metadata', {})
        }
        
        self.incidents.append(incident)
        
        # Auto-assign playbook
        playbook = await self._select_playbook(incident)
        if playbook:
            incident['playbook_id'] = playbook['id']
        
        return incident
    
    async def get_incidents(self, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Get incidents with filters"""
        filtered = self.incidents
        
        if filters:
            if 'severity' in filters:
                filtered = [i for i in filtered if i['severity'] == filters['severity']]
            if 'status' in filters:
                filtered = [i for i in filtered if i['status'] == filters['status']]
            if 'category' in filters:
                filtered = [i for i in filtered if i['category'] == filters['category']]
            if 'assigned_to' in filters:
                filtered = [i for i in filtered if i['assigned_to'] == filters['assigned_to']]
        
        return sorted(filtered, key=lambda x: x['created_at'], reverse=True)
    
    async def update_incident_status(self, incident_id: str, status: str, notes: str, user: str) -> Dict[str, Any]:
        """Update incident status"""
        for incident in self.incidents:
            if incident['id'] == incident_id:
                incident['status'] = status
                incident['updated_at'] = datetime.utcnow().isoformat()
                incident['timeline'].append({
                    'timestamp': datetime.utcnow().isoformat(),
                    'event': f"Status changed to {status}",
                    'notes': notes,
                    'user': user
                })
                return incident
        
        return {'error': 'Incident not found'}
    
    async def add_containment_action(self, incident_id: str, action: Dict[str, Any]) -> Dict[str, Any]:
        """Add containment action"""
        for incident in self.incidents:
            if incident['id'] == incident_id:
                action['timestamp'] = datetime.utcnow().isoformat()
                action['id'] = f"ACT_{len(incident['containment_actions']) + 1:04d}"
                incident['containment_actions'].append(action)
                incident['timeline'].append({
                    'timestamp': datetime.utcnow().isoformat(),
                    'event': f"Containment action: {action.get('description')}",
                    'user': action.get('performed_by')
                })
                return action
        
        return {'error': 'Incident not found'}
    
    async def add_eradication_action(self, incident_id: str, action: Dict[str, Any]) -> Dict[str, Any]:
        """Add eradication action"""
        for incident in self.incidents:
            if incident['id'] == incident_id:
                action['timestamp'] = datetime.utcnow().isoformat()
                action['id'] = f"ACT_{len(incident['eradication_actions']) + 1:04d}"
                incident['eradication_actions'].append(action)
                incident['timeline'].append({
                    'timestamp': datetime.utcnow().isoformat(),
                    'event': f"Eradication action: {action.get('description')}",
                    'user': action.get('performed_by')
                })
                return action
        
        return {'error': 'Incident not found'}
    
    async def add_recovery_action(self, incident_id: str, action: Dict[str, Any]) -> Dict[str, Any]:
        """Add recovery action"""
        for incident in self.incidents:
            if incident['id'] == incident_id:
                action['timestamp'] = datetime.utcnow().isoformat()
                action['id'] = f"ACT_{len(incident['recovery_actions']) + 1:04d}"
                incident['recovery_actions'].append(action)
                incident['timeline'].append({
                    'timestamp': datetime.utcnow().isoformat(),
                    'event': f"Recovery action: {action.get('description')}",
                    'user': action.get('performed_by')
                })
                return action
        
        return {'error': 'Incident not found'}
    
    async def create_playbook(self, playbook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create incident response playbook"""
        playbook = {
            'id': f"PB_{len(self.playbooks) + 1:04d}",
            'name': playbook_data.get('name'),
            'description': playbook_data.get('description'),
            'category': playbook_data.get('category'),
            'severity': playbook_data.get('severity'),
            'phases': playbook_data.get('phases', []),
            'steps': playbook_data.get('steps', []),
            'roles': playbook_data.get('roles', []),
            'tools': playbook_data.get('tools', []),
            'estimated_time': playbook_data.get('estimated_time'),
            'created_at': datetime.utcnow().isoformat()
        }
        
        self.playbooks.append(playbook)
        return playbook
    
    async def get_playbooks(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get incident response playbooks"""
        if category:
            return [p for p in self.playbooks if p['category'] == category]
        return self.playbooks
    
    async def execute_playbook(self, incident_id: str, playbook_id: str) -> Dict[str, Any]:
        """Execute playbook for incident"""
        incident = next((i for i in self.incidents if i['id'] == incident_id), None)
        playbook = next((p for p in self.playbooks if p['id'] == playbook_id), None)
        
        if not incident or not playbook:
            return {'error': 'Incident or playbook not found'}
        
        execution = {
            'incident_id': incident_id,
            'playbook_id': playbook_id,
            'started_at': datetime.utcnow().isoformat(),
            'status': 'in_progress',
            'completed_steps': [],
            'pending_steps': playbook['steps'].copy()
        }
        
        incident['playbook_execution'] = execution
        incident['timeline'].append({
            'timestamp': datetime.utcnow().isoformat(),
            'event': f"Playbook execution started: {playbook['name']}"
        })
        
        return execution
    
    async def complete_playbook_step(self, incident_id: str, step_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Mark playbook step as complete"""
        for incident in self.incidents:
            if incident['id'] == incident_id and 'playbook_execution' in incident:
                execution = incident['playbook_execution']
                execution['completed_steps'].append({
                    'step_id': step_id,
                    'result': result,
                    'completed_at': datetime.utcnow().isoformat()
                })
                return execution
        
        return {'error': 'Incident or execution not found'}
    
    async def escalate_incident(self, incident_id: str, escalate_to: str, reason: str) -> Dict[str, Any]:
        """Escalate incident"""
        for incident in self.incidents:
            if incident['id'] == incident_id:
                incident['escalated'] = True
                incident['escalated_to'] = escalate_to
                incident['escalation_reason'] = reason
                incident['escalated_at'] = datetime.utcnow().isoformat()
                
                # Increase severity
                if incident['severity'] == IncidentSeverity.MEDIUM.value:
                    incident['severity'] = IncidentSeverity.HIGH.value
                elif incident['severity'] == IncidentSeverity.HIGH.value:
                    incident['severity'] = IncidentSeverity.CRITICAL.value
                
                incident['timeline'].append({
                    'timestamp': datetime.utcnow().isoformat(),
                    'event': f"Incident escalated to {escalate_to}",
                    'reason': reason
                })
                
                return incident
        
        return {'error': 'Incident not found'}
    
    async def add_evidence(self, incident_id: str, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """Add evidence to incident"""
        for incident in self.incidents:
            if incident['id'] == incident_id:
                if 'evidence' not in incident:
                    incident['evidence'] = []
                
                evidence['id'] = f"EVD_{len(incident['evidence']) + 1:04d}"
                evidence['collected_at'] = datetime.utcnow().isoformat()
                incident['evidence'].append(evidence)
                
                incident['timeline'].append({
                    'timestamp': datetime.utcnow().isoformat(),
                    'event': f"Evidence added: {evidence.get('type')}",
                    'user': evidence.get('collected_by')
                })
                
                return evidence
        
        return {'error': 'Incident not found'}
    
    async def calculate_impact(self, incident_id: str) -> Dict[str, Any]:
        """Calculate incident impact"""
        incident = next((i for i in self.incidents if i['id'] == incident_id), None)
        
        if not incident:
            return {'error': 'Incident not found'}
        
        impact = {
            'systems_affected': len(incident.get('affected_systems', [])),
            'users_affected': len(incident.get('affected_users', [])),
            'data_compromised': incident.get('estimated_impact', {}).get('data_compromised', False),
            'downtime_hours': incident.get('estimated_impact', {}).get('downtime_hours', 0),
            'financial_impact': incident.get('estimated_impact', {}).get('financial_impact', 0),
            'reputation_impact': incident.get('estimated_impact', {}).get('reputation_impact', 'low'),
            'compliance_impact': incident.get('estimated_impact', {}).get('compliance_impact', False)
        }
        
        # Calculate overall impact score (0-100)
        score = 0
        score += min(impact['systems_affected'] * 5, 25)
        score += min(impact['users_affected'] * 2, 25)
        score += 20 if impact['data_compromised'] else 0
        score += min(impact['downtime_hours'] * 2, 15)
        score += 15 if impact['compliance_impact'] else 0
        
        impact['overall_score'] = min(score, 100)
        impact['impact_level'] = 'critical' if score > 75 else 'high' if score > 50 else 'medium' if score > 25 else 'low'
        
        incident['actual_impact'] = impact
        return impact
    
    async def generate_incident_report(self, incident_id: str) -> Dict[str, Any]:
        """Generate incident report"""
        incident = next((i for i in self.incidents if i['id'] == incident_id), None)
        
        if not incident:
            return {'error': 'Incident not found'}
        
        report = {
            'incident_id': incident['id'],
            'title': incident['title'],
            'executive_summary': self._generate_executive_summary(incident),
            'timeline': incident['timeline'],
            'affected_assets': {
                'systems': incident.get('affected_systems', []),
                'users': incident.get('affected_users', [])
            },
            'indicators_of_compromise': incident.get('indicators', {}),
            'response_actions': {
                'containment': incident.get('containment_actions', []),
                'eradication': incident.get('eradication_actions', []),
                'recovery': incident.get('recovery_actions', [])
            },
            'impact_assessment': incident.get('actual_impact', {}),
            'root_cause': incident.get('root_cause'),
            'lessons_learned': incident.get('lessons_learned', []),
            'recommendations': self._generate_recommendations(incident),
            'generated_at': datetime.utcnow().isoformat()
        }
        
        return report
    
    async def close_incident(self, incident_id: str, closure_notes: str, user: str) -> Dict[str, Any]:
        """Close incident"""
        incident = await self.update_incident_status(incident_id, IncidentStatus.CLOSED.value, closure_notes, user)
        
        if 'error' not in incident:
            incident['closed_at'] = datetime.utcnow().isoformat()
            incident['closed_by'] = user
            
            # Calculate metrics
            created = datetime.fromisoformat(incident['created_at'])
            closed = datetime.fromisoformat(incident['closed_at'])
            incident['resolution_time_hours'] = (closed - created).total_seconds() / 3600
        
        return incident
    
    async def get_incident_statistics(self, time_range: str = '30d') -> Dict[str, Any]:
        """Get incident statistics"""
        days = int(time_range.replace('d', ''))
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        recent = [
            i for i in self.incidents
            if datetime.fromisoformat(i['created_at']) > cutoff
        ]
        
        return {
            'total_incidents': len(recent),
            'by_severity': self._count_by_field(recent, 'severity'),
            'by_status': self._count_by_field(recent, 'status'),
            'by_category': self._count_by_field(recent, 'category'),
            'average_resolution_time': self._calculate_avg_resolution_time(recent),
            'open_incidents': len([i for i in recent if i['status'] != 'closed']),
            'closed_incidents': len([i for i in recent if i['status'] == 'closed'])
        }
    
    def _select_playbook(self, incident: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Auto-select appropriate playbook"""
        for playbook in self.playbooks:
            if playbook['category'] == incident['category']:
                return playbook
        return None
    
    def _generate_executive_summary(self, incident: Dict[str, Any]) -> str:
        """Generate executive summary"""
        return f"Security incident {incident['id']} involving {incident['category']} was detected on {incident['detected_at']}. " \
               f"The incident affected {len(incident.get('affected_systems', []))} systems and {len(incident.get('affected_users', []))} users. " \
               f"Current status: {incident['status']}. Severity: {incident['severity']}."
    
    def _generate_recommendations(self, incident: Dict[str, Any]) -> List[str]:
        """Generate recommendations"""
        recommendations = [
            "Implement additional monitoring for similar attack patterns",
            "Review and update security policies",
            "Conduct security awareness training",
            "Perform vulnerability assessment on affected systems"
        ]
        
        if incident['category'] == 'phishing':
            recommendations.append("Deploy email filtering solution")
        elif incident['category'] == 'malware':
            recommendations.append("Update antivirus signatures")
        
        return recommendations
    
    def _count_by_field(self, items: List[Dict], field: str) -> Dict[str, int]:
        """Count items by field"""
        counts = {}
        for item in items:
            value = item.get(field, 'unknown')
            counts[value] = counts.get(value, 0) + 1
        return counts
    
    def _calculate_avg_resolution_time(self, incidents: List[Dict]) -> float:
        """Calculate average resolution time"""
        closed = [i for i in incidents if i.get('closed_at')]
        
        if not closed:
            return 0.0
        
        total_hours = sum([
            (datetime.fromisoformat(i['closed_at']) - datetime.fromisoformat(i['created_at'])).total_seconds() / 3600
            for i in closed
        ])
        
        return round(total_hours / len(closed), 2)

# Singleton
incident_responder = IncidentResponder()
