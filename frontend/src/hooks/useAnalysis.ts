import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface Analysis {
  id: number;
  file_name: string;
  file_hash: string;
  analysis_type: 'static' | 'dynamic' | 'behavioral';
  status: string;
  results: any;
  created_at: string;
}

interface AnalysisResult {
  malicious: boolean;
  score: number;
  signatures: string[];
  indicators: any[];
}

export const useAnalyses = (params?: { skip?: number; limit?: number }) => {
  return useQuery({
    queryKey: ['analyses', params],
    queryFn: () => apiClient.get<Analysis[]>('/analysis/', params),
  });
};

export const useAnalysis = (id: number) => {
  return useQuery({
    queryKey: ['analyses', id],
    queryFn: () => apiClient.get<Analysis>(`/analysis/${id}`),
    enabled: !!id,
  });
};

export const useUploadForAnalysis = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ file, analysisType }: { file: File; analysisType: string }) => {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('analysis_type', analysisType);
      return apiClient.upload<Analysis>('/analysis/upload', formData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['analyses'] });
    },
  });
};

export const useAnalyzeHash = () => {
  return useMutation({
    mutationFn: (hash: string) => apiClient.post<AnalysisResult>('/analysis/hash', { hash }),
  });
};
