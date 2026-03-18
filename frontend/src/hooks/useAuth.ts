import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import apiClient from '../lib/api-client';

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  full_name: string;
}

interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const useLogin = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (credentials: LoginCredentials) => {
      const data = await apiClient.login(credentials.email, credentials.password);
      return data as LoginResponse;
    },
    onSuccess: (data) => {
      localStorage.setItem('token', data.access_token);
      queryClient.invalidateQueries({ queryKey: ['currentUser'] });
      navigate('/');
    },
  });
};

export const useRegister = () => {
  const navigate = useNavigate();

  return useMutation({
    mutationFn: async (data: RegisterData) => {
      return await apiClient.register(data);
    },
    onSuccess: () => {
      navigate('/login');
    },
  });
};

export const useCurrentUser = () => {
  return useQuery({
    queryKey: ['currentUser'],
    queryFn: async () => {
      const user = await apiClient.getCurrentUser();
      localStorage.setItem('user', JSON.stringify(user));
      return user as User;
    },
    enabled: !!localStorage.getItem('token'),
    retry: false,
  });
};

export const useLogout = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      await apiClient.logout();
    },
    onSuccess: () => {
      queryClient.clear();
      navigate('/login');
    },
  });
};
