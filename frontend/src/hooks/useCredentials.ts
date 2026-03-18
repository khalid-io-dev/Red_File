import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface Credential {
  id: number;
  scan_id?: number;
  campaign_id?: number;
  username: string;
  password: string;
  service: string;
  host: string;
  port?: number;
  validated: boolean;
  created_at: string;
}

export const useCredentials = (params?: { skip?: number; limit?: number; validated?: boolean }) => {
  return useQuery({
    queryKey: ['credentials', params],
    queryFn: () => apiClient.get<Credential[]>('/credentials/', params),
  });
};

export const useValidateCredential = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.post(`/credentials/${id}/validate`),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['credentials'] });
    },
  });
};

export const useDeleteCredential = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.delete(`/credentials/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['credentials'] });
    },
  });
};
