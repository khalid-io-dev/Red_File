import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

// ========== SIEM Integrator ==========

export const useConnectSplunk = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (config: { host: string; port: number; username: string; password: string }) =>
      apiClient.post('/siem/connect/splunk', config),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['siem', 'connections'] });
    },
  });
};

export const useConnectElastic = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (config: { hosts: string[]; username?: string; password?: string }) =>
      apiClient.post('/siem/connect/elastic', config),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['siem', 'connections'] });
    },
  });
};

export const useSIEMConnections = () => {
  return useQuery({
    queryKey: ['siem', 'connections'],
    queryFn: () => apiClient.get('/siem/connections'),
  });
};

export const useExecuteSIEMQuery = () => {
  return useMutation({
    mutationFn: (data: { siem_type: string; query: string; time_range?: string; limit?: number }) =>
      apiClient.post('/siem/query', data),
  });
};

export const useExecuteBatchQueries = () => {
  return useMutation({
    mutationFn: (queries: any[]) => apiClient.post('/siem/query/batch', queries),
  });
};

export const useSIEMDashboards = (siemType?: string) => {
  return useQuery({
    queryKey: ['siem', 'dashboards', siemType],
    queryFn: () => apiClient.get('/siem/dashboards', siemType ? { siem_type: siemType } : undefined),
  });
};

export const useCreateSIEMDashboard = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { name: string; siem_type: string; widgets: any[]; refresh_interval?: number }) =>
      apiClient.post('/siem/dashboards', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['siem', 'dashboards'] });
    },
  });
};

export const useSIEMActiveAlerts = (siemType?: string, severity?: string) => {
  return useQuery({
    queryKey: ['siem', 'alerts', siemType, severity],
    queryFn: () => apiClient.get('/siem/alerts/active', { siem_type: siemType, severity }),
  });
};

export const useSIEMStatistics = (siemType?: string) => {
  return useQuery({
    queryKey: ['siem', 'statistics', siemType],
    queryFn: () => apiClient.get('/siem/statistics', siemType ? { siem_type: siemType } : undefined),
  });
};

// ========== Multi-Agent Orchestrator ==========

export const useCreateMission = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: {
      name: string;
      target: string;
      objective: string;
      agents: string[];
      strategy?: string;
      ai_coordination?: boolean;
    }) => apiClient.post('/multi-agent/mission', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['missions'] });
    },
  });
};

export const useMissions = (status?: string) => {
  return useQuery({
    queryKey: ['missions', status],
    queryFn: () => apiClient.get('/multi-agent/missions', status ? { status } : undefined),
  });
};

export const useMissionStatus = (missionId: string) => {
  return useQuery({
    queryKey: ['missions', missionId, 'status'],
    queryFn: () => apiClient.get(`/multi-agent/mission/${missionId}/status`),
    enabled: !!missionId,
    refetchInterval: 3000, // Poll every 3 seconds
  });
};

export const usePauseMission = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (missionId: string) => apiClient.post(`/multi-agent/mission/${missionId}/pause`),
    onSuccess: (_, missionId) => {
      queryClient.invalidateQueries({ queryKey: ['missions', missionId] });
    },
  });
};

export const useResumeMission = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (missionId: string) => apiClient.post(`/multi-agent/mission/${missionId}/resume`),
    onSuccess: (_, missionId) => {
      queryClient.invalidateQueries({ queryKey: ['missions', missionId] });
    },
  });
};

export const useCoordinateAgents = () => {
  return useMutation({
    mutationFn: (data: { mission_id: string; problem: string; agents: string[]; context?: any }) =>
      apiClient.post('/multi-agent/coordinate', data),
  });
};

export const useAgentsStatus = () => {
  return useQuery({
    queryKey: ['agents', 'status'],
    queryFn: () => apiClient.get('/multi-agent/agents/status'),
    refetchInterval: 5000,
  });
};

export const useMissionReport = (missionId: string, format: string = 'json') => {
  return useQuery({
    queryKey: ['missions', missionId, 'report', format],
    queryFn: () => apiClient.get(`/multi-agent/mission/${missionId}/report`, { format }),
    enabled: !!missionId,
  });
};

// ========== Exploit Dev Framework ==========

export const useGenerateExploit = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: {
      vulnerability_description: string;
      target_platform: string;
      exploit_type: string;
      target_architecture?: string;
      payload_type?: string;
      ai_model?: string;
      evasion_level?: number;
    }) => apiClient.post('/exploit-dev/generate', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['exploits'] });
    },
  });
};

export const useReviewExploit = () => {
  return useMutation({
    mutationFn: (data: { exploit_code: string; review_aspects?: string[] }) =>
      apiClient.post('/exploit-dev/review', data),
  });
};

export const useAddEvasion = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { exploit_id: string; techniques: string[]; intensity?: number }) =>
      apiClient.post('/exploit-dev/add-evasion', data),
    onSuccess: (_, { exploit_id }) => {
      queryClient.invalidateQueries({ queryKey: ['exploits', exploit_id] });
    },
  });
};

export const useTestExploit = () => {
  return useMutation({
    mutationFn: (data: { exploit_id: string; test_environment: string; target_config: any }) =>
      apiClient.post('/exploit-dev/test', data),
  });
};

export const useTestResults = (testId: string) => {
  return useQuery({
    queryKey: ['exploit-tests', testId],
    queryFn: () => apiClient.get(`/exploit-dev/test/${testId}`),
    enabled: !!testId,
    refetchInterval: 2000,
  });
};

export const useChainExploits = () => {
  return useMutation({
    mutationFn: (data: { exploit_ids: string[]; chain_strategy?: string }) =>
      apiClient.post('/exploit-dev/chain', data),
  });
};

export const useExploitLibrary = (filters?: { platform?: string; exploit_type?: string }) => {
  return useQuery({
    queryKey: ['exploits', 'library', filters],
    queryFn: () => apiClient.get('/exploit-dev/library', filters),
  });
};

export const useExploit = (exploitId: string, includeCode: boolean = true) => {
  return useQuery({
    queryKey: ['exploits', exploitId, includeCode],
    queryFn: () => apiClient.get(`/exploit-dev/${exploitId}`, { include_code: includeCode }),
    enabled: !!exploitId,
  });
};

export const useDeleteExploit = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (exploitId: string) => apiClient.delete(`/exploit-dev/${exploitId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['exploits'] });
    },
  });
};

export const useWeaponizeExploit = () => {
  return useMutation({
    mutationFn: ({ exploitId, deliveryMethod }: { exploitId: string; deliveryMethod: string }) =>
      apiClient.post(`/exploit-dev/${exploitId}/weaponize`, null, { params: { delivery_method: deliveryMethod } }),
  });
};
