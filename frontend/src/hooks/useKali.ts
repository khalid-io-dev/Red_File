import { useMutation, useQuery } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

export const useNmap = () => {
  return useMutation({
    mutationFn: (data: { target: string; scan_type?: string; ports?: string }) =>
      apiClient.post('/kali/nmap', data),
  });
};

export const useSQLMap = () => {
  return useMutation({
    mutationFn: (data: { url: string; data?: string; cookie?: string }) =>
      apiClient.post('/kali/sqlmap', data),
  });
};

export const useNikto = () => {
  return useMutation({
    mutationFn: (target: string) => apiClient.post('/kali/nikto', { target }),
  });
};

export const useGobuster = () => {
  return useMutation({
    mutationFn: (data: { url: string; wordlist?: string }) =>
      apiClient.post('/kali/gobuster', data),
  });
};

export const useHydra = () => {
  return useMutation({
    mutationFn: (data: { target: string; service: string; username?: string; password_list?: string }) =>
      apiClient.post('/kali/hydra', data),
  });
};

export const useTaskStatus = (taskId: string) => {
  return useQuery({
    queryKey: ['kali-task', taskId],
    queryFn: () => apiClient.get(`/kali/status/${taskId}`),
    enabled: !!taskId,
    refetchInterval: 2000,
  });
};
