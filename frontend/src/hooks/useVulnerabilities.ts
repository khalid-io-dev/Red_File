import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface Vulnerability {
  id: number;
  cve_id: string;
  title: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low' | 'Info';
  cvss_score: number;
  description: string;
  affected_systems: string[];
  status: 'open' | 'in_progress' | 'resolved' | 'false_positive';
  category: string;
  discovered_at: string;
}

interface CVEDetail {
  cve_id: string;
  cvss_score: number;
  severity: string;
  description: string;
  references: string[];
  affected_products: string[];
  published_date: string;
}

export const useVulnerabilities = (params?: { 
  severity?: string; 
  status?: string;
  category?: string;
  skip?: number;
  limit?: number;
}) => {
  return useQuery({
    queryKey: ['vulnerabilities', params],
    queryFn: () => apiClient.get<Vulnerability[]>('/findings/', params),
  });
};

export const useVulnerability = (id: number) => {
  return useQuery({
    queryKey: ['vulnerabilities', id],
    queryFn: () => apiClient.get<Vulnerability>(`/findings/${id}`),
    enabled: !!id,
  });
};

export const useCVESearch = (cveId: string) => {
  return useQuery({
    queryKey: ['cve', cveId],
    queryFn: () => apiClient.get<CVEDetail>(`/vulnerabilities/cve/${cveId}`),
    enabled: !!cveId && cveId.length > 0,
  });
};

export const useUpdateVulnerability = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Vulnerability> }) =>
      apiClient.patch(`/findings/${id}`, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['vulnerabilities', id] });
      queryClient.invalidateQueries({ queryKey: ['vulnerabilities'] });
    },
  });
};

export const useVulnerabilityStats = () => {
  return useQuery({
    queryKey: ['vulnerabilities', 'stats'],
    queryFn: () => apiClient.get('/findings/stats/summary'),
  });
};
