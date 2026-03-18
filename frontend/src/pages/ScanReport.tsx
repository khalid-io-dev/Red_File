import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';

interface Finding {
    id: number;
    title: string;
    severity: string;
    description: string;
}

interface ExploitLog {
    message: string;
    type: string;
}

interface ExploitResult {
    success: boolean;
    evidence?: string;
    message?: string;
    logs?: ExploitLog[];
}

interface Scan {
    id: number;
    target_url: string;
    scan_type: string;
    status: string;
    created_at: string;
    completed_at: string;
}

export default function ScanReport() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [scan, setScan] = useState<Scan | null>(null);
    const [findings, setFindings] = useState<Finding[]>([]);
    const [loading, setLoading] = useState(true);
    const [exploiting, setExploiting] = useState<number | null>(null);
    const [exploitLogs, setExploitLogs] = useState<ExploitLog[]>([]);
    const [exploitResult, setExploitResult] = useState<ExploitResult | null>(null);
    const [showExploitModal, setShowExploitModal] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [scanRes, findingsRes] = await Promise.all([
                    api.get(`/scans/${id}`),
                    api.get(`/findings/?scan_id=${id}`)
                ]);
                setScan(scanRes.data);
                setFindings(findingsRes.data);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [id]);

    const runExploit = async (findingId: number, findingTitle: string) => {
        setExploiting(findingId);
        setExploitLogs([]);
        setExploitResult(null);
        setShowExploitModal(true);
        
        try {
            const res = await api.post('/pentest/exploit', { 
                target: scan?.target_url, 
                finding_type: findingTitle 
            });
            
            setExploitLogs(res.data.logs || []);
            setExploitResult(res.data);
        } catch (e: any) {
            setExploitLogs([{ message: `❌ Error: ${e.response?.data?.detail || e.message}`, type: 'error' }]);
            setExploitResult({ success: false, message: e.response?.data?.detail || e.message });
        } finally {
            setExploiting(null);
        }
    };

    const getLogColor = (type: string) => {
        const colors: any = {
            'start': 'text-cyan-400',
            'info': 'text-blue-400',
            'success': 'text-green-400',
            'fail': 'text-gray-500',
            'detail': 'text-yellow-300',
            'error': 'text-red-400',
            'separator': 'text-gray-700',
            'complete': 'text-green-500'
        };
        return colors[type] || 'text-gray-400';
    };

    if (loading) return <div className="text-center p-8">Loading...</div>;
    if (!scan) return <div className="text-center p-8">Scan not found</div>;

    const getSeverityColor = (severity: string) => {
        const colors: any = {
            'CRITICAL': 'text-red-500 bg-red-900/20 border-red-500',
            'HIGH': 'text-orange-500 bg-orange-900/20 border-orange-500',
            'MEDIUM': 'text-yellow-500 bg-yellow-900/20 border-yellow-500',
            'LOW': 'text-blue-500 bg-blue-900/20 border-blue-500',
            'INFO': 'text-gray-500 bg-gray-900/20 border-gray-500'
        };
        return colors[severity] || colors.INFO;
    };

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex items-center justify-between">
                <h2 className="text-3xl font-bold text-white">Scan Report #{scan.id}</h2>
                <button onClick={() => navigate('/scans')} className="text-cyan-500 hover:text-cyan-400">
                    ← Back to Scans
                </button>
            </div>

            <div className="glass-panel p-6 rounded-xl">
                <div className="grid grid-cols-2 gap-4 mb-6">
                    <div>
                        <label className="text-xs text-gray-500 uppercase">Target</label>
                        <p className="text-white font-mono">{scan.target_url}</p>
                    </div>
                    <div>
                        <label className="text-xs text-gray-500 uppercase">Type</label>
                        <p className="text-white">{scan.scan_type}</p>
                    </div>
                    <div>
                        <label className="text-xs text-gray-500 uppercase">Status</label>
                        <p className="text-white">{scan.status}</p>
                    </div>
                    <div>
                        <label className="text-xs text-gray-500 uppercase">Completed</label>
                        <p className="text-white">{scan.completed_at ? new Date(scan.completed_at).toLocaleString() : 'N/A'}</p>
                    </div>
                </div>

                <div className="border-t border-gray-800 pt-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-xl font-bold text-white">Findings ({findings.length})</h3>
                    </div>
                    {findings.length === 0 ? (
                        <div className="bg-gray-950 p-4 rounded border border-gray-800">
                            <p className="text-green-400 font-mono text-sm">✓ No vulnerabilities detected</p>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {findings.map((finding) => (
                                <div key={finding.id} className="bg-gray-950 p-4 rounded border border-gray-800">
                                    <div className="flex items-start justify-between mb-2">
                                        <h4 className="text-white font-bold">{finding.title}</h4>
                                        <div className="flex items-center gap-2">
                                            <span className={`px-2 py-1 rounded text-xs border ${getSeverityColor(finding.severity)}`}>
                                                {finding.severity}
                                            </span>
                                            {(finding.severity === 'HIGH' || finding.severity === 'CRITICAL') && (
                                                <button
                                                    onClick={() => runExploit(finding.id, finding.title)}
                                                    disabled={exploiting === finding.id}
                                                    className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                                                >
                                                    {exploiting === finding.id ? '⏳' : '💥 Exploit'}
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                    <p className="text-gray-400 text-sm">{finding.description}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* Exploit Modal */}
            {showExploitModal && (
                <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowExploitModal(false)}>
                    <div className="glass-panel p-6 rounded-xl max-w-4xl w-full max-h-[80vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-2xl font-bold text-white">💥 Exploitation Results</h3>
                            <button onClick={() => setShowExploitModal(false)} className="text-gray-400 hover:text-white text-2xl">
                                ×
                            </button>
                        </div>

                        {/* Terminal Output */}
                        <div className="bg-black rounded-lg p-4 font-mono text-sm mb-4 max-h-96 overflow-y-auto border border-gray-800">
                            {exploitLogs.length === 0 ? (
                                <div className="text-cyan-400">⏳ Running exploit...</div>
                            ) : (
                                exploitLogs.map((log, idx) => (
                                    <div key={idx} className={`${getLogColor(log.type)} mb-1`}>
                                        {log.message}
                                    </div>
                                ))
                            )}
                        </div>

                        {/* Result Summary */}
                        {exploitResult && (
                            <div className={`p-4 rounded-lg border ${
                                exploitResult.success 
                                    ? 'bg-green-950/30 border-green-900/50' 
                                    : 'bg-red-950/30 border-red-900/50'
                            }`}>
                                <div className="flex items-center gap-2 mb-2">
                                    <span className="text-2xl">{exploitResult.success ? '✅' : '❌'}</span>
                                    <h4 className={`font-bold text-lg ${
                                        exploitResult.success ? 'text-green-400' : 'text-red-400'
                                    }`}>
                                        {exploitResult.success ? 'Exploitation Successful!' : 'Exploitation Failed'}
                                    </h4>
                                </div>
                                <p className={exploitResult.success ? 'text-green-300' : 'text-red-300'}>
                                    {exploitResult.evidence || exploitResult.message || 'No additional information'}
                                </p>
                            </div>
                        )}

                        <button
                            onClick={() => setShowExploitModal(false)}
                            className="mt-4 w-full px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg transition-all"
                        >
                            Close
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
