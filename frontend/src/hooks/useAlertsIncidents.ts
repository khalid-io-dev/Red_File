import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

export const useAlerts = (filters?: { severity?: string; status?: string }) => {
  return useQuery({
    queryKey: ['alerts', filters],
    queryFn: () => apiClient.get('/alerts/', filters),
  });
};

export const useCreateAlert = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { title: string; severity: string; description: string; source: string }) =>
      apiClient.post('/alerts/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    },
  });
};

export const useAcknowledgeAlert = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (alertId: string) => apiClient.put(`/alerts/${alertId}/acknowledge`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    },
  });
};

export const useResolveAlert = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ alertId, resolution }: { alertId: string; resolution: string }) =>
      apiClient.put(`/alerts/${alertId}/resolve`, { resolution }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    },
  });
};

export const useAlertStatistics = () => {
  return useQuery({
    queryKey: ['alerts', 'statistics'],
    queryFn: () => apiClient.get('/alerts/statistics'),
  });
};

export const useIncidents = (filters?: { status?: string; severity?: string }) => {
  return useQuery({
    queryKey: ['incidents', filters],
    queryFn: () => apiClient.get('/incidents/', filters),
  });
};

export const useCreateIncident = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { title: string; severity: string; description: string; affected_systems: string[] }) =>
      apiClient.post('/incidents/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['incidents'] });
    },
  });
};

export const useIncidentTimeline = (incidentId: string) => {
  return useQuery({
    queryKey: ['incidents', incidentId, 'timeline'],
    queryFn: () => apiClient.get(`/incidents/${incidentId}/timeline`),
    enabled: !!incidentId,
  });
};

export const useAddIncidentAction = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ incidentId, action }: { incidentId: string; action: any }) =>
      apiClient.post(`/incidents/${incidentId}/actions`, action),
    onSuccess: (_, { incidentId }) => {
      queryClient.invalidateQueries({ queryKey: ['incidents', incidentId] });
    },
  });
};
