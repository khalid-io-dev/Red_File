import { useAuth } from '../context/AuthContext';
import NewScan from './NewScan';
import { useDashboardStats } from '../hooks/useDashboard';
import { Loader2 } from 'lucide-react';

export default function Dashboard() {
    const { user } = useAuth();
    const { data: stats, isLoading } = useDashboardStats();

    // Default values if stats are loading or failed
    const activeScans = stats?.active_scans || 0;
    const criticalFindings = stats?.critical_findings || 0;
    const honeypotHits = 0; // Not yet in backend stats

    return (
        <div className="space-y-8 animate-fade-in">
            <header>
                <h2 className="text-3xl font-bold text-white mb-2">Operation Center</h2>
                <p className="text-gray-400">Welcome back, {user?.full_name || 'Operator'}</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="glass-panel p-6 rounded-xl border-l-4 border-l-cyan-500 relative overflow-hidden group hover:shadow-[0_0_30px_rgba(8,145,178,0.2)] transition-all duration-300">
                    <div className="absolute right-0 top-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                        <svg className="w-24 h-24" fill="currentColor" viewBox="0 0 20 20"><path d="M10 12a2 2 0 100-4 2 2 0 000 4z"></path><path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd"></path></svg>
                    </div>
                    <h3 className="text-cyan-400/80 text-xs font-bold uppercase tracking-widest mb-2">Active Scans</h3>
                    <div className="flex items-end justify-between relative z-10">
                        <p className="text-4xl font-bold text-white font-mono tracking-tighter">
                            {isLoading ? <Loader2 className="w-8 h-8 animate-spin" /> : activeScans}
                        </p>
                        <span className={`text-xs font-semibold px-2 py-1 rounded border ${activeScans > 0
                                ? 'text-cyan-500 bg-cyan-900/30 border-cyan-500/20 animate-pulse'
                                : 'text-gray-500 bg-gray-900/30 border-gray-500/20'
                            }`}>
                            {activeScans > 0 ? 'Running' : 'Idle'}
                        </span>
                    </div>
                </div>

                <div className="glass-panel p-6 rounded-xl border-l-4 border-l-red-500 relative overflow-hidden group hover:shadow-[0_0_30px_rgba(239,68,68,0.2)] transition-all duration-300">
                    <div className="absolute right-0 top-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                        <svg className="w-24 h-24" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd"></path></svg>
                    </div>
                    <h3 className="text-red-400/80 text-xs font-bold uppercase tracking-widest mb-2">Critical Findings</h3>
                    <div className="flex items-end justify-between relative z-10">
                        <p className="text-4xl font-bold text-white font-mono tracking-tighter">
                            {isLoading ? <Loader2 className="w-8 h-8 animate-spin" /> : criticalFindings}
                        </p>
                        <span className="text-green-500 text-xs font-semibold px-2 py-1 bg-green-900/30 rounded border border-green-500/20">Clear</span>
                    </div>
                </div>

                <div className="glass-panel p-6 rounded-xl border-l-4 border-l-yellow-500 relative overflow-hidden group hover:shadow-[0_0_30px_rgba(234,179,8,0.2)] transition-all duration-300">
                    <div className="absolute right-0 top-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                        <svg className="w-24 h-24" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clipRule="evenodd"></path></svg>
                    </div>
                    <h3 className="text-yellow-400/80 text-xs font-bold uppercase tracking-widest mb-2">Honeypot Hits</h3>
                    <div className="flex items-end justify-between relative z-10">
                        <p className="text-4xl font-bold text-white font-mono tracking-tighter">
                            {isLoading ? <Loader2 className="w-8 h-8 animate-spin" /> : honeypotHits}
                        </p>
                        <span className="text-yellow-500 text-xs font-semibold px-2 py-1 bg-yellow-900/30 rounded border border-yellow-500/20">Last 24h</span>
                    </div>
                </div>
            </div>

            <div className="glass-panel p-6 rounded-xl">
                <h3 className="text-xl font-bold mb-6 text-white border-b border-gray-800 pb-4 flex items-center gap-2">
                    <span className="text-cyan-500">⚡</span> Quick Actions
                </h3>
                <NewScan />
            </div>
        </div>
    );
}

