import { useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

export const useEmailHarvest = () => {
  return useMutation({
    mutationFn: (domain: string) => apiClient.post('/osint/email-harvest', { domain }),
  });
};

export const useWhoisLookup = () => {
  return useMutation({
    mutationFn: (domain: string) => apiClient.post('/osint/whois', { domain }),
  });
};

export const useSubdomainEnum = () => {
  return useMutation({
    mutationFn: (domain: string) => apiClient.post('/osint/subdomains', { domain }),
  });
};

export const useSocialProfiles = () => {
  return useMutation({
    mutationFn: (username: string) => apiClient.post('/osint/social-profiles', { username }),
  });
};

export const useGeolocation = () => {
  return useMutation({
    mutationFn: (ip_address: string) => apiClient.post('/osint/geolocation', { ip_address }),
  });
};

export const useFullOSINT = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (target: string) => apiClient.post('/osint/full-scan', { target }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['osint'] });
    },
  });
};
