import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface AttackChain {
  id: number;
  name: string;
  description: string;
  tactics: string[];
  techniques: string[];
  status: string;
  created_at: string;
}

interface CreateAttackChainData {
  name: string;
  description: string;
  tactics: string[];
  techniques: string[];
}

export const useAttackChains = (params?: { skip?: number; limit?: number }) => {
  return useQuery({
    queryKey: ['attack-chains', params],
    queryFn: () => apiClient.get<AttackChain[]>('/attack/chains', params),
  });
};

export const useAttackChain = (id: number) => {
  return useQuery({
    queryKey: ['attack-chains', id],
    queryFn: () => apiClient.get<AttackChain>(`/attack/chains/${id}`),
    enabled: !!id,
  });
};

export const useCreateAttackChain = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateAttackChainData) => apiClient.post<AttackChain>('/attack/chains', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['attack-chains'] });
    },
  });
};

export const useMitreTechniques = () => {
  return useQuery({
    queryKey: ['mitre', 'techniques'],
    queryFn: () => apiClient.get('/attack/mitre/techniques'),
  });
};

export const useMitreTactics = () => {
  return useQuery({
    queryKey: ['mitre', 'tactics'],
    queryFn: () => apiClient.get('/attack/mitre/tactics'),
  });
};
