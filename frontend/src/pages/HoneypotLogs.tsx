import { useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Loader2, ArrowLeft } from 'lucide-react';
import { useCowrieLogs, useDionaeaLogs } from '../hooks/useHoneypots';

export default function HoneypotLogs() {
  const [searchParams] = useSearchParams();
  const ipFilter = searchParams.get('ip') || '';
  
  // Get logs from both honeypots
  const { data: cowrieData, isLoading: cowrieLoading } = useCowrieLogs();
  const { data: dionaeaData, isLoading: dionaeaLoading } = useDionaeaLogs();
  
  const isLoading = cowrieLoading || dionaeaLoading;

  if (isLoading) return <div className="flex justify-center p-8"><Loader2 className="w-8 h-8 animate-spin" /></div>;

  // Combine and filter logs
  const allLogs: any[] = [];
  
  // Add Cowrie logs
  if (cowrieData?.attacks) {
    for (const attack of cowrieData.attacks) {
      allLogs.push({
        id: attack.timestamp + attack.src_ip,
        honeypot_type: 'cowrie',
        source_ip: attack.src_ip,
        destination_port: '2222',
        event_type: attack.eventid || 'connection',
        timestamp: attack.timestamp,
        details: attack
      });
    }
  }
  
  // Add Dionaea logs
  if (dionaeaData?.attacks) {
    for (const attack of dionaeaData.attacks) {
      allLogs.push({
        id: attack.timestamp + attack.src_ip,
        honeypot_type: 'dionaea',
        source_ip: attack.src_ip,
        destination_port: attack.dst_port || '80',
        event_type: attack.eventid || 'connection',
        timestamp: attack.timestamp,
        details: attack
      });
    }
  }
  
  // Filter by IP if specified
  const filteredLogs = ipFilter 
    ? allLogs.filter(log => log.source_ip === ipFilter)
    : allLogs;

  // Sort by timestamp (newest first)
  filteredLogs.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to="/honeypots" className="p-2 rounded-lg hover:bg-white/10 text-gray-400 hover:text-white">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold">
              {ipFilter ? `Attack Logs: ${ipFilter}` : 'Honeypot Logs'}
            </h1>
            {ipFilter && (
              <p className="text-gray-400 text-sm">
                Showing all activity from this attacker IP
              </p>
            )}
          </div>
        </div>
        <div className="text-gray-400 text-sm">
          {filteredLogs.length} events
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        {filteredLogs.length > 0 ? (
          <div className="divide-y divide-white/10">
            {filteredLogs.map((log) => (
              <div key={log.id} className="p-4 hover:bg-white/5">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-cyan-400 font-mono text-sm">{log.honeypot_type}</span>
                      <span className={`px-2 py-0.5 rounded text-xs ${
                        log.event_type?.includes('success') ? 'bg-green-500/20 text-green-400' :
                        log.event_type?.includes('failed') ? 'bg-red-500/20 text-red-400' :
                        'bg-blue-500/20 text-blue-400'
                      }`}>
                        {log.event_type || 'connection'}
                      </span>
                    </div>
                    <div className="text-gray-300 mb-2">
                      {log.details?.username && `User: ${log.details.username} `}
                      {log.details?.password && `Pass: ${log.details.password} `}
                      {log.details?.input && `Cmd: ${log.details.input}`}
                    </div>
                    <div className="text-sm text-gray-400">
                      Source: {log.source_ip} → Port: {log.destination_port}
                    </div>
                  </div>
                  <div className="text-sm text-gray-400">
                    {new Date(log.timestamp).toLocaleString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center text-gray-400 py-12">
            {ipFilter ? `No logs found for IP: ${ipFilter}` : 'No logs found'}
          </div>
        )}
      </div>
    </div>
  );
}
