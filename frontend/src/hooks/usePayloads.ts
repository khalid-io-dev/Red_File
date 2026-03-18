import { useMutation, useQuery } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface PayloadRequest {
  type: string;
  platform: string;
  lhost: string;
  lport: string;
  encoder?: string;
  format?: string;
  model?: string;  // AI model selection
}

interface Payload {
  id: number;
  name: string;
  type: string;
  platform: string;
  code: string;
  obfuscated_code?: string;
  file_path?: string;
  created_at: string;
}

export const useGeneratePayload = () => {
  return useMutation({
    mutationFn: (data: PayloadRequest) =>
      apiClient.post<Payload>('/payloads/generate', data),
  });
};

export const usePayloads = () => {
  return useQuery({
    queryKey: ['payloads'],
    queryFn: () => apiClient.get<Payload[]>('/payloads/'),
  });
};

export const useObfuscatePayload = () => {
  return useMutation({
    mutationFn: ({ id, techniques }: { id: number; techniques: string[] }) =>
      apiClient.post(`/payloads/${id}/obfuscate`, { techniques }),
  });
};

export const useAvailableModels = () => {
  return useQuery({
    queryKey: ['payload-models'],
    queryFn: () => apiClient.get<{ models: Record<string, string> }>('/payloads/models'),
  });
};
