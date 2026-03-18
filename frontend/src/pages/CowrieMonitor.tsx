import { Loader2, Terminal, Shield, AlertTriangle, Users } from 'lucide-react';
import { useHoneypotLogs, useHoneypotStats } from '../../hooks/useHoneypots';

export default function CowrieMonitor() {
  const { data: logsData, isLoading: logsLoading } = useHoneypotLogs({ honeypot_type: 'cowrie' });
  const { data: statsData, isLoading: statsLoading } = useHoneypotStats('cowrie');

  if (logsLoading || statsLoading) return <div className="flex justify-center p-8"><Loader2 className="w-8 h-8 animate-spin" /></div>;

  const logs = logsData?.logs || [];
  const stats = statsData || { total_events: 0, login_attempts: 0, successful_logins: 0, commands_executed: 0 };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Terminal className="w-8 h-8 text-cyan-400" />
        <div>
          <h1 className="text-2xl font-bold">Cowrie SSH Honeypot Monitor</h1>
          <p className="text-gray-400">Medium-interaction SSH/Telnet honeypot</p>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <Shield className="w-4 h-4 text-cyan-400" />
            <div className="text-gray-400 text-sm">Total Events</div>
          </div>
          <div className="text-2xl font-bold">{stats.total_events}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <Users className="w-4 h-4 text-orange-400" />
            <div className="text-gray-400 text-sm">Login Attempts</div>
          </div>
          <div className="text-2xl font-bold">{stats.login_attempts}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-4 h-4 text-red-400" />
            <div className="text-gray-400 text-sm">Successful Logins</div>
          </div>
          <div className="text-2xl font-bold">{stats.successful_logins}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <Terminal className="w-4 h-4 text-green-400" />
            <div className="text-gray-400 text-sm">Commands Executed</div>
          </div>
          <div className="text-2xl font-bold">{stats.commands_executed}</div>
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        <div className="p-4 border-b border-white/10">
          <h2 className="text-lg font-bold">Recent Activity</h2>
        </div>
        {logs.length > 0 ? (
          <div className="divide-y divide-white/10">
            {logs.map((log: any) => (
              <div key={log.id} className="p-4 hover:bg-white/5">
                <div className="flex items-start justify-between mb-2">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`px-2 py-0.5 rounded text-xs ${
                        log.severity === 'critical' ? 'bg-red-500/20 text-red-400' :
                        log.severity === 'high' ? 'bg-orange-500/20 text-orange-400' :
                        log.severity === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                        'bg-blue-500/20 text-blue-400'
                      }`}>{log.severity}</span>
                      <span className="text-cyan-400 font-mono text-sm">{log.event_type}</span>
                    </div>
                    <div className="text-sm text-gray-300 mb-1">Source: {log.source_ip}</div>
                    {log.username && (
                      <div className="text-sm text-gray-400">
                        Credentials: <span className="font-mono">{log.username}:{log.password || '***'}</span>
                      </div>
                    )}
                    {log.command && (
                      <div className="text-xs text-gray-500 font-mono mt-1 bg-black/20 p-2 rounded">$ {log.command}</div>
                    )}
                  </div>
                  <div className="text-sm text-gray-400">{new Date(log.timestamp).toLocaleString()}</div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center text-gray-400 py-12">No activity recorded</div>
        )}
      </div>
    </div>
  );
}
