import { useMutation, useQuery } from '@tanstack/react-query';
import apiClient from '../lib/api-client';

// ============================================================================
// AI Agent Hooks
// ============================================================================

interface ChatMessage {
    role: string;
    content: string;
}

interface ChatRequest {
    messages: ChatMessage[];
    stream?: boolean;
}

interface TaskRequest {
    task: string;
    context?: Record<string, any>;
    stream?: boolean;
}

export const useAIChat = () => {
    return useMutation({
        mutationFn: (data: ChatRequest) =>
            apiClient.post('/agent/chat', data),
    });
};

export const useAITask = () => {
    return useMutation({
        mutationFn: (data: TaskRequest) =>
            apiClient.post('/agent/task', data),
    });
};

export const useAIStatus = () => {
    return useQuery({
        queryKey: ['ai-status'],
        queryFn: () => apiClient.get('/agent/status'),
    });
};

export const useAgents = () => {
    return useQuery({
        queryKey: ['agents'],
        queryFn: () => apiClient.get(`/agent/agents?_t=${Date.now()}`),
    });
};

export const useStartAgent = () => {
    return useMutation({
        mutationFn: ({ agentId, target }: { agentId: string; target?: string }) => {
            console.log('useStartAgent called with:', { agentId, target });
            const params = target && target.trim() ? { target: target.trim() } : {};
            console.log('Sending params:', params);
            return apiClient.post(`/agent/agents/${agentId}/start`, null, { params });
        },
    });
};

export const usePauseAgent = () => {
    return useMutation({
        mutationFn: (agentId: string) =>
            apiClient.post(`/agent/agents/${agentId}/pause`),
    });
};

// ============================================================================
// MITRE ATT&CK Hooks
// ============================================================================

export const useMITRECoverage = (tools?: string[]) => {
    return useQuery({
        queryKey: ['mitre-coverage', tools],
        queryFn: () => apiClient.get(`/attack-chain/mitre/coverage?tools=${tools?.join(',') || ''}`),
    });
};

export const useMITRESuggest = () => {
    return useMutation({
        mutationFn: (currentTechniques: string[]) =>
            apiClient.get(`/attack-chain/mitre/suggest?current_techniques=${currentTechniques.join(',')}`),
    });
};

export const useMITREMatrix = (tools?: string[]) => {
    return useQuery({
        queryKey: ['mitre-matrix', tools],
        queryFn: () => apiClient.get(`/attack-chain/mitre/matrix?tools=${tools?.join(',') || ''}`),
    });
};

export const useMITRENavigator = (tools?: string[]) => {
    return useQuery({
        queryKey: ['mitre-navigator', tools],
        queryFn: () => apiClient.get(`/attack-chain/mitre/navigator?tools=${tools?.join(',') || ''}`),
        enabled: false, // Only fetch when explicitly requested
    });
};

// ============================================================================
// Attack Chain Hooks
// ============================================================================

interface AttackChainRequest {
    target: string;
    chain_type?: string;
}

interface AgentRequest {
    target: string;
    agent_type?: string;
}

export const useAttackChainExecute = () => {
    return useMutation({
        mutationFn: (data: AttackChainRequest) =>
            apiClient.post('/attack-chain/chain/execute', data),
    });
};

export const useAgentExecute = () => {
    return useMutation({
        mutationFn: (data: AgentRequest) =>
            apiClient.post('/attack-chain/agent/execute', data),
    });
};

// ============================================================================
// Campaign Reasoning Hooks
// ============================================================================

export const useReasoningAnalysis = () => {
    return useMutation({
        mutationFn: (data: { results: Record<string, any>; model?: string }) =>
            apiClient.post('/campaign/reasoning/analyze', data),
    });
};

export const useReasoningStrategy = () => {
    return useMutation({
        mutationFn: (data: { target: string; recon_data: Record<string, any>; model?: string }) =>
            apiClient.post('/campaign/reasoning/strategy', data),
    });
};

export const useReasoningNextAction = () => {
    return useMutation({
        mutationFn: (data: { findings: any[]; tools_used: string[]; model?: string }) =>
            apiClient.post('/campaign/reasoning/next-action', data),
    });
};

export const useReasoningAttackPath = () => {
    return useMutation({
        mutationFn: (data: { findings: Record<string, any>; model?: string }) =>
            apiClient.post('/campaign/reasoning/attack-path', data),
    });
};

export const useReasoningDetectDefenses = () => {
    return useMutation({
        mutationFn: (data: { tool_outputs: Record<string, string>; model?: string }) =>
            apiClient.post('/campaign/reasoning/detect-defenses', data),
    });
};

// ============================================================================
// Social Engineering Hooks
// ============================================================================

interface OSINTRequest {
    target: string;
    target_type: string;
}

interface EmailCraftRequest {
    target_info: Record<string, any>;
    payload_link: string;
    template_type?: string;
}

