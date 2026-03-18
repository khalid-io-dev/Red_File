import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface Tool {
  id: string;
  name: string;
  category: string;
  description: string;
  status: 'available' | 'running' | 'error';
}

interface ExecuteToolData {
  tool_name: string;
  target?: string;
  options?: Record<string, any>;
}

export const useTools = (category?: string) => {
  return useQuery({
    queryKey: ['tools', category],
    queryFn: () => apiClient.get<Tool[]>('/tools/', category ? { category } : undefined),
  });
};

export const useExecuteTool = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ExecuteToolData) => apiClient.post('/tools/execute', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tools'] });
    },
  });
};
