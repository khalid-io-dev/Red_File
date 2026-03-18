export interface Finding {
  id: number;
  title: string;
  description: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  target: string;
  tool: string;
  evidence: string;
  remediation?: string;
  cvss_score?: number;
  cve_id?: string;
  created_at: string;
  scan_id?: number;
  campaign_id?: number;
}

export interface FindingStats {
  total: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
  info: number;
}
