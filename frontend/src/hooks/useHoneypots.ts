import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

// Types for honeypot status
export interface HoneypotStatus {
  cowrie: {
    status: 'running' | 'stopped' | 'not_configured';
    log_path?: string;
    port: number;
  };
  dionaea: {
    status: 'running' | 'stopped' | 'not_configured';
    port: string;
  };
}

// Types for honeypot logs
export interface HoneypotLogEntry {
  honeypot: string;
  attacks: any[];
  total_attacks: number;
  unique_ips: number;
  credentials_tried?: Array<{
    username: string;
    password: string;
    src_ip: string;
    success?: boolean;
  }>;
}

// Types for analytics
export interface HoneypotAnalytics {
  total_attacks: number;
  unique_attackers: number;
  top_attackers: Array<{ ip: string; count: number }>;
  dionaea_stats: HoneypotLogEntry;
  cowrie_stats: HoneypotLogEntry;
  attack_timeline: Array<{
    timestamp: string;
    honeypot: string;
    src_ip: string;
    target_port?: string;
    credentials?: string;
  }>;
}

// Fetch honeypot status (running/stopped)
export const useHoneypotStatus = () => {
  return useQuery({
    queryKey: ['honeypots', 'status'],
    queryFn: () => apiClient.get<HoneypotStatus>('/enhancements/honeypot/status'),
    refetchInterval: 30000, // Refresh every 30 seconds
  });
};

// Fetch Cowrie logs
export const useCowrieLogs = () => {
  return useQuery({
    queryKey: ['honeypots', 'cowrie'],
    queryFn: () => apiClient.get<HoneypotLogEntry>('/enhancements/honeypot/cowrie'),
    refetchInterval: 10000, // Refresh every 10 seconds
  });
};

// Fetch Dionaea logs
export const useDionaeaLogs = () => {
  return useQuery({
    queryKey: ['honeypots', 'dionaea'],
    queryFn: () => apiClient.get<HoneypotLogEntry>('/enhancements/honeypot/dionaea'),
    refetchInterval: 10000,
  });
};

// Fetch honeypot analytics
export const useHoneypotAnalytics = () => {
  return useQuery({
    queryKey: ['honeypots', 'analytics'],
    queryFn: () => apiClient.get<HoneypotAnalytics>('/enhancements/honeypot/analytics'),
    refetchInterval: 30000,
  });
};

// Legacy hook - kept for backward compatibility
export const useHoneypotLogs = (params?: { 
  skip?: number; 
  limit?: number; 
  honeypot_type?: string;
  start_date?: string;
  end_date?: string;
}) => {
  return useQuery({
    queryKey: ['honeypots', 'logs', params],
    queryFn: () => apiClient.get<any[]>('/honeypots/logs', params),
    refetchInterval: 10000,
  });
};

export const useHoneypotStats = (honeypotType?: string) => {
  return useQuery({
    queryKey: ['honeypots', 'stats', honeypotType],
    queryFn: () => apiClient.get<any>('/honeypots/stats', honeypotType ? { type: honeypotType } : undefined),
    refetchInterval: 30000,
  });
};

// Start a honeypot
export const useStartHoneypot = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (honeypotType: string) => 
      apiClient.post<{ success: boolean; message: string }>(`/enhancements/honeypot/start`, { honeypot_type: honeypotType }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['honeypots'] });
    },
  });
};

// Stop a honeypot
export const useStopHoneypot = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (honeypotType: string) => 
      apiClient.post<{ success: boolean; message: string }>(`/enhancements/honeypot/stop`, { honeypot_type: honeypotType }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['honeypots'] });
    },
  });
};
