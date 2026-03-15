"""
Anomaly Detector Service - Statistical anomaly detection
"""
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import deque
import statistics

class AnomalyDetector:
    """Statistical anomaly detection for security events"""
    
    def __init__(self):
        self.time_series_data = {}
        self.thresholds = {}
        self.detection_methods = ['zscore', 'iqr', 'moving_average', 'exponential_smoothing']
    
    async def detect_anomalies(self, data: List[float], method: str = 'zscore', threshold: float = 3.0) -> Dict[str, Any]:
        """Detect anomalies using specified method"""
        if method == 'zscore':
            return await self._zscore_detection(data, threshold)
        elif method == 'iqr':
            return await self._iqr_detection(data)
        elif method == 'moving_average':
            return await self._moving_average_detection(data, window=10)
        elif method == 'exponential_smoothing':
            return await self._exponential_smoothing_detection(data, alpha=0.3)
        else:
            return {'error': 'Unknown detection method'}
    
    async def detect_time_series_anomalies(self, series_id: str, values: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect anomalies in time series data"""
        if not values:
            return {'anomalies': [], 'total_points': 0}
        
        # Extract numeric values
        numeric_values = [v.get('value', 0) for v in values]
        
        # Detect using multiple methods
        zscore_result = await self._zscore_detection(numeric_values, 3.0)
        iqr_result = await self._iqr_detection(numeric_values)
        
        # Combine results
        anomaly_indices = set(zscore_result['anomaly_indices'] + iqr_result['anomaly_indices'])
        
        anomalies = []
        for idx in sorted(anomaly_indices):
            if idx < len(values):
                anomalies.append({
                    'index': idx,
                    'timestamp': values[idx].get('timestamp'),
                    'value': values[idx].get('value'),
                    'expected_range': zscore_result.get('expected_range', {}),
                    'deviation': abs(values[idx].get('value', 0) - statistics.mean(numeric_values)) if numeric_values else 0
                })
        
        return {
            'series_id': series_id,
            'total_points': len(values),
            'anomalies_detected': len(anomalies),
            'anomaly_rate': len(anomalies) / len(values) if values else 0,
            'anomalies': anomalies,
            'statistics': {
                'mean': statistics.mean(numeric_values) if numeric_values else 0,
                'median': statistics.median(numeric_values) if numeric_values else 0,
                'std_dev': statistics.stdev(numeric_values) if len(numeric_values) > 1 else 0
            }
        }
    
    async def detect_network_anomalies(self, network_data: List[Dict]) -> Dict[str, Any]:
        """Detect network traffic anomalies"""
        anomalies = []
        
        # Analyze packet rates
        packet_rates = [d.get('packet_rate', 0) for d in network_data]
        rate_anomalies = await self.detect_anomalies(packet_rates, method='zscore')
        
        # Analyze bandwidth
        bandwidth = [d.get('bandwidth', 0) for d in network_data]
        bandwidth_anomalies = await self.detect_anomalies(bandwidth, method='iqr')
        
        # Analyze connection counts
        connections = [d.get('connections', 0) for d in network_data]
        connection_anomalies = await self.detect_anomalies(connections, method='moving_average')
        
        # Combine anomalies
        for idx in rate_anomalies['anomaly_indices']:
            if idx < len(network_data):
                anomalies.append({
                    'type': 'packet_rate',
                    'timestamp': network_data[idx].get('timestamp'),
                    'value': packet_rates[idx],
                    'severity': 'high' if packet_rates[idx] > 10000 else 'medium'
                })
        
        for idx in bandwidth_anomalies['anomaly_indices']:
            if idx < len(network_data):
                anomalies.append({
                    'type': 'bandwidth',
                    'timestamp': network_data[idx].get('timestamp'),
                    'value': bandwidth[idx],
                    'severity': 'high' if bandwidth[idx] > 1000000000 else 'medium'
                })
        
        return {
            'total_samples': len(network_data),
            'anomalies_detected': len(anomalies),
            'anomalies': anomalies,
            'summary': {
                'packet_rate_anomalies': len(rate_anomalies['anomaly_indices']),
                'bandwidth_anomalies': len(bandwidth_anomalies['anomaly_indices']),
                'connection_anomalies': len(connection_anomalies['anomaly_indices'])
            }
        }
    
    async def detect_login_anomalies(self, login_events: List[Dict]) -> Dict[str, Any]:
        """Detect anomalous login patterns"""
        anomalies = []
        
        # Group by user
        user_logins = {}
        for event in login_events:
            user = event.get('user')
            if user not in user_logins:
                user_logins[user] = []
            user_logins[user].append(event)
        
        # Analyze each user
        for user, logins in user_logins.items():
            # Check for rapid successive logins
            if len(logins) > 10:
                anomalies.append({
                    'type': 'excessive_logins',
                    'user': user,
                    'count': len(logins),
                    'severity': 'high'
                })
            
            # Check for failed login spikes
            failed = [l for l in logins if l.get('status') == 'failed']
            if len(failed) > 5:
                anomalies.append({
                    'type': 'failed_login_spike',
                    'user': user,
                    'failed_count': len(failed),
                    'severity': 'critical'
                })
            
            # Check for unusual locations
            locations = set([l.get('location') for l in logins])
            if len(locations) > 3:
                anomalies.append({
                    'type': 'multiple_locations',
                    'user': user,
                    'locations': list(locations),
                    'severity': 'medium'
                })
        
        return {
            'total_events': len(login_events),
            'users_analyzed': len(user_logins),
            'anomalies_detected': len(anomalies),
            'anomalies': anomalies
        }
    
    async def detect_data_transfer_anomalies(self, transfer_data: List[Dict]) -> Dict[str, Any]:
        """Detect anomalous data transfers"""
        volumes = [t.get('volume', 0) for t in transfer_data]
        
        anomaly_result = await self.detect_anomalies(volumes, method='zscore', threshold=2.5)
        
        anomalies = []
        for idx in anomaly_result['anomaly_indices']:
            if idx < len(transfer_data):
                transfer = transfer_data[idx]
                anomalies.append({
                    'timestamp': transfer.get('timestamp'),
                    'source': transfer.get('source'),
                    'destination': transfer.get('destination'),
                    'volume': volumes[idx],
                    'volume_gb': volumes[idx] / (1024**3),
                    'severity': 'critical' if volumes[idx] > 10*(1024**3) else 'high'
                })
        
        return {
            'total_transfers': len(transfer_data),
            'anomalies_detected': len(anomalies),
            'total_volume': sum(volumes),
            'avg_volume': statistics.mean(volumes) if volumes else 0,
            'anomalies': anomalies
        }
    
    async def detect_process_anomalies(self, process_data: List[Dict]) -> Dict[str, Any]:
        """Detect anomalous process behavior"""
        anomalies = []
        
        # Analyze CPU usage
        cpu_usage = [p.get('cpu', 0) for p in process_data]
        cpu_anomalies = await self.detect_anomalies(cpu_usage, method='zscore')
        
        # Analyze memory usage
        memory_usage = [p.get('memory', 0) for p in process_data]
        memory_anomalies = await self.detect_anomalies(memory_usage, method='iqr')
        
        # Check for suspicious processes
        for idx, process in enumerate(process_data):
            if idx in cpu_anomalies['anomaly_indices']:
                anomalies.append({
                    'type': 'high_cpu',
                    'process': process.get('name'),
                    'pid': process.get('pid'),
                    'cpu': cpu_usage[idx],
                    'severity': 'high'
                })
            
            if idx in memory_anomalies['anomaly_indices']:
                anomalies.append({
                    'type': 'high_memory',
                    'process': process.get('name'),
                    'pid': process.get('pid'),
                    'memory': memory_usage[idx],
                    'severity': 'medium'
                })
            
            # Check for suspicious process names
            if self._is_suspicious_process(process.get('name', '')):
                anomalies.append({
                    'type': 'suspicious_process',
                    'process': process.get('name'),
                    'pid': process.get('pid'),
                    'severity': 'critical'
                })
        
        return {
            'total_processes': len(process_data),
            'anomalies_detected': len(anomalies),
            'anomalies': anomalies
        }
    
    async def detect_dns_anomalies(self, dns_queries: List[Dict]) -> Dict[str, Any]:
        """Detect anomalous DNS queries"""
        anomalies = []
        
        # Check for DGA domains
        for query in dns_queries:
            domain = query.get('domain', '')
            if self._is_dga_domain(domain):
                anomalies.append({
                    'type': 'dga_domain',
                    'domain': domain,
                    'timestamp': query.get('timestamp'),
                    'severity': 'high'
                })
            
            # Check for excessive subdomain levels
            if domain.count('.') > 5:
                anomalies.append({
                    'type': 'excessive_subdomains',
                    'domain': domain,
                    'timestamp': query.get('timestamp'),
                    'severity': 'medium'
                })
            
            # Check for long domain names
            if len(domain) > 50:
                anomalies.append({
                    'type': 'long_domain',
                    'domain': domain,
                    'timestamp': query.get('timestamp'),
                    'severity': 'medium'
                })
        
        # Analyze query frequency
        query_counts = {}
        for query in dns_queries:
            domain = query.get('domain')
            query_counts[domain] = query_counts.get(domain, 0) + 1
        
        # Detect high-frequency queries
        for domain, count in query_counts.items():
            if count > 100:
                anomalies.append({
                    'type': 'high_frequency_queries',
                    'domain': domain,
                    'count': count,
                    'severity': 'medium'
                })
        
        return {
            'total_queries': len(dns_queries),
            'unique_domains': len(query_counts),
            'anomalies_detected': len(anomalies),
            'anomalies': anomalies
        }
    
    async def set_threshold(self, metric: str, threshold: float) -> Dict[str, Any]:
        """Set custom threshold for metric"""
        self.thresholds[metric] = threshold
        return {
            'metric': metric,
            'threshold': threshold,
            'status': 'set'
        }
    
    async def get_baseline_statistics(self, data: List[float]) -> Dict[str, Any]:
        """Calculate baseline statistics"""
        if not data:
            return {'error': 'No data provided'}
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        return {
            'count': n,
            'mean': statistics.mean(data),
            'median': statistics.median(data),
            'mode': statistics.mode(data) if n > 1 else data[0],
            'std_dev': statistics.stdev(data) if n > 1 else 0,
            'variance': statistics.variance(data) if n > 1 else 0,
            'min': min(data),
            'max': max(data),
            'range': max(data) - min(data),
            'q1': sorted_data[n//4],
            'q3': sorted_data[3*n//4],
            'iqr': sorted_data[3*n//4] - sorted_data[n//4]
        }
    
    async def _zscore_detection(self, data: List[float], threshold: float) -> Dict[str, Any]:
        """Z-score based anomaly detection"""
        if len(data) < 2:
            return {'anomaly_indices': [], 'method': 'zscore'}
        
        mean = statistics.mean(data)
        std_dev = statistics.stdev(data)
        
        if std_dev == 0:
            return {'anomaly_indices': [], 'method': 'zscore'}
        
        anomaly_indices = []
        for i, value in enumerate(data):
            zscore = abs((value - mean) / std_dev)
            if zscore > threshold:
                anomaly_indices.append(i)
        
        return {
            'method': 'zscore',
            'threshold': threshold,
            'anomaly_indices': anomaly_indices,
            'anomaly_count': len(anomaly_indices),
            'expected_range': {
                'lower': mean - (threshold * std_dev),
                'upper': mean + (threshold * std_dev)
            }
        }
    
    async def _iqr_detection(self, data: List[float]) -> Dict[str, Any]:
        """IQR (Interquartile Range) based anomaly detection"""
        if len(data) < 4:
            return {'anomaly_indices': [], 'method': 'iqr'}
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        q1 = sorted_data[n//4]
        q3 = sorted_data[3*n//4]
        iqr = q3 - q1
        
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        
        anomaly_indices = []
        for i, value in enumerate(data):
            if value < lower_bound or value > upper_bound:
                anomaly_indices.append(i)
        
        return {
            'method': 'iqr',
            'anomaly_indices': anomaly_indices,
            'anomaly_count': len(anomaly_indices),
            'expected_range': {
                'lower': lower_bound,
                'upper': upper_bound
            },
            'iqr': iqr
        }
    
    async def _moving_average_detection(self, data: List[float], window: int) -> Dict[str, Any]:
        """Moving average based anomaly detection"""
        if len(data) < window:
            return {'anomaly_indices': [], 'method': 'moving_average'}
        
        anomaly_indices = []
        
        for i in range(window, len(data)):
            window_data = data[i-window:i]
            avg = statistics.mean(window_data)
            std = statistics.stdev(window_data) if len(window_data) > 1 else 0
            
            if std > 0:
                deviation = abs(data[i] - avg) / std
                if deviation > 2.5:
                    anomaly_indices.append(i)
        
        return {
            'method': 'moving_average',
            'window_size': window,
            'anomaly_indices': anomaly_indices,
            'anomaly_count': len(anomaly_indices)
        }
    
    async def _exponential_smoothing_detection(self, data: List[float], alpha: float) -> Dict[str, Any]:
        """Exponential smoothing based anomaly detection"""
        if len(data) < 2:
            return {'anomaly_indices': [], 'method': 'exponential_smoothing'}
        
        smoothed = [data[0]]
        for i in range(1, len(data)):
            smoothed.append(alpha * data[i] + (1 - alpha) * smoothed[i-1])
        
        # Calculate residuals
        residuals = [abs(data[i] - smoothed[i]) for i in range(len(data))]
        
        # Detect anomalies based on residuals
        if len(residuals) > 1:
            threshold = statistics.mean(residuals) + 2 * statistics.stdev(residuals)
            anomaly_indices = [i for i, r in enumerate(residuals) if r > threshold]
        else:
            anomaly_indices = []
        
        return {
            'method': 'exponential_smoothing',
            'alpha': alpha,
            'anomaly_indices': anomaly_indices,
            'anomaly_count': len(anomaly_indices)
        }
    
    def _is_suspicious_process(self, process_name: str) -> bool:
        """Check if process name is suspicious"""
        suspicious_keywords = ['mimikatz', 'psexec', 'netcat', 'nc.exe', 'powershell', 'cmd.exe']
        return any(keyword in process_name.lower() for keyword in suspicious_keywords)
    
    def _is_dga_domain(self, domain: str) -> bool:
        """Check if domain looks like DGA (Domain Generation Algorithm)"""
        if not domain:
            return False
        
        # Simple heuristic: high consonant ratio
        consonants = 'bcdfghjklmnpqrstvwxyz'
        domain_lower = domain.lower().split('.')[0]  # Get subdomain
        
        if len(domain_lower) < 8:
            return False
        
        consonant_count = sum(1 for c in domain_lower if c in consonants)
        ratio = consonant_count / len(domain_lower)
        
        return ratio > 0.7

# Singleton
anomaly_detector = AnomalyDetector()
