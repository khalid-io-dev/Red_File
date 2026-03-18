import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

// ========== Automated Penetration Testing ==========

export const useStartPentest = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: {
      name: string;
      target: string;
      scope: string[];
      methodology?: string;
      depth?: string;
      ai_planning?: boolean;
    }) => apiClient.post('/automated-pentest/start', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pentests'] });
    },
  });
};

export const usePentests = (status?: string) => {
  return useQuery({
    queryKey: ['pentests', status],
    queryFn: () => apiClient.get('/automated-pentest/tests', status ? { status } : undefined),
  });
};

export const usePentestStatus = (testId: string) => {
  return useQuery({
    queryKey: ['pentests', testId, 'status'],
    queryFn: () => apiClient.get(`/automated-pentest/test/${testId}/status`),
    enabled: !!testId,
    refetchInterval: 3000,
  });
};

export const usePentestReport = (testId: string, format: string = 'json') => {
  return useQuery({
    queryKey: ['pentests', testId, 'report', format],
    queryFn: () => apiClient.get(`/automated-pentest/test/${testId}/report`, { format }),
    enabled: !!testId,
  });
};

export const usePausePentest = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (testId: string) => apiClient.post(`/automated-pentest/test/${testId}/pause`),
    onSuccess: (_, testId) => {
      queryClient.invalidateQueries({ queryKey: ['pentests', testId] });
    },
  });
};

export const useResumePentest = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (testId: string) => apiClient.post(`/automated-pentest/test/${testId}/resume`),
    onSuccess: (_, testId) => {
      queryClient.invalidateQueries({ queryKey: ['pentests', testId] });
    },
  });
};

export const useStopPentest = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (testId: string) => apiClient.post(`/automated-pentest/test/${testId}/stop`),
    onSuccess: (_, testId) => {
      queryClient.invalidateQueries({ queryKey: ['pentests', testId] });
    },
  });
};

// ========== Continuous Security Monitoring ==========

export const useStartMonitoring = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: {
      name: string;
      targets: string[];
      monitor_types: string[];
      ai_detection?: boolean;
      auto_response?: boolean;
      alert_threshold?: string;
    }) => apiClient.post('/continuous-monitor/start', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['monitoring'] });
    },
  });
};

export const useStopMonitoring = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => apiClient.post('/continuous-monitor/stop'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['monitoring'] });
    },
  });
};

export const useMonitoringStatus = () => {
  return useQuery({
    queryKey: ['monitoring', 'status'],
    queryFn: () => apiClient.get('/continuous-monitor/status'),
    refetchInterval: 5000,
  });
};

export const useDetectedThreats = (severity?: string, limit: number = 100) => {
  return useQuery({
    queryKey: ['monitoring', 'threats', severity, limit],
    queryFn: () => apiClient.get('/continuous-monitor/threats', { severity, limit }),
    refetchInterval: 10000,
  });
};

export const useExecuteResponse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ threatId, action }: { threatId: string; action: { action_type: string; parameters: any } }) =>
      apiClient.post(`/continuous-monitor/response`, action, { params: { threat_id: threatId } }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['monitoring', 'threats'] });
    },
  });
};

export const useMonitoringBaselines = () => {
  return useQuery({
    queryKey: ['monitoring', 'baselines'],
    queryFn: () => apiClient.get('/continuous-monitor/baselines'),
  });
};

export const useUpdateBaselines = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => apiClient.post('/continuous-monitor/baselines/update'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['monitoring', 'baselines'] });
    },
  });
};

export const useAlertQueue = () => {
  return useQuery({
    queryKey: ['monitoring', 'alerts', 'queue'],
    queryFn: () => apiClient.get('/continuous-monitor/alerts/queue'),
    refetchInterval: 5000,
  });
};

export const useThreatHistory = (days: number = 7) => {
  return useQuery({
    queryKey: ['monitoring', 'history', days],
    queryFn: () => apiClient.get('/continuous-monitor/history', { days }),
  });
};
