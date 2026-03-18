import React, { createContext, useContext, ReactNode } from 'react';
import { useCurrentUser } from '../hooks/useAuth';

interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: Error | null;
}

const AuthContext = createContext<AuthContextType>(null!);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { data: user, isLoading, error } = useCurrentUser();

  return (
    <AuthContext.Provider value={{ user: user || null, loading: isLoading, error: error as Error | null }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
