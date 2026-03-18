import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';
import { Target, Shield, Key, FileText, TrendingUp, Activity } from 'lucide-react';
import SeverityChart from '../components/charts/SeverityChart';
import ToolDistribution from '../components/charts/ToolDistribution';
import TimelineChart from '../components/charts/TimelineChart';

export default function SimpleDashboard() {
  const { data: stats } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const [scans, findings, credentials] = await Promise.all([
        api.get('/scans/'),
        api.get('/findings/stats/summary'),
        api.get('/credentials/stats'),
      ]);
      return {
        scans: scans.data.length || 0,
        findings: findings.data,
        credentials: credentials.data.total || 0,
      };
    },
  });

  const { data: recentScans } = useQuery({
    queryKey: ['recent-scans'],
    queryFn: async () => {
      const { data } = await api.get('/scans/?limit=5');
      return data;
    },
  });

  const timelineData = [
    { date: '2024-01-20', scans: 5, findings: 12 },
    { date: '2024-01-21', scans: 8, findings: 18 },
    { date: '2024-01-22', scans: 6, findings: 15 },
    { date: '2024-01-23', scans: 10, findings: 25 },
    { date: '2024-01-24', scans: 7, findings: 20 },
    { date: '2024-01-25', scans: 9, findings: 22 },
    { date: '2024-01-26', scans: 11, findings: 28 },
  ];

  const toolData = {
    nmap: 15,
    sqlmap: 12,
    nikto: 10,
    hydra: 8,
    nuclei: 7,
    gobuster: 6,
    wpscan: 5,
    masscan: 4,
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <p className="text-gray-400 mt-1">Security operations overview</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-panel p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Total Scans</p>
              <p className="text-3xl font-bold text-cyan-400">{stats?.scans || 0}</p>
            </div>
            <Target className="w-12 h-12 text-cyan-400 opacity-20" />
          </div>
        </div>

        <div className="glass-panel p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Findings</p>
              <p className="text-3xl font-bold text-red-400">{stats?.findings?.total || 0}</p>
            </div>
            <Shield className="w-12 h-12 text-red-400 opacity-20" />
          </div>
        </div>

        <div className="glass-panel p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Credentials</p>
              <p className="text-3xl font-bold text-green-400">{stats?.credentials || 0}</p>
            </div>
            <Key className="w-12 h-12 text-green-400 opacity-20" />
          </div>
        </div>

        <div className="glass-panel p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Reports</p>
              <p className="text-3xl font-bold text-purple-400">12</p>
            </div>
            <FileText className="w-12 h-12 text-purple-400 opacity-20" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-panel p-6">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-cyan-400" />
            Findings by Severity
          </h2>
          {stats?.findings && (
            <SeverityChart data={stats.findings} />
          )}
        </div>

        <div className="glass-panel p-6">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Activity className="w-5 h-5 text-cyan-400" />
            Tool Usage
          </h2>
          <ToolDistribution data={toolData} />
        </div>
      </div>

      <div className="glass-panel p-6">
        <h2 className="text-xl font-bold text-white mb-4">Activity Timeline</h2>
        <TimelineChart data={timelineData} />
      </div>

      <div className="glass-panel p-6">
        <h2 className="text-xl font-bold text-white mb-4">Recent Scans</h2>
        <div className="space-y-3">
          {recentScans?.map((scan: any) => (
            <div key={scan.id} className="flex items-center justify-between p-3 bg-gray-800/50 rounded-lg border border-gray-700">
              <div>
                <p className="text-gray-300 font-medium">{scan.target_url}</p>
                <p className="text-sm text-gray-400">{scan.scan_type}</p>
              </div>
              <div className="text-right">
                <span className={`px-2 py-1 rounded text-xs ${
                  scan.status === 'COMPLETED' ? 'bg-green-500/20 text-green-400' :
                  scan.status === 'RUNNING' ? 'bg-blue-500/20 text-blue-400' :
                  'bg-gray-500/20 text-gray-400'
                }`}>
                  {scan.status}
                </span>
                <p className="text-xs text-gray-500 mt-1">{new Date(scan.created_at).toLocaleDateString()}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
