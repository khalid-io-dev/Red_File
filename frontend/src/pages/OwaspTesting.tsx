import { useState, useEffect } from 'react';
import api from '../services/api';
import axios from 'axios';

interface Log {
    message: string;
    type: string;
    timestamp: number | string;
}

interface Vulnerability {
    title: string;
    severity: string;
    description: string;
    payload?: string;
    location?: string;
    credentials?: string;
    impact?: string;
    exploitation?: string;
    evidence?: string;
    remediation?: string;
}

export default function OwaspTesting() {
    const [targetUrl, setTargetUrl] = useState('');
    const [testing, setTesting] = useState(false);
    const [logs, setLogs] = useState<Log[]>([]);
    const [vulnerabilities, setVulnerabilities] = useState<Vulnerability[]>([]);
    const [testComplete, setTestComplete] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [progress, setProgress] = useState(0);
    const [currentTest, setCurrentTest] = useState('');
    const [report, setReport] = useState('');
    const [modelUsed, setModelUsed] = useState('');

    const runTest = async () => {
        if (!targetUrl) {
            setError('Please enter a target URL');
            return;
        }

        // Validate URL format
        try {
            new URL(targetUrl.startsWith('http') ? targetUrl : `https://${targetUrl}`);
        } catch {
            setError('Please enter a valid URL (e.g., https://example.com)');
            return;
        }

        setTesting(true);
        setLogs([]);
        setVulnerabilities([]);
        setTestComplete(false);
        setError(null);
        setProgress(0);
        setCurrentTest('Initializing...');
        setReport('');

        // Initial log
        const initialLogs = [
            { message: `🎯 Starting OWASP Top 10 tests on ${targetUrl}`, type: 'start', timestamp: Date.now() },
            { message: `🤖 Using AI-powered vulnerability scanning`, type: 'info', timestamp: Date.now() },
            { message: '═'.repeat(50), type: 'separator', timestamp: Date.now() },
        ];
        
        setLogs(initialLogs);

        // Simulate progress updates for better UX
        const progressInterval = setInterval(() => {
            setProgress(prev => {
                if (prev >= 90) {
                    clearInterval(progressInterval);
                    return prev;
                }
                return prev + 5;
            });
        }, 1000);

        try {
            // Call the OWASP test endpoint
            const res = await api.post('/pentest/owasp-test', 
                { 
                    target: targetUrl.startsWith('http') ? targetUrl : `https://${targetUrl}`,
                    use_llm: true,
                    model: 'qwen2.5:1.8b'  // Smaller model that fits in limited memory
                },
                { timeout: 300000 } // 5 minute timeout for AI scanning
            );
            
            clearInterval(progressInterval);
            setProgress(100);
            
            // Set response data
            setLogs(res.data.logs || []);
            setVulnerabilities(res.data.results || []);
            setReport(res.data.report || '');
            setModelUsed(res.data.model_used || '');
            setTestComplete(true);
            setCurrentTest('Complete');
            
        } catch (e: any) {
            clearInterval(progressInterval);
            setProgress(0);
            
            let errorMessage = 'An unexpected error occurred';
            
            // Handle different error types
            if (axios.isAxiosError(e)) {
                if (e.code === 'ECONNABORTED') {
                    errorMessage = 'Request timed out. The scan took too long. Try a simpler target.';
                } else if (!e.response) {
                    errorMessage = 'Network error. Check if backend is running at http://localhost:8000';
                } else if (e.response?.status === 401) {
                    errorMessage = 'Authentication required. Please login first.';
                } else {
                    errorMessage = e.response?.data?.detail || e.message;
                }
            } else if (e instanceof Error) {
                errorMessage = e.message;
            } else {
                errorMessage = String(e);
            }
            
            setError(errorMessage);
            
            setLogs([...initialLogs, { 
                message: `❌ Error: ${errorMessage}`, 
                type: 'error', 
                timestamp: Date.now() 
            }]);
        } finally {
            setTesting(false);
        }
    };

    const handleRetry = () => {
        setError(null);
        runTest();
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

    const getSeverityColor = (severity: string) => {
        const colors: any = {
            'CRITICAL': 'text-red-500 bg-red-900/20 border-red-500',
            'HIGH': 'text-orange-500 bg-orange-900/20 border-orange-500',
            'MEDIUM': 'text-yellow-500 bg-yellow-900/20 border-yellow-500',
            'LOW': 'text-blue-500 bg-blue-900/20 border-blue-500',
        };
        return colors[severity] || colors.MEDIUM;
    };

    return (
        <div className="space-y-6 animate-fade-in">
            <div>
                <h2 className="text-3xl font-bold text-white mb-2">🤖 AI-Powered OWASP Testing</h2>
                <p className="text-gray-400">Comprehensive vulnerability assessment using local LLM + Kali tools</p>
            </div>

            {/* Error Display */}
            {error && (
                <div className="glass-panel p-4 rounded-xl border border-red-500/50 bg-red-900/20">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <span className="text-red-400 text-xl">⚠️</span>
                            <div>
                                <div className="text-red-400 font-bold">Error</div>
                                <div className="text-red-300 text-sm">{error}</div>
                            </div>
                        </div>
                        <button
                            onClick={handleRetry}
                            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                        >
                            Retry
                        </button>
                    </div>
                </div>
            )}

            {/* Progress Display */}
            {testing && (
                <div className="glass-panel p-6 rounded-xl">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-white font-bold flex items-center gap-2">
                            <span className="animate-pulse">🔄</span>
                            {currentTest || 'Scanning...'}
                        </span>
                        <span className="text-cyan-400 font-mono">{progress}%</span>
                    </div>
                    <div className="w-full bg-gray-800 rounded-full h-3 overflow-hidden">
                        <div 
                            className="bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 h-3 rounded-full transition-all duration-500"
                            style={{ width: `${progress}%` }}
                        />
                    </div>
                    <div className="mt-2 text-xs text-gray-500">
                        Using Ollama LLM for intelligent vulnerability analysis
                    </div>
                </div>
            )}

            <div className="glass-panel p-6 rounded-xl">
                <div className="flex gap-4">
                    <input
                        type="text"
                        value={targetUrl}
                        onChange={(e) => setTargetUrl(e.target.value)}
                        placeholder="jobdating.youcode.ma or https://example.com"
                        className="flex-1 px-4 py-3 bg-gray-950 border border-gray-800 rounded-lg text-white focus:outline-none focus:border-cyan-500"
                        disabled={testing}
                    />
                    <button
                        onClick={runTest}
                        disabled={testing}
                        className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all font-bold"
                    >
                        {testing ? '⏳ Scanning...' : '🚀 Start Scan'}
                    </button>
                </div>

                <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                    <div className="bg-gray-950 p-3 rounded border border-gray-800">
                        <div className="text-gray-500 text-xs">AI Model</div>
                        <div className="text-cyan-400 font-bold text-xs">Qwen2.5-1.8B</div>
                    </div>
                    <div className="bg-gray-950 p-3 rounded border border-gray-800">
                        <div className="text-gray-500 text-xs">Test Coverage</div>
                        <div className="text-white font-bold">OWASP Top 10</div>
                    </div>
                    <div className="bg-gray-950 p-3 rounded border border-gray-800">
                        <div className="text-gray-500 text-xs">Scanner</div>
                        <div className="text-white font-bold">Kali + AI</div>
                    </div>
                    <div className="bg-gray-950 p-3 rounded border border-gray-800">
                        <div className="text-gray-500 text-xs">Mode</div>
                        <div className="text-green-400 font-bold">Intelligent</div>
                    </div>
                </div>
            </div>

            {logs.length > 0 && (
                <div className="glass-panel p-6 rounded-xl">
                    <h3 className="text-xl font-bold text-white mb-4">🖥️ Terminal Output</h3>
                    <div className="bg-black rounded-lg p-4 font-mono text-sm max-h-96 overflow-y-auto border border-gray-800">
                        {logs.map((log, idx) => (
                            <div key={idx} className={`${getLogColor(log.type)} mb-1`}>
                                {log.message}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {report && (
                <div className="glass-panel p-6 rounded-xl">
                    <h3 className="text-xl font-bold text-white mb-4">📋 AI Security Report</h3>
                    <div className="bg-gray-950 p-4 rounded-lg border border-gray-800 overflow-auto max-h-[500px]">
                        <pre className="text-green-400 text-sm font-mono whitespace-pre-wrap">{report}</pre>
                    </div>
                </div>
            )}

            {testComplete && vulnerabilities.length > 0 && (
                <div className="glass-panel p-6 rounded-xl">
                    <h3 className="text-xl font-bold text-white mb-4">🚨 Vulnerabilities Found ({vulnerabilities.length})</h3>
                    <div className="space-y-4">
                        {vulnerabilities.map((vuln, idx) => (
                            <div key={idx} className="bg-gray-950 p-4 rounded-lg border border-gray-800">
                                <div className="flex items-start justify-between mb-3">
                                    <h4 className="text-white font-bold text-lg">{vuln.title}</h4>
                                    <span className={`px-3 py-1 rounded text-xs border ${getSeverityColor(vuln.severity)}`}>
                                        {vuln.severity}
                                    </span>
                                </div>
                                
                                <div className="space-y-2 text-sm">
                                    {vuln.description && (
                                    <div>
                                        <span className="text-gray-500">Description:</span>
                                        <p className="text-gray-300 mt-1">{vuln.description}</p>
                                    </div>
                                    )}
                                    
                                    {vuln.evidence && (
                                        <div className="bg-yellow-900/20 border border-yellow-900/50 rounded p-3 mt-2">
                                            <span className="text-yellow-400 font-bold text-xs uppercase">Evidence:</span>
                                            <p className="text-yellow-300 mt-1 text-sm font-mono">{vuln.evidence}</p>
                                        </div>
                                    )}
                                    
                                    {vuln.remediation && (
                                        <div className="bg-green-900/20 border border-green-900/50 rounded p-3 mt-2">
                                            <span className="text-green-400 font-bold text-xs uppercase">Remediation:</span>
                                            <p className="text-green-300 mt-1 text-sm">{vuln.remediation}</p>
                                        </div>
                                    )}
                                    
                                    {vuln.impact && (
                                        <div className="bg-red-950/30 border border-red-900/50 rounded p-3 mt-2">
                                            <span className="text-red-400 font-bold text-xs uppercase">Impact:</span>
                                            <p className="text-red-300 mt-1 text-sm">{vuln.impact}</p>
                                        </div>
                                    )}
                                    
                                    {vuln.exploitation && (
                                        <div className="bg-orange-950/30 border border-orange-900/50 rounded p-3 mt-2">
                                            <span className="text-orange-400 font-bold text-xs uppercase">💥 How to Exploit:</span>
                                            <p className="text-orange-200 mt-1 text-sm">{vuln.exploitation}</p>
                                        </div>
                                    )}
                                    
                                    {vuln.location && (
                                        <div>
                                            <span className="text-gray-500">Location:</span>
                                            <p className="text-cyan-400 mt-1 font-mono">{vuln.location}</p>
                                        </div>
                                    )}
                                    
                                    {vuln.payload && (
                                        <div>
                                            <span className="text-gray-500">Payload:</span>
                                            <p className="text-yellow-400 mt-1 font-mono bg-gray-900 p-2 rounded">{vuln.payload}</p>
                                        </div>
                                    )}
                                    
                                    {vuln.credentials && (
                                        <div>
                                            <span className="text-gray-500">Credentials:</span>
                                            <p className="text-red-400 mt-1 font-mono bg-gray-900 p-2 rounded">{vuln.credentials}</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {testComplete && vulnerabilities.length === 0 && (
                <div className="glass-panel p-6 rounded-xl">
                    <div className="text-center py-8">
                        <div className="text-6xl mb-4">✅</div>
                        <h3 className="text-2xl font-bold text-green-400 mb-2">No Vulnerabilities Found</h3>
                        <p className="text-gray-400">The target passed all OWASP Top 10 tests</p>
                    </div>
                </div>
            )}

            <div className="glass-panel p-6 rounded-xl">
                <h3 className="text-lg font-bold text-white mb-4">🛠️ AI-Powered Testing Capabilities</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                    {[
                        '🤖 LLM-Based Vulnerability Analysis',
                        '🔍 Nmap Reconnaissance',
                        '💉 SQL Injection Testing (SQLMap)',
                        '⚡ XSS Testing (Nikto)',
                        '🔐 Authentication Testing',
                        '📊 Security Misconfiguration Checks',
                        '🌐 Web Application Scanning',
                        '📝 AI-Generated Reports'
                    ].map((test, idx) => (
                        <div key={idx} className="bg-gray-950 p-3 rounded border border-gray-800 text-gray-300">
                            {test}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
