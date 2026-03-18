import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface ContainerScanResult {
  id: number;
  type: 'docker' | 'kubernetes';
  target: string;
  vulnerabilities: ContainerVulnerability[];
  status: string;
  scan_date: string;
}

interface ContainerVulnerability {
  package: string;
  version: string;
  cve_id: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  fixed_version?: string;
}

export const useContainerScans = (type?: string) => {
  return useQuery({
    queryKey: ['container-scans', type],
    queryFn: () => apiClient.get<ContainerScanResult[]>('/container/scans', { type }),
  });
};

export const useDockerScan = () => {
  return useMutation({
    mutationFn: (image: string) =>
      apiClient.post('/tools/execute', {
        tool: 'docker_scanner',
        params: { image }
      }),
  });
};

export const useKubernetesScan = () => {
  return useMutation({
    mutationFn: (namespace?: string) =>
      apiClient.post('/tools/execute', {
        tool: 'k8s_scanner',
        params: { namespace }
      }),
  });
};
