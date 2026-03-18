import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

// Vulnerabilities
export const useVulnerabilities = (filters?: { severity?: string; status?: string }) => {
  return useQuery({
    queryKey: ['vulnerabilities', filters],
    queryFn: () => apiClient.get('/vulnerabilities/', filters),
  });
};

export const useCreateVulnerability = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: any) => apiClient.post('/vulnerabilities/', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vulnerabilities'] });
    },
  });
};

export const useCreateRemediationPlan = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ vulnId, plan }: { vulnId: string; plan: any }) =>
      apiClient.post(`/vulnerabilities/${vulnId}/remediation`, plan),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vulnerabilities'] });
    },
  });
};

export const useVulnerabilityTrends = () => {
  return useQuery({
    queryKey: ['vulnerabilities', 'trends'],
    queryFn: () => apiClient.get('/vulnerabilities/trends'),
  });
};

// ML Detection
export const useDetectMalware = () => {
  return useMutation({
    mutationFn: (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      return apiClient.upload('/ml/detect/malware', formData);
    },
  });
};

export const useDetectPhishing = () => {
  return useMutation({
    mutationFn: (email: { subject: string; body: string; sender: string }) =>
      apiClient.post('/ml/detect/phishing', email),
  });
};

export const useDetectIntrusion = () => {
  return useMutation({
    mutationFn: (traffic: { packets: any[]; metadata: any }) =>
      apiClient.post('/ml/detect/intrusion', traffic),
  });
};

export const useMLModels = () => {
  return useQuery({
    queryKey: ['ml', 'models'],
    queryFn: () => apiClient.get('/ml/models'),
  });
};

// IOC Analysis
export const useAnalyzeIP = () => {
  return useMutation({
    mutationFn: (ip: string) => apiClient.post('/ioc/analyze/ip', { ip }),
  });
};

export const useAnalyzeDomain = () => {
  return useMutation({
    mutationFn: (domain: string) => apiClient.post('/ioc/analyze/domain', { domain }),
  });
};

export const useAnalyzeHash = () => {
  return useMutation({
    mutationFn: (hash: string) => apiClient.post('/ioc/analyze/hash', { hash }),
  });
};

export const useAnalyzeURL = () => {
  return useMutation({
    mutationFn: (url: string) => apiClient.post('/ioc/analyze/url', { url }),
  });
};

export const useBatchAnalyzeIOC = () => {
  return useMutation({
    mutationFn: (iocs: any[]) => apiClient.post('/ioc/batch', { iocs }),
  });
};
