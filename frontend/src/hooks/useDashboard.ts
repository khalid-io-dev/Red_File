import { useQuery } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface DashboardStats {
  total_scans: number;
  active_scans: number;
  total_findings: number;
  critical_findings: number;
  high_findings: number;
  total_campaigns: number;
  active_campaigns: number;
  total_credentials: number;
  validated_credentials: number;
}

interface RecentActivity {
  id: number;
  type: 'scan' | 'finding' | 'campaign' | 'credential';
  title: string;
  description: string;
  timestamp: string;
  severity?: string;
}

export const useDashboardStats = () => {
  return useQuery({
    queryKey: ['dashboard', 'stats'],
    queryFn: () => apiClient.get<DashboardStats>('/dashboard/stats'),
    refetchInterval: 30000, // Refetch every 30 seconds
  });
};

export const useRecentActivity = (limit: number = 10) => {
  return useQuery({
    queryKey: ['dashboard', 'activity', limit],
    queryFn: () => apiClient.get<RecentActivity[]>('/dashboard/activity', { limit }),
    refetchInterval: 15000, // Refetch every 15 seconds
  });
};

export const useSeverityDistribution = () => {
  return useQuery({
    queryKey: ['dashboard', 'severity'],
    queryFn: () => apiClient.get('/dashboard/severity-distribution'),
  });
};

export const useToolUsage = () => {
  return useQuery({
    queryKey: ['dashboard', 'tools'],
    queryFn: () => apiClient.get('/dashboard/tool-usage'),
  });
};
