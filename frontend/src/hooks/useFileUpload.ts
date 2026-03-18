import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
}

export const useFileUpload = (endpoint: string) => {
  const [progress, setProgress] = useState<UploadProgress>({ loaded: 0, total: 0, percentage: 0 });

  const mutation = useMutation({
    mutationFn: async (file: File) => {
      return await apiClient.upload(endpoint, file, (percentage) => {
        setProgress({
          loaded: (file.size * percentage) / 100,
          total: file.size,
          percentage,
        });
      });
    },
    onSuccess: () => {
      setProgress({ loaded: 0, total: 0, percentage: 0 });
    },
  });

  return {
    upload: mutation.mutate,
    isUploading: mutation.isPending,
    progress,
    error: mutation.error,
    data: mutation.data,
  };
};

// Specific upload hooks
export const useMalwareUpload = () => useFileUpload('/upload/malware');
export const useWordlistUpload = () => useFileUpload('/upload/wordlist');
export const useReportUpload = () => useFileUpload('/upload/report');
