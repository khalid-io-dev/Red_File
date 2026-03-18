import { useQuery, useMutation } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

export const useMITRETactics = () => {
  return useQuery({
    queryKey: ['mitre', 'tactics'],
    queryFn: () => apiClient.get('/mitre/tactics'),
  });
};

export const useMITRETechniques = (tacticId?: string) => {
  return useQuery({
    queryKey: ['mitre', 'techniques', tacticId],
    queryFn: () => apiClient.get('/mitre/techniques', tacticId ? { tactic_id: tacticId } : undefined),
  });
};

export const useMITREMatrix = () => {
  return useQuery({
    queryKey: ['mitre', 'matrix'],
    queryFn: () => apiClient.get('/mitre/matrix'),
  });
};

export const useMapFinding = () => {
  return useMutation({
    mutationFn: (data: { finding_description: string; tool_name: string }) =>
      apiClient.post('/mitre/map-finding', data),
  });
};

export const useMITRECoverage = () => {
  return useQuery({
    queryKey: ['mitre', 'coverage'],
    queryFn: () => apiClient.get('/mitre/coverage'),
  });
};
