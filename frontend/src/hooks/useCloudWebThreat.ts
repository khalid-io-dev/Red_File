import { useMutation, useQuery } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

export const useScanAWS = () => {
  return useMutation({
    mutationFn: (credentials: { access_key: string; secret_key: string; region?: string }) =>
      apiClient.post('/cloud/scan/aws', credentials),
  });
};

export const useScanAzure = () => {
  return useMutation({
    mutationFn: (credentials: { subscription_id: string; tenant_id: string; client_id: string; client_secret: string }) =>
      apiClient.post('/cloud/scan/azure', credentials),
  });
};

export const useScanGCP = () => {
  return useMutation({
    mutationFn: (credentials: { project_id: string; credentials_json: string }) =>
      apiClient.post('/cloud/scan/gcp', credentials),
  });
};

export const useCloudScans = () => {
  return useQuery({
    queryKey: ['cloud', 'scans'],
    queryFn: () => apiClient.get('/cloud/scans'),
  });
};

export const useCloudScan = (scanId: string) => {
  return useQuery({
    queryKey: ['cloud', 'scan', scanId],
    queryFn: () => apiClient.get(`/cloud/scan/${scanId}`),
    enabled: !!scanId,
    refetchInterval: 3000,
  });
};

export const useSQLInjectionScan = () => {
  return useMutation({
    mutationFn: (data: { url: string; method?: string; data?: string }) =>
      apiClient.post('/web/scan/sqli', data),
  });
};

export const useXSSScan = () => {
  return useMutation({
    mutationFn: (data: { url: string; forms?: boolean }) =>
      apiClient.post('/web/scan/xss', data),
  });
};

export const useCSRFScan = () => {
  return useMutation({
    mutationFn: (url: string) => apiClient.post('/web/scan/csrf', { url }),
  });
};

export const useFullWebScan = () => {
  return useMutation({
    mutationFn: (url: string) => apiClient.post('/web/scan/full', { url }),
  });
};

export const useThreatFeeds = () => {
  return useQuery({
    queryKey: ['threat-intel', 'feeds'],
    queryFn: () => apiClient.get('/threat-intel/feeds'),
  });
};

export const useThreatActors = () => {
  return useQuery({
    queryKey: ['threat-intel', 'actors'],
    queryFn: () => apiClient.get('/threat-intel/actors'),
  });
};

export const useCVEs = (limit: number = 20) => {
  return useQuery({
    queryKey: ['threat-intel', 'cves', limit],
    queryFn: () => apiClient.get('/threat-intel/cves', { limit }),
  });
};

export const useAnalyzeIOC = () => {
  return useMutation({
    mutationFn: (data: { ioc: string; ioc_type: string }) =>
      apiClient.post('/threat-intel/analyze', data),
  });
};
