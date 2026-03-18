import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'admin' | 'analyst' | 'viewer';
  is_active: boolean;
  created_at: string;
}

interface CreateUserData {
  email: string;
  full_name: string;
  password: string;
  role: string;
}

interface UpdateUserData {
  email?: string;
  full_name?: string;
  role?: string;
  is_active?: boolean;
}

export const useUsers = (params?: { skip?: number; limit?: number; role?: string }) => {
  return useQuery({
    queryKey: ['users', params],
    queryFn: () => apiClient.get<User[]>('/user-management/users', params),
  });
};

export const useUser = (id: number) => {
  return useQuery({
    queryKey: ['users', id],
    queryFn: () => apiClient.get<User>(`/user-management/users/${id}`),
    enabled: !!id,
  });
};

export const useCreateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateUserData) => apiClient.post<User>('/user-management/users', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};

export const useUpdateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateUserData }) =>
      apiClient.put<User>(`/user-management/users/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};

export const useDeleteUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => apiClient.delete(`/user-management/users/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};
