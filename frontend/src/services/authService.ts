import api from './api';

interface TokenPayload {
    access_token: string;
    token_type: string;
}

interface User {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name?: string;
    id: number;
}

export const login = async (username: string, password: string): Promise<TokenPayload> => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await api.post<TokenPayload>('/login/access-token', formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });
    return response.data;
};

export const register = async (userData: any): Promise<any> => {
    const response = await api.post('/users/', userData);
    return response.data;
};

export const getMe = async (): Promise<User> => {
    const response = await api.get('/users/me');
    return response.data;
};
