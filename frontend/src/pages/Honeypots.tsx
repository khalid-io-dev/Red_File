import { Loader2, Play, Pause, RotateCcw } from 'lucide-react';
import { useHoneypotStatus, useCowrieLogs, useDionaeaLogs, useHoneypotAnalytics, HoneypotStatus, HoneypotLogEntry, HoneypotAnalytics } from '../hooks/useHoneypots';

export default function Honeypots() {
    // Fetch honeypot status
    const { data: status, isLoading: statusLoading, refetch: refetchStatus } = useHoneypotStatus();
    
    // Fetch logs from each honeypot
    const { data: cowrieData, isLoading: cowrieLoading } = useCowrieLogs();
    const { data: dionaeaData, isLoading: dionaeaLoading } = useDionaeaLogs();
    
    // Fetch analytics
    const { data: analytics, isLoading: analyticsLoading } = useHoneypotAnalytics();

    const isLoading = statusLoading || cowrieLoading || dionaeaLoading || analyticsLoading;

    // Helper to get status color
    const getStatusColor = (honeypotStatus: string) => {
        switch (honeypotStatus) {
            case 'running':
                return {
                    bg: 'bg-green-500',
                    text: 'text-green-500',
                    border: 'hover:border-green-500/30',
                    glow: 'shadow-[0_0_10px_rgba(34,197,94,0.5)]'
                };
            case 'stopped':
                return {
                    bg: 'bg-red-500',
                    text: 'text-red-500',
                    border: 'hover:border-red-500/30',
                    glow: 'shadow-[0_0_10px_rgba(239,68,68,0.5)]'
                };
            default:
                return {
                    bg: 'bg-gray-500',
                    text: 'text-gray-500',
                    border: 'hover:border-gray-500/30',
                    glow: 'shadow-[0_0_10px_rgba(107,114,128,0.5)]'
                };
        }
    };

    // Get all logs from analytics timeline
    const getAllLogs = () => {
        if (!analytics?.attack_timeline) return [];
        return analytics.attack_timeline.map((entry, idx) => ({
            id: idx,
            timestamp: entry.timestamp,
            honeypot_type: entry.honeypot,
            source_ip: entry.src_ip,
            destination_port: entry.target_port || 0,
            protocol: entry.target_port ? 'TCP' : 'SSH',
            credentials: entry.credentials
        }));
    };

    const logs = getAllLogs();

    return (
        <div className="space-y-8">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-3xl font-bold text-white tracking-tight">Honeypot Grid</h2>
                    <p className="text-gray-400 text-sm mt-1">Deception systems status and intrusion logs</p>
                </div>
                <button 
                    onClick={() => {
                        refetchStatus();
                    }}
                    className="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg text-sm transition-colors"
                >
                    <RotateCcw className="w-4 h-4" />
                    Refresh
                </button>
            </div>

            {/* Honeypot Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Dionaea Card */}
                <div className={`glass-panel p-6 rounded-xl border border-gray-800 relative overflow-hidden group ${status?.dionaea ? getStatusColor(status.dionaea.status).border : 'hover:border-gray-500/30'} transition-all duration-300`}>
                    <div className="absolute top-0 right-0 p-4 opacity-10 text-6xl group-hover:scale-110 transition-transform duration-300">🍯</div>
                    <div className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent ${status?.dionaea ? getStatusColor(status.dionaea.status).bg : 'bg-gray-500'}/50 to-transparent opacity-50`}></div>
                    <h3 className="text-xl font-bold mb-2 text-white">Dionaea Node</h3>
                    <p className="text-gray-400 text-sm mb-6">Malware capturing honeypot. Emulates CMB, FTP, HTTP, MSSQL, MySQL, SMB.</p>
                    
                    {statusLoading ? (
                        <div className="flex items-center gap-2">
                            <Loader2 className="w-4 h-4 text-gray-500 animate-spin" />
                            <span className="text-gray-500 font-mono text-xs">Loading...</span>
                        </div>
                    ) : (
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <span className={`w-2 h-2 ${status?.dionaea ? getStatusColor(status.dionaea.status).bg : 'bg-gray-500'} rounded-full ${status?.dionaea?.status === 'running' ? 'animate-pulse' : ''} ${status?.dionaea ? getStatusColor(status.dionaea.status).glow : ''}`}></span>
                                <span className={`${status?.dionaea ? getStatusColor(status.dionaea.status).text : 'text-gray-500'} font-mono text-xs uppercase font-bold tracking-wider`}>
                                    {status?.dionaea?.status || 'Unknown'}
                                </span>
                            </div>
                            <span className="text-gray-600 font-mono text-xs">Port: {status?.dionaea?.port || 'N/A'}</span>
                        </div>
                    )}
                    
                    {/* Stats */}
                    {dionaeaData && (
                        <div className="mt-4 pt-4 border-t border-gray-800">
                            <div className="grid grid-cols-2 gap-4 text-xs">
                                <div>
                                    <span className="text-gray-500">Total Attacks:</span>
                                    <span className="ml-2 text-red-400 font-mono">{dionaeaData.total_attacks || 0}</span>
                                </div>
                                <div>
                                    <span className="text-gray-500">Unique IPs:</span>
                                    <span className="ml-2 text-cyan-400 font-mono">{dionaeaData.unique_ips || 0}</span>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Cowrie Card */}
                <div className={`glass-panel p-6 rounded-xl border border-gray-800 relative overflow-hidden group ${status?.cowrie ? getStatusColor(status.cowrie.status).border : 'hover:border-gray-500/30'} transition-all duration-300`}>
                    <div className="absolute top-0 right-0 p-4 opacity-10 text-6xl group-hover:scale-110 transition-transform duration-300">🐚</div>
                    <div className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent ${status?.cowrie ? getStatusColor(status.cowrie.status).bg : 'bg-gray-500'}/50 to-transparent opacity-50`}></div>
                    <h3 className="text-xl font-bold mb-2 text-white">Cowrie Node</h3>
                    <p className="text-gray-400 text-sm mb-6">Interactive SSH/Telnet honeypot designed to log brute force attacks.</p>
                    
                    {statusLoading ? (
                        <div className="flex items-center gap-2">
                            <Loader2 className="w-4 h-4 text-gray-500 animate-spin" />
                            <span className="text-gray-500 font-mono text-xs">Loading...</span>
                        </div>
                    ) : (
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <span className={`w-2 h-2 ${status?.cowrie ? getStatusColor(status.cowrie.status).bg : 'bg-gray-500'} rounded-full ${status?.cowrie?.status === 'running' ? 'animate-pulse' : ''} ${status?.cowrie ? getStatusColor(status.cowrie.status).glow : ''}`}></span>
                                <span className={`${status?.cowrie ? getStatusColor(status.cowrie.status).text : 'text-gray-500'} font-mono text-xs uppercase font-bold tracking-wider`}>
                                    {status?.cowrie?.status || 'Unknown'}
                                </span>
                            </div>
                            <span className="text-gray-600 font-mono text-xs">Port: {status?.cowrie?.port || 'N/A'}</span>
                        </div>
                    )}
                    
                    {/* Stats */}
                    {cowrieData && (
                        <div className="mt-4 pt-4 border-t border-gray-800">
                            <div className="grid grid-cols-2 gap-4 text-xs">
                                <div>
                                    <span className="text-gray-500">Total Attacks:</span>
                                    <span className="ml-2 text-red-400 font-mono">{cowrieData.total_attacks || 0}</span>
                                </div>
                                <div>
                                    <span className="text-gray-500">Unique IPs:</span>
                                    <span className="ml-2 text-cyan-400 font-mono">{cowrieData.unique_ips || 0}</span>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Analytics Summary */}
            {analytics && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="glass-panel p-4 rounded-xl border border-gray-800">
                        <div className="text-gray-400 text-xs uppercase tracking-wider">Total Attacks</div>
                        <div className="text-2xl font-bold text-red-400 mt-1">{analytics.total_attacks || 0}</div>
                    </div>
                    <div className="glass-panel p-4 rounded-xl border border-gray-800">
                        <div className="text-gray-400 text-xs uppercase tracking-wider">Unique Attackers</div>
                        <div className="text-2xl font-bold text-cyan-400 mt-1">{analytics.unique_attackers || 0}</div>
                    </div>
                    <div className="glass-panel p-4 rounded-xl border border-gray-800">
                        <div className="text-gray-400 text-xs uppercase tracking-wider">Top Attacker</div>
                        <div className="text-lg font-bold text-orange-400 mt-1 font-mono">
                            {analytics.top_attackers?.[0]?.ip || 'N/A'}
                        </div>
                    </div>
                </div>
            )}

            {/* Intrusion Logs Table */}
            <div className="glass-panel rounded-xl border border-gray-800 overflow-hidden">
                <div className="p-4 border-b border-gray-800 bg-gray-900/50">
                    <h3 className="font-bold text-gray-200 flex items-center gap-2">
                        <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                        Intrusion Logs
                    </h3>
                </div>

                {isLoading ? (
                    <div className="flex items-center justify-center p-8">
                        <Loader2 className="w-6 h-6 text-cyan-400 animate-spin" />
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-gray-900/50 text-gray-400 uppercase tracking-wider text-xs font-semibold">
                                <tr>
                                    <th className="p-4">Timestamp</th>
                                    <th className="p-4">Detector</th>
                                    <th className="p-4">Attacker IP</th>
                                    <th className="p-4">Target Port</th>
                                    <th className="p-4">Details</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-800/50">
                                {logs.map((log: any) => (
                                    <tr key={log.id} className="hover:bg-red-900/5 transition-colors font-mono text-xs group">
                                        <td className="p-4 text-gray-500">
                                            {log.timestamp ? new Date(log.timestamp).toLocaleString() : 'N/A'}
                                        </td>
                                        <td className="p-4">
                                            <span className={`px-2 py-1 rounded text-xs font-bold uppercase ${
                                                log.honeypot_type === 'dionaea' 
                                                    ? 'bg-orange-900/30 text-orange-400' 
                                                    : 'bg-blue-900/30 text-blue-400'
                                            }`}>
                                                {log.honeypot_type}
                                            </span>
                                        </td>
                                        <td className="p-4 text-red-400 bg-red-900/10 rounded">{log.source_ip || 'N/A'}</td>
                                        <td className="p-4 text-gray-400">{log.destination_port || 'N/A'}</td>
                                        <td className="p-4">
                                            {log.credentials && (
                                                <span className="text-yellow-400 text-xs">
                                                    {log.credentials}
                                                </span>
                                            )}
                                        </td>
                                    </tr>
                                ))}
                                {logs.length === 0 && (
                                    <tr>
                                        <td colSpan={5} className="p-12 text-center">
                                            <p className="text-gray-500">No intrusion attempts detected yet.</p>
                                            <p className="text-gray-600 text-xs mt-2">Attacks on your honeypots will appear here in real-time.</p>
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}
