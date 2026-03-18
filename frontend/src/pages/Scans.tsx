import { useEffect, useState } from 'react';
import api from '../services/api';
import NewScan from './NewScan';

interface Scan {
    id: number;
    target_url: string;
    scan_type: string;
    status: string;
    created_at: string;
}

export default function Scans() {
    const [scans, setScans] = useState<Scan[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchScans = async () => {
        try {
            const response = await api.get('/scans/');
            setScans(response.data);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchScans();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-3xl font-bold text-white tracking-tight">Active Operations</h2>
                    <p className="text-gray-400 text-sm mt-1">Manage and monitor running reconnaissance tasks</p>
                </div>
                <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse"></span>
                    <span className="text-cyan-500 text-xs font-mono uppercase tracking-wider">System Online</span>
                </div>
            </div>

            <div className="glass-panel p-6 rounded-xl border border-gray-800">
                <NewScan />
            </div>

            <div className="glass-panel rounded-xl border border-gray-800 overflow-hidden">
                <div className="p-4 border-b border-gray-800 flex items-center justify-between bg-gray-900/50">
                    <h3 className="font-bold text-gray-200 flex items-center gap-2">
                        <svg className="w-5 h-5 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
                        Scan History
                    </h3>
                    <button onClick={fetchScans} className="text-xs text-cyan-500 hover:text-cyan-400 uppercase font-bold tracking-wider flex items-center gap-1">
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                        Refresh
                    </button>
                </div>

                {loading ? (
                    <div className="p-8 text-center text-gray-500 animate-pulse">Loading scan data...</div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-gray-900/50 text-gray-400 uppercase tracking-wider text-xs font-semibold">
                                <tr>
                                    <th className="p-4">Target ID</th>
                                    <th className="p-4">Target URL</th>
                                    <th className="p-4">Scan Type</th>
                                    <th className="p-4">Status</th>
                                    <th className="p-4">Timestamp</th>
                                    <th className="p-4 text-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-800/50">
                                {scans.map(scan => (
                                    <tr key={scan.id} className="hover:bg-cyan-900/5 transition-colors group">
                                        <td className="p-4 font-mono text-gray-500">#{scan.id.toString().padStart(4, '0')}</td>
                                        <td className="p-4 font-mono text-gray-300 group-hover:text-cyan-400 transition-colors">{scan.target_url}</td>
                                        <td className="p-4">
                                            <span className="px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wide border border-gray-700 bg-gray-800 text-gray-400">
                                                {scan.scan_type}
                                            </span>
                                        </td>
                                        <td className="p-4">
                                            <StatusBadge status={scan.status} />
                                        </td>
                                        <td className="p-4 text-gray-500 text-xs">
                                            {new Date(scan.created_at).toLocaleString()}
                                        </td>
                                        <td className="p-4 text-right">
                                            <button 
                                                onClick={() => window.location.href = `/scans/${scan.id}`}
                                                className="text-cyan-500 hover:text-white opacity-0 group-hover:opacity-100 transition-all text-xs font-bold uppercase tracking-wider"
                                            >
                                                View Report
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        {scans.length === 0 && (
                            <div className="p-12 text-center">
                                <div className="w-16 h-16 bg-gray-900 rounded-full flex items-center justify-center mx-auto mb-4 text-gray-700">
                                    <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                </div>
                                <p className="text-gray-500">No active scans detected.</p>
                                <p className="text-xs text-gray-600 mt-1">Initiate a new scan to begin reconnaissance.</p>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

const StatusBadge = ({ status }: { status: string }) => {
    const styles: any = {
        COMPLETED: "bg-green-900/20 text-green-400 border-green-900/50 shadow-[0_0_10px_rgba(74,222,128,0.1)]",
        RUNNING: "bg-cyan-900/20 text-cyan-400 border-cyan-900/50 shadow-[0_0_10px_rgba(34,211,238,0.1)] animate-pulse",
        FAILED: "bg-red-900/20 text-red-400 border-red-900/50 shadow-[0_0_10px_rgba(248,113,113,0.1)]",
        PENDING: "bg-yellow-900/20 text-yellow-400 border-yellow-900/50"
    };

    return (
        <span className={`px-2.5 py-1 rounded border text-[10px] font-bold uppercase tracking-wider ${styles[status] || styles.PENDING}`}>
            {status}
        </span>
    );
};
