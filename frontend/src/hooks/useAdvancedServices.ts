import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

// Behavior Analytics
export const useAnalyzeUserBehavior = () => {
  return useMutation({
    mutationFn: (data: { user_id: string; activities: any[] }) =>
      apiClient.post('/behavior/analyze/user', data),
  });
};

export const useAnalyzeEntityBehavior = () => {
  return useMutation({
    mutationFn: (data: { entity_id: string; entity_type: string; activities: any[] }) =>
      apiClient.post('/behavior/analyze/entity', data),
  });
};

export const useBehaviorBaselines = () => {
  return useQuery({
    queryKey: ['behavior', 'baselines'],
    queryFn: () => apiClient.get('/behavior/baselines'),
  });
};

export const useBehaviorAnomalies = () => {
  return useQuery({
    queryKey: ['behavior', 'anomalies'],
    queryFn: () => apiClient.get('/behavior/anomalies'),
  });
};

// Anomaly Detection
export const useDetectTrafficAnomalies = () => {
  return useMutation({
    mutationFn: (data: { data_points: number[]; timestamps: string[] }) =>
      apiClient.post('/anomaly/detect/traffic', data),
  });
};

export const useDetectLoginAnomalies = () => {
  return useMutation({
    mutationFn: (data: { user_id: string; login_times: string[]; ip_addresses: string[] }) =>
      apiClient.post('/anomaly/detect/login', data),
  });
};

export const useAnomalyStatistics = () => {
  return useQuery({
    queryKey: ['anomaly', 'statistics'],
    queryFn: () => apiClient.get('/anomaly/statistics'),
  });
};

// Threat Prediction
export const usePredictAttackLikelihood = () => {
  return useMutation({
    mutationFn: (data: { target: string; threat_indicators: string[] }) =>
      apiClient.post('/prediction/attack-likelihood', data),
  });
};

export const useForecastThreatTrends = () => {
  return useMutation({
    mutationFn: (days: number = 30) =>
      apiClient.post('/prediction/threat-trends', null, { params: { days } }),
  });
};

export const usePredictionForecasts = () => {
  return useQuery({
    queryKey: ['prediction', 'forecasts'],
    queryFn: () => apiClient.get('/prediction/forecasts'),
  });
};

// Compliance
export const useComplianceFrameworks = () => {
  return useQuery({
    queryKey: ['compliance', 'frameworks'],
    queryFn: () => apiClient.get('/compliance-checker/frameworks'),
  });
};

export const useCheckCompliance = () => {
  return useMutation({
    mutationFn: (framework: string) =>
      apiClient.post(`/compliance-checker/check/${framework}`),
  });
};

export const useComplianceGaps = (framework?: string) => {
  return useQuery({
    queryKey: ['compliance', 'gaps', framework],
    queryFn: () => apiClient.get('/compliance-checker/gaps', framework ? { framework } : undefined),
  });
};

export const useAuditReadiness = (framework: string) => {
  return useQuery({
    queryKey: ['compliance', 'audit-readiness', framework],
    queryFn: () => apiClient.get('/compliance-checker/audit-readiness', { framework }),
    enabled: !!framework,
  });
};

// Network Topology
export const useDiscoverTopology = () => {
  return useMutation({
    mutationFn: (network_range: string) =>
      apiClient.post('/topology/discover', { network_range }),
  });
};

export const useTopologyGraph = (scanId?: string) => {
  return useQuery({
    queryKey: ['topology', 'graph', scanId],
    queryFn: () => apiClient.get('/topology/graph', scanId ? { scan_id: scanId } : undefined),
  });
};

export const useTopologySubnets = () => {
  return useQuery({
    queryKey: ['topology', 'subnets'],
    queryFn: () => apiClient.get('/topology/subnets'),
  });
};

// Log Analysis
export const useUploadLogs = () => {
  return useMutation({
    mutationFn: ({ file, logType }: { file: File; logType: string }) => {
      const formData = new FormData();
      formData.append('file', file);
      return apiClient.upload(`/logs/upload?log_type=${logType}`, formData);
    },
  });
};

export const useAnalyzeLogs = () => {
  return useMutation({
    mutationFn: (data: { log_content: string; log_type: string }) =>
      apiClient.post('/logs/analyze', data),
  });
};

export const useLogThreats = () => {
  return useQuery({
    queryKey: ['logs', 'threats'],
    queryFn: () => apiClient.get('/logs/threats'),
  });
};

export const useLogStatistics = () => {
  return useQuery({
    queryKey: ['logs', 'statistics'],
    queryFn: () => apiClient.get('/logs/statistics'),
  });
};
