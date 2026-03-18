import { useQuery } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

export const useAgentLogs = (agentId: string, enabled: boolean = true) => {
    return useQuery({
        queryKey: ['agent-logs', agentId],
        queryFn: () => apiClient.get(`/agent/agents/${agentId}/logs?limit=20`),
        enabled,
        refetchInterval: 3000, // Refetch every 3 seconds
    });
};

export const useAgentResults = (agentId: string) => {
    return useQuery({
        queryKey: ['agent-results', agentId],
        queryFn: () => apiClient.get(`/agent/agents/${agentId}/results`),
        refetchInterval: 5000, // Refetch every 5 seconds
    });
};
