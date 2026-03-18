import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface Scan {
  id: number;
  target: string;
  scan_type: string;
  status: string;
  progress: number;
  created_at: string;
  updated_at: string;
  findings_count?: number;
  credentials_count?: number;
}

interface CreateScanData {
  target: string;
  scan_type: string;
  tools?: string[];
}

export const useScans = (params?: { skip?: number; limit?: number; status?: string }) => {
  return useQuery({
    queryKey: ['scans', params],
    queryFn: () => apiClient.get<Scan[]>('/scans/', params),
  });
};

export const useScan = (id: number) => {
  return useQuery({
    queryKey: ['scans', id],
    queryFn: () => apiClient.get<Scan>(`/scans/${id}`),
    enabled: !!id,
  });
};

export const useCreateScan = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateScanData) => apiClient.post<Scan>('/scans/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scans'] });
    },
  });
};

export const useDeleteScan = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.delete(`/scans/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scans'] });
    },
  });
};

export const useStopScan = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.post(`/scans/${id}/stop`),
    onSuccess: (_, id) => {
      queryClient.invalidateQueries({ queryKey: ['scans', id] });
      queryClient.invalidateQueries({ queryKey: ['scans'] });
    },
  });
};
