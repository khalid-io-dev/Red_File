import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface Asset {
  id: string;
  name: string;
  type: string;
  ip_address?: string;
  hostname?: string;
  os?: string;
  location?: string;
  owner?: string;
  criticality: string;
  status: string;
  created_at: string;
  updated_at: string;
}

interface CreateAssetData {
  name: string;
  type: string;
  ip_address?: string;
  hostname?: string;
  os?: string;
  location?: string;
  owner?: string;
  criticality?: string;
  status?: string;
}

export const useAssets = (filters?: { type?: string; criticality?: string; status?: string }) => {
  return useQuery({
    queryKey: ['assets', filters],
    queryFn: () => apiClient.get<Asset[]>('/assets/', filters),
  });
};

export const useCreateAsset = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateAssetData) => apiClient.post<Asset>('/assets/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets'] });
    },
  });
};

export const useUpdateAsset = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<CreateAssetData> }) =>
      apiClient.put<Asset>(`/assets/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets'] });
    },
  });
};

export const useDeleteAsset = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => apiClient.delete(`/assets/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets'] });
    },
  });
};

export const useDiscoverAssets = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (networkRange: string) =>
      apiClient.post('/assets/discover', null, { params: { network_range: networkRange } }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets'] });
    },
  });
};

export const useAssetHealth = (assetId: string) => {
  return useQuery({
    queryKey: ['assets', assetId, 'health'],
    queryFn: () => apiClient.get(`/assets/${assetId}/health`),
    enabled: !!assetId,
  });
};

export const useAssetRisk = (assetId: string) => {
  return useQuery({
    queryKey: ['assets', assetId, 'risk'],
    queryFn: () => apiClient.get(`/assets/${assetId}/risk`),
    enabled: !!assetId,
  });
};

export const useAssetDependencies = (assetId: string) => {
  return useQuery({
    queryKey: ['assets', assetId, 'dependencies'],
    queryFn: () => apiClient.get(`/assets/${assetId}/dependencies`),
    enabled: !!assetId,
  });
};

export const useAssetTimeline = (assetId: string) => {
  return useQuery({
    queryKey: ['assets', assetId, 'timeline'],
    queryFn: () => apiClient.get(`/assets/${assetId}/timeline`),
    enabled: !!assetId,
  });
};

export const useScanAsset = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (assetId: string) => apiClient.post(`/assets/${assetId}/scan`),
    onSuccess: (_, assetId) => {
      queryClient.invalidateQueries({ queryKey: ['assets', assetId] });
    },
  });
};

export const useAssetStatistics = () => {
  return useQuery({
    queryKey: ['assets', 'statistics'],
    queryFn: () => apiClient.get('/assets/statistics'),
  });
};

export const useSearchAssets = (query: string) => {
  return useQuery({
    queryKey: ['assets', 'search', query],
    queryFn: () => apiClient.get('/assets/search', { q: query }),
    enabled: query.length > 0,
  });
};
