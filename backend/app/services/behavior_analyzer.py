"""
Behavior Analyzer Service - User and Entity Behavior Analytics (UEBA)
"""
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class BehaviorAnalyzer:
    """Analyze user and entity behavior for anomalies"""
    
    def __init__(self):
        self.baselines = {}
        self.profiles = {}
        self.risk_scores = {}
    
    async def analyze_user(self, user_id: str, activities: List[Dict]) -> Dict[str, Any]:
        """Analyze user behavior"""
        baseline = await self._get_or_create_baseline(user_id, 'user')
        
        anomalies = []
        risk_score = 0.0
        
        # Analyze login patterns
        login_anomaly = await self._analyze_login_patterns(user_id, activities, baseline)
        if login_anomaly['is_anomalous']:
            anomalies.append(login_anomaly)
            risk_score += login_anomaly['risk_contribution']
        
        # Analyze access patterns
        access_anomaly = await self._analyze_access_patterns(user_id, activities, baseline)
        if access_anomaly['is_anomalous']:
            anomalies.append(access_anomaly)
            risk_score += access_anomaly['risk_contribution']
        
        # Analyze data access
        data_anomaly = await self._analyze_data_access(user_id, activities, baseline)
        if data_anomaly['is_anomalous']:
            anomalies.append(data_anomaly)
            risk_score += data_anomaly['risk_contribution']
        
        # Analyze time patterns
        time_anomaly = await self._analyze_time_patterns(user_id, activities, baseline)
        if time_anomaly['is_anomalous']:
            anomalies.append(time_anomaly)
            risk_score += time_anomaly['risk_contribution']
        
        risk_score = min(risk_score, 100)
        
        return {
            'user_id': user_id,
            'risk_score': risk_score,
            'risk_level': self._calculate_risk_level(risk_score),
            'anomalies': anomalies,
            'total_activities': len(activities),
            'baseline_deviation': self._calculate_deviation(activities, baseline),
            'recommendations': self._generate_user_recommendations(risk_score, anomalies)
        }
    
    async def analyze_entity(self, entity_id: str, entity_type: str, activities: List[Dict]) -> Dict[str, Any]:
        """Analyze entity behavior (device, service, application)"""
        baseline = await self._get_or_create_baseline(entity_id, entity_type)
        
        anomalies = []
        risk_score = 0.0
        
        # Analyze communication patterns
        comm_anomaly = await self._analyze_communication_patterns(entity_id, activities, baseline)
        if comm_anomaly['is_anomalous']:
            anomalies.append(comm_anomaly)
            risk_score += comm_anomaly['risk_contribution']
        
        # Analyze resource usage
        resource_anomaly = await self._analyze_resource_usage(entity_id, activities, baseline)
        if resource_anomaly['is_anomalous']:
            anomalies.append(resource_anomaly)
            risk_score += resource_anomaly['risk_contribution']
        
        # Analyze network behavior
        network_anomaly = await self._analyze_network_behavior(entity_id, activities, baseline)
        if network_anomaly['is_anomalous']:
            anomalies.append(network_anomaly)
            risk_score += network_anomaly['risk_contribution']
        
        risk_score = min(risk_score, 100)
        
        return {
            'entity_id': entity_id,
            'entity_type': entity_type,
            'risk_score': risk_score,
            'risk_level': self._calculate_risk_level(risk_score),
            'anomalies': anomalies,
            'baseline_deviation': self._calculate_deviation(activities, baseline),
            'recommendations': self._generate_entity_recommendations(risk_score, anomalies)
        }
    
    async def create_baseline(self, subject_id: str, subject_type: str, historical_data: List[Dict]) -> Dict[str, Any]:
        """Create behavioral baseline"""
        baseline = {
            'subject_id': subject_id,
            'subject_type': subject_type,
            'created_at': datetime.utcnow().isoformat(),
            'data_points': len(historical_data),
            'patterns': {}
        }
        
        if subject_type == 'user':
            baseline['patterns'] = {
                'typical_login_hours': self._extract_typical_hours(historical_data, 'login'),
                'typical_locations': self._extract_typical_locations(historical_data),
                'typical_resources': self._extract_typical_resources(historical_data),
                'avg_session_duration': self._calculate_avg_duration(historical_data),
                'typical_data_volume': self._calculate_avg_data_volume(historical_data)
            }
        else:
            baseline['patterns'] = {
                'typical_connections': self._extract_typical_connections(historical_data),
                'typical_protocols': self._extract_typical_protocols(historical_data),
                'avg_bandwidth': self._calculate_avg_bandwidth(historical_data),
                'typical_ports': self._extract_typical_ports(historical_data)
            }
        
        self.baselines[subject_id] = baseline
        return baseline
    
    async def detect_insider_threat(self, user_id: str, activities: List[Dict]) -> Dict[str, Any]:
        """Detect potential insider threat indicators"""
        indicators = []
        threat_score = 0.0
        
        # Check for data hoarding
        if self._detect_data_hoarding(activities):
            indicators.append({
                'type': 'data_hoarding',
                'description': 'Unusual data collection behavior',
                'severity': 'high'
            })
            threat_score += 25
        
        # Check for after-hours access
        if self._detect_after_hours_access(activities):
            indicators.append({
                'type': 'after_hours_access',
                'description': 'Access during unusual hours',
                'severity': 'medium'
            })
            threat_score += 15
        
        # Check for privilege escalation attempts
        if self._detect_privilege_escalation(activities):
            indicators.append({
                'type': 'privilege_escalation',
                'description': 'Attempted privilege escalation',
                'severity': 'critical'
            })
            threat_score += 35
        
        # Check for unauthorized access attempts
        if self._detect_unauthorized_access(activities):
            indicators.append({
                'type': 'unauthorized_access',
                'description': 'Access to unauthorized resources',
                'severity': 'high'
            })
            threat_score += 25
        
        return {
            'user_id': user_id,
            'is_threat': threat_score > 50,
            'threat_score': min(threat_score, 100),
            'threat_level': 'critical' if threat_score > 75 else 'high' if threat_score > 50 else 'medium' if threat_score > 25 else 'low',
            'indicators': indicators,
            'recommended_actions': self._recommend_insider_actions(threat_score)
        }
    
    async def analyze_peer_group(self, user_id: str, peer_group: List[str], activities: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Analyze user behavior compared to peer group"""
        user_activities = activities.get(user_id, [])
        
        # Calculate peer group statistics
        peer_stats = {
            'avg_login_count': 0,
            'avg_data_access': 0,
            'avg_session_duration': 0
        }
        
        for peer_id in peer_group:
            if peer_id != user_id and peer_id in activities:
                peer_activities = activities[peer_id]
                peer_stats['avg_login_count'] += len([a for a in peer_activities if a.get('type') == 'login'])
                peer_stats['avg_data_access'] += len([a for a in peer_activities if a.get('type') == 'data_access'])
        
        if peer_group:
            for key in peer_stats:
                peer_stats[key] /= len(peer_group)
        
        # Compare user to peers
        user_login_count = len([a for a in user_activities if a.get('type') == 'login'])
        user_data_access = len([a for a in user_activities if a.get('type') == 'data_access'])
        
        deviations = []
        
        if user_login_count > peer_stats['avg_login_count'] * 2:
            deviations.append({
                'metric': 'login_frequency',
                'user_value': user_login_count,
                'peer_avg': peer_stats['avg_login_count'],
                'deviation_factor': user_login_count / max(peer_stats['avg_login_count'], 1)
            })
        
        if user_data_access > peer_stats['avg_data_access'] * 2:
            deviations.append({
                'metric': 'data_access',
                'user_value': user_data_access,
                'peer_avg': peer_stats['avg_data_access'],
                'deviation_factor': user_data_access / max(peer_stats['avg_data_access'], 1)
            })
        
        return {
            'user_id': user_id,
            'peer_group_size': len(peer_group),
            'is_outlier': len(deviations) > 0,
            'deviations': deviations,
            'peer_stats': peer_stats
        }
    
    async def track_behavior_change(self, subject_id: str, time_window: int = 30) -> Dict[str, Any]:
        """Track behavior changes over time"""
        # Simulated behavior change tracking
        return {
            'subject_id': subject_id,
            'time_window_days': time_window,
            'changes_detected': [
                {
                    'metric': 'login_frequency',
                    'change_percentage': 45,
                    'direction': 'increase',
                    'significance': 'high'
                },
                {
                    'metric': 'data_access_volume',
                    'change_percentage': 120,
                    'direction': 'increase',
                    'significance': 'critical'
                }
            ],
            'trend': 'increasing_risk',
            'recommendation': 'Investigate immediately'
        }
    
    async def calculate_risk_score(self, subject_id: str, subject_type: str) -> Dict[str, Any]:
        """Calculate comprehensive risk score"""
        base_score = self.risk_scores.get(subject_id, 50)
        
        factors = {
            'behavioral_anomalies': 20,
            'policy_violations': 15,
            'access_patterns': 10,
            'peer_deviation': 5
        }
        
        return {
            'subject_id': subject_id,
            'risk_score': base_score,
            'risk_level': self._calculate_risk_level(base_score),
            'contributing_factors': factors,
            'last_updated': datetime.utcnow().isoformat()
        }
    
    async def _get_or_create_baseline(self, subject_id: str, subject_type: str) -> Dict[str, Any]:
        """Get or create baseline for subject"""
        if subject_id not in self.baselines:
            self.baselines[subject_id] = {
                'subject_id': subject_id,
                'subject_type': subject_type,
                'patterns': {}
            }
        return self.baselines[subject_id]
    
    async def _analyze_login_patterns(self, user_id: str, activities: List[Dict], baseline: Dict) -> Dict[str, Any]:
        """Analyze login patterns"""
        logins = [a for a in activities if a.get('type') == 'login']
        
        # Check for unusual login times
        unusual_times = len([l for l in logins if self._is_unusual_time(l.get('timestamp'))])
        
        # Check for multiple failed attempts
        failed_logins = len([l for l in logins if l.get('status') == 'failed'])
        
        is_anomalous = unusual_times > 2 or failed_logins > 3
        
        return {
            'type': 'login_pattern',
            'is_anomalous': is_anomalous,
            'details': {
                'total_logins': len(logins),
                'unusual_time_logins': unusual_times,
                'failed_logins': failed_logins
            },
            'risk_contribution': 20 if is_anomalous else 0
        }
    
    async def _analyze_access_patterns(self, user_id: str, activities: List[Dict], baseline: Dict) -> Dict[str, Any]:
        """Analyze resource access patterns"""
        accesses = [a for a in activities if a.get('type') == 'access']
        
        # Check for unusual resource access
        unusual_resources = len([a for a in accesses if a.get('resource') not in baseline.get('patterns', {}).get('typical_resources', [])])
        
        is_anomalous = unusual_resources > 5
        
        return {
            'type': 'access_pattern',
            'is_anomalous': is_anomalous,
            'details': {
                'total_accesses': len(accesses),
                'unusual_resources': unusual_resources
            },
            'risk_contribution': 15 if is_anomalous else 0
        }
    
    async def _analyze_data_access(self, user_id: str, activities: List[Dict], baseline: Dict) -> Dict[str, Any]:
        """Analyze data access behavior"""
        data_accesses = [a for a in activities if a.get('type') == 'data_access']
        
        total_volume = sum([a.get('volume', 0) for a in data_accesses])
        baseline_volume = baseline.get('patterns', {}).get('typical_data_volume', 1000000)
        
        is_anomalous = total_volume > baseline_volume * 3
        
        return {
            'type': 'data_access',
            'is_anomalous': is_anomalous,
            'details': {
                'total_volume': total_volume,
                'baseline_volume': baseline_volume,
                'deviation_factor': total_volume / max(baseline_volume, 1)
            },
            'risk_contribution': 25 if is_anomalous else 0
        }
    
    async def _analyze_time_patterns(self, user_id: str, activities: List[Dict], baseline: Dict) -> Dict[str, Any]:
        """Analyze time-based patterns"""
        after_hours = len([a for a in activities if self._is_after_hours(a.get('timestamp'))])
        
        is_anomalous = after_hours > len(activities) * 0.3
        
        return {
            'type': 'time_pattern',
            'is_anomalous': is_anomalous,
            'details': {
                'after_hours_activities': after_hours,
                'total_activities': len(activities)
            },
            'risk_contribution': 15 if is_anomalous else 0
        }
    
    async def _analyze_communication_patterns(self, entity_id: str, activities: List[Dict], baseline: Dict) -> Dict[str, Any]:
        """Analyze entity communication patterns"""
        connections = [a for a in activities if a.get('type') == 'connection']
        
        unusual_destinations = len([c for c in connections if c.get('destination') not in baseline.get('patterns', {}).get('typical_connections', [])])
        
        is_anomalous = unusual_destinations > 10
        
        return {
            'type': 'communication_pattern',
            'is_anomalous': is_anomalous,
            'details': {
                'total_connections': len(connections),
                'unusual_destinations': unusual_destinations
            },
            'risk_contribution': 20 if is_anomalous else 0
        }
    
    async def _analyze_resource_usage(self, entity_id: str, activities: List[Dict], baseline: Dict) -> Dict[str, Any]:
        """Analyze resource usage"""
        cpu_usage = sum([a.get('cpu', 0) for a in activities]) / max(len(activities), 1)
        
        is_anomalous = cpu_usage > 80
        
        return {
            'type': 'resource_usage',
            'is_anomalous': is_anomalous,
            'details': {
                'avg_cpu_usage': cpu_usage
            },
            'risk_contribution': 15 if is_anomalous else 0
        }
    
    async def _analyze_network_behavior(self, entity_id: str, activities: List[Dict], baseline: Dict) -> Dict[str, Any]:
        """Analyze network behavior"""
        network_activities = [a for a in activities if a.get('type') == 'network']
        
        total_bandwidth = sum([a.get('bandwidth', 0) for a in network_activities])
        baseline_bandwidth = baseline.get('patterns', {}).get('avg_bandwidth', 1000000)
        
        is_anomalous = total_bandwidth > baseline_bandwidth * 5
        
        return {
            'type': 'network_behavior',
            'is_anomalous': is_anomalous,
            'details': {
                'total_bandwidth': total_bandwidth,
                'baseline_bandwidth': baseline_bandwidth
            },
            'risk_contribution': 20 if is_anomalous else 0
        }
    
    def _calculate_risk_level(self, score: float) -> str:
        """Calculate risk level from score"""
        if score > 75:
            return 'critical'
        elif score > 50:
            return 'high'
        elif score > 25:
            return 'medium'
        return 'low'
    
    def _calculate_deviation(self, activities: List[Dict], baseline: Dict) -> float:
        """Calculate deviation from baseline"""
        return 0.35  # Simulated
    
    def _generate_user_recommendations(self, risk_score: float, anomalies: List[Dict]) -> List[str]:
        """Generate recommendations for user"""
        recommendations = []
        if risk_score > 75:
            recommendations.append('Lock account immediately')
            recommendations.append('Initiate security investigation')
        elif risk_score > 50:
            recommendations.append('Require additional authentication')
            recommendations.append('Monitor user activity closely')
        else:
            recommendations.append('Continue monitoring')
        return recommendations
    
    def _generate_entity_recommendations(self, risk_score: float, anomalies: List[Dict]) -> List[str]:
        """Generate recommendations for entity"""
        return ['Isolate from network', 'Run security scan', 'Review logs']
    
    def _detect_data_hoarding(self, activities: List[Dict]) -> bool:
        """Detect data hoarding behavior"""
        downloads = [a for a in activities if a.get('type') == 'download']
        return len(downloads) > 50
    
    def _detect_after_hours_access(self, activities: List[Dict]) -> bool:
        """Detect after-hours access"""
        after_hours = [a for a in activities if self._is_after_hours(a.get('timestamp'))]
        return len(after_hours) > len(activities) * 0.3
    
    def _detect_privilege_escalation(self, activities: List[Dict]) -> bool:
        """Detect privilege escalation attempts"""
        escalations = [a for a in activities if a.get('type') == 'privilege_change']
        return len(escalations) > 0
    
    def _detect_unauthorized_access(self, activities: List[Dict]) -> bool:
        """Detect unauthorized access"""
        unauthorized = [a for a in activities if a.get('authorized') == False]
        return len(unauthorized) > 0
    
    def _recommend_insider_actions(self, threat_score: float) -> List[str]:
        """Recommend actions for insider threat"""
        if threat_score > 75:
            return ['Suspend account', 'Notify security team', 'Preserve evidence', 'Initiate investigation']
        elif threat_score > 50:
            return ['Increase monitoring', 'Restrict access', 'Alert manager']
        return ['Continue monitoring', 'Document behavior']
    
    def _is_unusual_time(self, timestamp: str) -> bool:
        """Check if timestamp is unusual"""
        return False  # Simulated
    
    def _is_after_hours(self, timestamp: str) -> bool:
        """Check if timestamp is after hours"""
        return False  # Simulated
    
    def _extract_typical_hours(self, data: List[Dict], activity_type: str) -> List[int]:
        """Extract typical hours"""
        return [9, 10, 11, 12, 13, 14, 15, 16, 17]
    
    def _extract_typical_locations(self, data: List[Dict]) -> List[str]:
        """Extract typical locations"""
        return ['Office', 'Home']
    
    def _extract_typical_resources(self, data: List[Dict]) -> List[str]:
        """Extract typical resources"""
        return ['file_server', 'email', 'crm']
    
    def _calculate_avg_duration(self, data: List[Dict]) -> float:
        """Calculate average duration"""
        return 480.0  # 8 hours
    
    def _calculate_avg_data_volume(self, data: List[Dict]) -> float:
        """Calculate average data volume"""
        return 1000000.0  # 1MB
    
    def _extract_typical_connections(self, data: List[Dict]) -> List[str]:
        """Extract typical connections"""
        return ['internal_server', 'database']
    
    def _extract_typical_protocols(self, data: List[Dict]) -> List[str]:
        """Extract typical protocols"""
        return ['HTTPS', 'SSH']
    
    def _calculate_avg_bandwidth(self, data: List[Dict]) -> float:
        """Calculate average bandwidth"""
        return 1000000.0
    
    def _extract_typical_ports(self, data: List[Dict]) -> List[int]:
        """Extract typical ports"""
        return [80, 443, 22]

# Singleton
behavior_analyzer = BehaviorAnalyzer()
