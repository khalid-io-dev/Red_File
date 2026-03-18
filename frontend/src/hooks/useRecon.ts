import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

// ============================================================================
// Types
// ============================================================================

interface OSINTSearchRequest {
    query: string;
    source_type?: string;
    sources?: string[];
}

interface OSINTSearchResult {
    query: string;
    type: string;
    timestamp: string;
    sources_checked: string[];
    findings: Array<{
        type: string;
        data: string;
        source: string;
    }>;
}

interface Investigation {
    id: number;
    target: string;
    type: string;
    status: string;
    findings: number;
    date: string;
}

interface InvestigationCreate {
    target: string;
    investigation_type: string;
    notes?: string;
}

interface DomainIntelligence {
    domain: string;
    whois: {
        registrar: string;
        created: string;
        expires: string;
        nameservers: string[];
    };
    dns: {
        a_records: string[];
        mx_records: string[];
        txt_records: string[];
    };
    subdomains: string[];
    technologies: string[];
}

// ============================================================================
// OSINT Search Hook
// ============================================================================

export const useOSINTSearch = () => {
    return useMutation({
        mutationFn: (data: OSINTSearchRequest) =>
            apiClient.post<OSINTSearchResult>('/recon/search', data),
    });
};

// ============================================================================
// Investigation Hooks
// ============================================================================

export const useInvestigations = () => {
    return useQuery({
        queryKey: ['investigations'],
        queryFn: () => apiClient.get<Investigation[]>('/recon/investigations'),
    });
};

export const useInvestigation = (id: string) => {
    return useQuery({
        queryKey: ['investigation', id],
        queryFn: () => apiClient.get<Investigation>(`/recon/investigations/${id}`),
        enabled: !!id,
    });
};

export const useCreateInvestigation = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: InvestigationCreate) =>
            apiClient.post('/recon/investigations', data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['investigations'] });
        },
    });
};

export const useDeleteInvestigation = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: number) => apiClient.delete(`/recon/investigations/${id}`),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['investigations'] });
        },
    });
};

// ============================================================================
// Investigation History Hook
// ============================================================================

export const useInvestigationHistory = () => {
    return useQuery({
        queryKey: ['investigation-history'],
        queryFn: () => apiClient.get('/recon/investigations/history'),
    });
};

// ============================================================================
// Domain Intelligence Hook
// ============================================================================

export const useDomainIntelligence = (domain: string) => {
    return useQuery({
        queryKey: ['domain', domain],
        queryFn: () => apiClient.get<DomainIntelligence>(`/recon/domain/${domain}`),
        enabled: !!domain,
    });
};

// ============================================================================
// Email Harvesting Hook
// ============================================================================

interface EmailHarvestRequest {
    domain: string;
    source?: string;
}

export const useEmailHarvesting = () => {
    return useMutation({
        mutationFn: (data: EmailHarvestRequest) =>
            apiClient.post('/recon/email/harvest', data),
    });
};

// ============================================================================
// Social Media Search Hook
// ============================================================================

interface SocialSearchRequest {
    username: string;
    platforms?: string[];
}

export const useSocialMediaSearch = () => {
    return useMutation({
        mutationFn: (data: SocialSearchRequest) =>
            apiClient.post('/recon/social/search', data),
    });
};

// ============================================================================
// Network Discovery Hook
// ============================================================================

interface NetworkDiscoveryRequest {
    target: string;
    scan_type?: string;
}

export const useNetworkDiscovery = () => {
    return useMutation({
        mutationFn: (data: NetworkDiscoveryRequest) =>
            apiClient.post('/recon/network/discover', data),
    });
};

// ============================================================================
// Breach Search Hook
// ============================================================================

interface BreachSearchRequest {
    email: string;
    sources?: string[];
}

export const useBreachSearch = () => {
    return useMutation({
        mutationFn: (data: BreachSearchRequest) =>
            apiClient.post('/recon/breaches/search', data),
    });
};

// ============================================================================
// Email Intelligence Hook
// ============================================================================

export const useEmailIntelligence = (email: string) => {
    return useQuery({
        queryKey: ['email', email],
        queryFn: () => apiClient.get(`/recon/email/${email}`),
        enabled: !!email,
    });
};

// ============================================================================
// IP Intelligence Hook
// ============================================================================

export const useIPIntelligence = (ip: string) => {
    return useQuery({
        queryKey: ['ip', ip],
        queryFn: () => apiClient.get(`/recon/ip/${ip}`),
        enabled: !!ip,
    });
};
