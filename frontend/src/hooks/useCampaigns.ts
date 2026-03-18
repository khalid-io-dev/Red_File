import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface Campaign {
  id: number;
  name: string;
  description?: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'paused';
  targets: string[];
  progress: number;
  total_targets: number;
  completed_targets: number;
  findings_count: number;
  credentials_count: number;
  created_at: string;
  updated_at: string;
}

interface CreateCampaignData {
  name: string;
  description?: string;
  targets: string[];
  scan_type: string;
  tools?: string[];
}

export const useCampaigns = (params?: { skip?: number; limit?: number; status?: string }) => {
  return useQuery({
    queryKey: ['campaigns', params],
    queryFn: () => apiClient.get<Campaign[]>('/campaign/', params),
  });
};

export const useCampaign = (id: number) => {
  return useQuery({
    queryKey: ['campaigns', id],
    queryFn: () => apiClient.get<Campaign>(`/campaign/${id}`),
    enabled: !!id,
  });
};

export const useCreateCampaign = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateCampaignData) => apiClient.post<Campaign>('/campaign/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] });
    },
  });
};

export const useStartCampaign = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.post(`/campaign/${id}/start`),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['campaigns', id] });
      queryClient.invalidateQueries({ queryKey: ['campaigns'] });
    },
  });
};

export const useStopCampaign = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.post(`/campaign/${id}/stop`),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['campaigns', id] });
      queryClient.invalidateQueries({ queryKey: ['campaigns'] });
    },
  });
};

export const useDeleteCampaign = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.delete(`/campaign/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] });
    },
  });
};

export const useCampaignFindings = (id: number) => {
  return useQuery({
    queryKey: ['campaigns', id, 'findings'],
    queryFn: () => apiClient.get(`/campaign/${id}/findings`),
    enabled: !!id,
  });
};

export const useCampaignCredentials = (id: number) => {
  return useQuery({
    queryKey: ['campaigns', id, 'credentials'],
    queryFn: () => apiClient.get(`/campaign/${id}/credentials`),
    enabled: !!id,
  });
};
