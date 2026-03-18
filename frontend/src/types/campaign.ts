export interface Campaign {
  id: number;
  name: string;
  description?: string;
  targets: string[];
  chain_type: string;
  status: 'pending' | 'running' | 'paused' | 'completed' | 'failed';
  progress: number;
  findings: any[];
  credentials: any[];
  created_at: string;
  updated_at: string;
}

export interface CreateCampaignRequest {
  name: string;
  description?: string;
  targets: string[];
  chain_type: 'web' | 'network' | 'custom';
  options?: Record<string, any>;
}
