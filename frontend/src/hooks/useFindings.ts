import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface Finding {
  id: number;
  scan_id: number;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  status: 'open' | 'in_progress' | 'resolved' | 'false_positive';
  cvss_score?: number;
  cve_id?: string;
  evidence?: string;
  remediation?: string;
  created_at: string;
  updated_at: string;
}

interface FindingsParams {
  skip?: number;
  limit?: number;
  severity?: string;
  status?: string;
  scan_id?: number;
}

export const useFindings = (params?: FindingsParams) => {
  return useQuery({
    queryKey: ['findings', params],
    queryFn: () => apiClient.get<Finding[]>('/findings/', params),
  });
};

export const useFinding = (id: number) => {
  return useQuery({
    queryKey: ['findings', id],
    queryFn: () => apiClient.get<Finding>(`/findings/${id}`),
    enabled: !!id,
  });
};

export const useUpdateFinding = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Finding> }) =>
      apiClient.put<Finding>(`/findings/${id}`, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['findings', id] });
      queryClient.invalidateQueries({ queryKey: ['findings'] });
    },
  });
};

export const useDeleteFinding = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.delete(`/findings/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['findings'] });
    },
  });
};

export const useBulkUpdateFindings = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ ids, data }: { ids: number[]; data: Partial<Finding> }) =>
      apiClient.post('/findings/bulk-update', { ids, ...data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['findings'] });
    },
  });
};