interface SECampaignCreate {
    name: string;
    target_email: string;
    target_name?: string;
    target_company?: string;
    template_type: string;
    payload_id?: number;
}

export const useSEOSINT = () => {
    return useMutation({
        mutationFn: (data: OSINTRequest) =>
            apiClient.post('/social/osint', data),
    });
};

export const useEmailCraft = () => {
    return useMutation({
        mutationFn: (data: EmailCraftRequest) =>
            apiClient.post('/social/email-craft', data),
    });
};

export const useSECampaigns = () => {
    return useQuery({
        queryKey: ['se-campaigns'],
        queryFn: () => apiClient.get('/social/campaigns'),
    });
};

export const useCreateSECampaign = () => {
    return useMutation({
        mutationFn: (data: SECampaignCreate) =>
            apiClient.post('/social/campaign', data),
    });
};

export const useFakeLogin = () => {
    return useMutation({
        mutationFn: (brand: string) =>
            apiClient.post('/social/fake-login', { brand }),
    });
};

export const useTrackingLink = () => {
    return useMutation({
        mutationFn: (url: string) =>
            apiClient.post('/social/tracking-link', { url }),
    });
};

export const useSpearPhishing = () => {
    return useMutation({
        mutationFn: (target_info: Record<string, any>) =>
            apiClient.post('/social/spear-phishing', { target_info }),
    });
};

// ============================================================================
// Advanced Tools Hooks
// ============================================================================

interface BinaryAnalysisRequest {
    binary_path: string;
    analysis_type?: string;
}

interface WebScanRequest {
    target_url: string;
    scan_type?: string;
}

interface JWTAnalysisRequest {
    token: string;
    crack?: boolean;
    wordlist?: string;
}

interface ADAssessmentRequest {
    domain: string;
    username: string;
    password: string;
    assessment_type?: string;
}

interface NetworkScanRequest {
    target: string;
    scan_type?: string;
}

// Reverse Engineering
export const useReverseEngineering = () => {
    return useMutation({
        mutationFn: (data: BinaryAnalysisRequest) => {
            console.log('[useReverseEngineering] Sending request:', data);
            return apiClient.post('/advanced-tools/reverse-engineering/analyze', data);
        },
    });
};

export const useUploadBinary = () => {
    return useMutation({
        mutationFn: ({ file, analysis_type }: { file: File; analysis_type?: string }) => {
            console.log('[useUploadBinary] Uploading file:', file.name, 'analysis_type:', analysis_type);
            const formData = new FormData();
            formData.append('file', file);
            if (analysis_type) {
                formData.append('analysis_type', analysis_type);
            }
            return apiClient.post('/advanced-tools/reverse-engineering/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
        },
    });
};

export const useRETools = () => {
    return useQuery({
        queryKey: ['re-tools'],
        queryFn: () => {
            console.log('[useRETools] Fetching tools...');
            return apiClient.get('/advanced-tools/reverse-engineering/tools');
        },
    });
};

// Web Tools
export const useWebToolsScan = () => {
    return useMutation({
        mutationFn: (data: WebScanRequest) => {
            console.log('[useWebToolsScan] Sending request:', data);
            return apiClient.post('/advanced-tools/web-tools/scan', data);
        },
    });
};

export const useJWTAnalysis = () => {
    return useMutation({
        mutationFn: (data: JWTAnalysisRequest) => {
            console.log('[useJWTAnalysis] Sending request');
            return apiClient.post('/advanced-tools/web-tools/jwt/analyze', data);
        },
    });
};

export const useWfuzz = () => {
    return useMutation({
        mutationFn: (data: { target_url: string; wordlist?: string }) => {
            console.log('[useWfuzz] Sending request:', data);
            return apiClient.post('/advanced-tools/web-tools/wfuzz', null, { params: data });
        },
    });
};

// Network Tools
export const useADAssessment = () => {
    return useMutation({
        mutationFn: (data: ADAssessmentRequest) =>
            apiClient.post('/advanced-tools/network-tools/ad-assessment', data),
    });
};

export const useNetworkToolsScan = () => {
    return useMutation({
        mutationFn: (data: NetworkScanRequest) =>
            apiClient.post('/advanced-tools/network-tools/scan', data),
    });
};

export const useResponder = () => {
    return useMutation({
        mutationFn: (data: { interface: string; duration?: number }) =>
            apiClient.post('/advanced-tools/network-tools/responder', null, { params: data }),
    });
};

export const useKerbrute = () => {
    return useMutation({
        mutationFn: (data: { domain: string; userlist?: string }) =>
            apiClient.post('/advanced-tools/network-tools/kerbrute', null, { params: data }),
    });
};

export const useToolsStatus = () => {
    return useQuery({
        queryKey: ['tools-status'],
        queryFn: () => apiClient.get('/advanced-tools/tools/status'),
    });
};
