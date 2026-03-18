import { useHoneypotStats, useHoneypotLogs } from '../hooks/useHoneypots';
import { Shield, Activity, Globe, AlertTriangle, Loader2 } from 'lucide-react';

export default function HoneypotDashboard() {
  const { data: stats, isLoading: statsLoading } = useHoneypotStats();
  const { data: logs = [], isLoading: logsLoading } = useHoneypotLogs({ limit: 10 });

  if (statsLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500/20 to-emerald-500/20 border border-green-500/30 flex items-center justify-center">
            <Shield className="w-5 h-5 text-green-400" />
          </div>
          Honeypot Dashboard
        </h1>
        <p className="text-gray-400 mt-1 ml-13">Deception system monitoring</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-panel p-4">
          <div className="flex items-center gap-2 text-gray-400 text-sm mb-2">
            <Activity className="w-4 h-4" />
            Total Events
          </div>
          <p className="text-2xl font-bold text-cyan-400">{stats?.total_events || 0}</p>
        </div>
        <div className="glass-panel p-4">
          <div className="flex items-center gap-2 text-gray-400 text-sm mb-2">
            <Globe className="w-4 h-4" />
            Unique IPs
          </div>
          <p className="text-2xl font-bold text-purple-400">{stats?.unique_ips || 0}</p>
        </div>
        <div className="glass-panel p-4">
          <div className="flex items-center gap-2 text-gray-400 text-sm mb-2">
            <AlertTriangle className="w-4 h-4" />
            Top Port
          </div>
          <p className="text-2xl font-bold text-red-400">{stats?.top_ports?.[0]?.port || 'N/A'}</p>
        </div>
        <div className="glass-panel p-4">
          <div className="flex items-center gap-2 text-gray-400 text-sm mb-2">
            <Globe className="w-4 h-4" />
            Top Country
          </div>
          <p className="text-lg font-bold text-amber-400">{stats?.top_countries?.[0]?.country || 'N/A'}</p>
        </div>
      </div>

      <div className="glass-panel rounded-xl overflow-hidden">
        <div className="p-4 border-b border-gray-800 bg-gray-900/50">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-red-400" />
            Recent Intrusion Attempts
          </h2>
        </div>
        {logsLoading ? (
          <div className="flex items-center justify-center p-8">
            <Loader2 className="w-6 h-6 text-cyan-400 animate-spin" />
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Type</th>
                <th>Source IP</th>
                <th>Port</th>
                <th>Protocol</th>
              </tr>
            </thead>
            <tbody>
              {logs.length > 0 ? (
                logs.map((log) => (
                  <tr key={log.id}>
                    <td className="text-sm text-gray-400">{new Date(log.timestamp).toLocaleString()}</td>
                    <td><span className="text-cyan-400 font-bold">{log.honeypot_type}</span></td>
                    <td className="font-mono text-red-400">{log.source_ip}</td>
                    <td className="font-mono">{log.destination_port}</td>
                    <td className="text-gray-400">{log.protocol}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5} className="text-center py-8 text-gray-500">No intrusion attempts detected</td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
