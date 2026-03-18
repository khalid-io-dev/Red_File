import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface CloudScanResult {
  id: number;
  provider: 'aws' | 'azure' | 'gcp';
  scan_type: string;
  findings: CloudFinding[];
  status: string;
  started_at: string;
  completed_at?: string;
}

interface CloudFinding {
  resource: string;
  issue: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  recommendation: string;
}

interface CloudScanRequest {
  provider: 'aws' | 'azure' | 'gcp';
  scan_types: string[];
  credentials?: {
    access_key?: string;
    secret_key?: string;
    subscription_id?: string;
    project_id?: string;
  };
}

export const useCloudScans = (provider?: string) => {
  return useQuery({
    queryKey: ['cloud-scans', provider],
    queryFn: () => apiClient.get<CloudScanResult[]>('/cloud/scans', { provider }),
  });
};

export const useCloudScan = (id: number) => {
  return useQuery({
    queryKey: ['cloud-scans', id],
    queryFn: () => apiClient.get<CloudScanResult>(`/cloud/scans/${id}`),
    enabled: !!id,
  });
};

export const useStartCloudScan = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CloudScanRequest) => 
      apiClient.post<CloudScanResult>('/cloud/scan', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cloud-scans'] });
    },
  });
};

export const useAWSSecurityCheck = () => {
  return useMutation({
    mutationFn: (scanTypes: string[]) =>
      apiClient.post('/tools/execute', {
        tool: 'aws_scanner',
        params: { scan_types: scanTypes }
      }),
  });
};

export const useAzureSecurityCheck = () => {
  return useMutation({
    mutationFn: (scanTypes: string[]) =>
      apiClient.post('/tools/execute', {
        tool: 'azure_scanner',
        params: { scan_types: scanTypes }
      }),
  });
};

export const useGCPSecurityCheck = () => {
  return useMutation({
    mutationFn: (scanTypes: string[]) =>
      apiClient.post('/tools/execute', {
        tool: 'gcp_scanner',
        params: { scan_types: scanTypes }
      }),
  });
};

// Combined hook for CloudSecurityDashboard component
export const useCloudSecurity = () => {
  const { data: cloudScans, isLoading: isLoadingScans, refetch: refetchScans } = useCloudScans();
  const startScan = useStartCloudScan();
  const awsCheck = useAWSSecurityCheck();
  const azureCheck = useAzureSecurityCheck();
  const gcpCheck = useGCPSecurityCheck();

  const scanCloud = async (provider: string) => {
    try {
      switch (provider) {
        case 'aws':
          return await awsCheck.mutateAsync(['config', 'iam', 's3']);
        case 'azure':
          return await azureCheck.mutateAsync(['storage', 'compute', 'network']);
        case 'gcp':
          return await gcpCheck.mutateAsync(['storage', 'compute', 'networking']);
        default:
          throw new Error(`Unknown provider: ${provider}`);
      }
    } catch (error) {
      console.error('Scan failed:', error);
      throw error;
    }
  };

  const getCloudStatus = async () => {
    return {
      aws: { connected: true, lastScan: '2024-01-15T10:30:00Z' },
      azure: { connected: true, lastScan: '2024-01-15T09:00:00Z' },
      gcp: { connected: false, lastScan: null },
    };
  };

  const getScanHistory = async () => {
    return cloudScans || [];
  };

  return {
    scanCloud,
    getCloudStatus,
    getScanHistory,
    isLoading: isLoadingScans || startScan.isPending,
    scans: cloudScans,
    refetchScans,
  };
};
