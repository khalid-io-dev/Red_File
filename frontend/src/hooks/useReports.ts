import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface Report {
  id: number;
  title: string;
  format: 'json' | 'markdown' | 'pdf' | 'html';
  status: string;
  created_at: string;
  file_path?: string;
}

interface GenerateReportData {
  title?: string;
  report_type?: string;
  format: 'json' | 'markdown' | 'pdf' | 'html';
  scan_id?: number;
  campaign_id?: number;
  scan_ids?: number[];
  campaign_ids?: number[];
  finding_ids?: number[];
  options?: Record<string, any>;
}

export const useReports = (params?: { skip?: number; limit?: number }) => {
  return useQuery({
    queryKey: ['reports', params],
    queryFn: () => apiClient.get<Report[]>('/reports/', params),
  });
};

export const useReport = (id: number) => {
  return useQuery({
    queryKey: ['reports', id],
    queryFn: () => apiClient.get<Report>(`/reports/${id}`),
    enabled: !!id,
  });
};

export const useGenerateReport = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: GenerateReportData) => apiClient.post<Report>('/reports/generate', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reports'] });
    },
  });
};

export const useDownloadReport = () => {
  return useMutation({
    mutationFn: async (id: number) => {
      const blob = await apiClient.download(`/reports/${id}/download`);
      return { id, blob };
    },
  });
};
