export interface Scan {
  id: number;
  target: string;
  scan_type: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  results: any;
  created_at: string;
  updated_at: string;
  user_id: number;
}

export interface CreateScanRequest {
  target: string;
  scan_type: 'quick' | 'deep' | 'passive';
  tools?: string[];
  options?: Record<string, any>;
}
