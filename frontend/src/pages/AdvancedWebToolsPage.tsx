import { useState, useEffect } from 'react';
import { Globe, Shield, Key, Search, AlertTriangle, Loader2, ScrollText, Terminal } from 'lucide-react';
import { useWebToolsScan, useJWTAnalysis, useWfuzz } from '../hooks/useAdvancedTools';
import { useLogs } from '../hooks/useLogs';
import Badge from '../components/ui/Badge';
import LogConsole from '../components/ui/LogConsole';

interface ScanResult {
  target?: string;
  executive_summary?: string;
  scans?: Record<string, any>;
  final_report?: string;
  [key: string]: any;
}

interface JWTResult {
  analysis?: {
    header?: Record<string, any>;
    payload?: Record<string, any>;
    issues?: string[];
  };
  [key: string]: any;
}

interface FuzzResult {
  [key: string]: any;
}

const AdvancedWebToolsPage = () => {
  const [targetUrl, setTargetUrl] = useState('');
  const [scanType, setScanType] = useState('full');
  const [jwtToken, setJwtToken] = useState('');
  const [activeTab, setActiveTab] = useState<'scan' | 'jwt' | 'fuzz'>('scan');
  const [error, setError] = useState<string | null>(null);
  const [showRawData, setShowRawData] = useState(false);

  const { logs, isLogOpen, addInfo, addSuccess, addWarning, addError, clearLogs, openLogs, closeLogs } = useLogs();

  const { mutate: runScan, data: scanResultsData, isPending: isScanning, error: scanError } = useWebToolsScan();
  const { mutate: analyzeJWT, data: jwtResultsData, isPending: isAnalyzing, error: jwtError } = useJWTAnalysis();
  const { mutate: runFuzz, data: fuzzResultsData, isPending: isFuzzing, error: fuzzError } = useWfuzz();

  const scanResults = scanResultsData as ScanResult | undefined;
  const jwtResults = jwtResultsData as JWTResult | undefined;
  const fuzzResults = fuzzResultsData as FuzzResult | undefined;

  // Log errors for debugging
  useEffect(() => {
    if (scanError) {
      console.error('[AdvancedWebToolsPage] Scan error:', scanError);
      addError(`Scan failed: ${scanError.message || 'Unknown error'}`);
    }
  }, [scanError, addError]);

  useEffect(() => {
    if (jwtError) {
      console.error('[AdvancedWebToolsPage] JWT error:', jwtError);
      addError(`JWT analysis failed: ${jwtError.message || 'Unknown error'}`);
    }
  }, [jwtError, addError]);

  useEffect(() => {
    if (fuzzError) {
      console.error('[AdvancedWebToolsPage] Fuzz error:', fuzzError);
      addError(`Fuzzing failed: ${fuzzError.message || 'Unknown error'}`);
    }
  }, [fuzzError, addError]);

  // Log scan results when they arrive
  useEffect(() => {
    if (scanResults) {
      addSuccess('Web scan completed successfully!');
      
      if (scanResults.target) {
        addInfo(`Target scanned: ${scanResults.target}`);
      }
      
      if (scanResults.executive_summary) {
        addSuccess('Executive summary received');
      }
      
      if (scanResults.final_report) {
        addSuccess('Final security report received');
      }
      
      if (scanResults.scans) {
        const scanKeys = Object.keys(scanResults.scans);
        addInfo(`Individual scan results: ${scanKeys.join(', ')}`);
      }
      
      // Log any other keys found
      const knownKeys = ['target', 'executive_summary', 'final_report', 'scans'];
      const otherKeys = Object.keys(scanResults).filter(k => !knownKeys.includes(k));
      if (otherKeys.length > 0) {
        addInfo(`Additional data keys: ${otherKeys.join(', ')}`);
      }
    }
  }, [scanResults, addInfo, addSuccess]);

  // Log JWT results when they arrive
  useEffect(() => {
    if (jwtResults) {
      addSuccess('JWT analysis completed!');
      
      if (jwtResults.analysis) {
        addInfo('JWT structure parsed successfully');
        if (jwtResults.analysis.header) {
          addInfo('JWT header decoded');
        }
        if (jwtResults.analysis.payload) {
          addInfo('JWT payload decoded');
        }
        if (jwtResults.analysis.issues && jwtResults.analysis.issues.length > 0) {
          addWarning(`Found ${jwtResults.analysis.issues.length} security issues`);
          jwtResults.analysis.issues.forEach((issue, idx) => {
            addWarning(`Issue ${idx + 1}: ${issue}`);
          });
        } else {
          addSuccess('No security issues found in JWT');
        }
      } else {
        addWarning('JWT analysis data not in expected format');
        addInfo(`Available keys: ${Object.keys(jwtResults).join(', ')}`);
      }
    }
  }, [jwtResults, addInfo, addSuccess, addWarning]);

  // Log fuzz results when they arrive
  useEffect(() => {
    if (fuzzResults) {
      addSuccess('Fuzzing completed!');
      addInfo(`Result keys: ${Object.keys(fuzzResults).join(', ')}`);
    }
  }, [fuzzResults, addInfo, addSuccess]);

  const handleScan = () => {
    setError(null);
    clearLogs();
    openLogs();
    addInfo(`Starting web scan for: ${targetUrl}`);
    addInfo(`Scan type: ${scanType}`);
    
    runScan({ target_url: targetUrl, scan_type: scanType }, {
      onSuccess: (data) => console.log('[AdvancedWebToolsPage] Scan success:', data),
      onError: (err: any) => {
        const errorMsg = err?.response?.data?.detail || err?.message || 'Scan failed';
        setError(errorMsg);
        addError(`Scan error: ${errorMsg}`);
      }
    });
  };

  const handleJWT = () => {
    setError(null);
    clearLogs();
    openLogs();
    addInfo('Starting JWT token analysis');
    
    analyzeJWT({ token: jwtToken, crack: false }, {
      onSuccess: (data) => console.log('[AdvancedWebToolsPage] JWT analysis success:', data),
      onError: (err: any) => {
        const errorMsg = err?.response?.data?.detail || err?.message || 'JWT analysis failed';
        setError(errorMsg);
        addError(`JWT analysis error: ${errorMsg}`);
      }
    });
  };

  const handleFuzz = () => {
    setError(null);
    clearLogs();
    openLogs();
    addInfo(`Starting web fuzzing for: ${targetUrl}`);
    
    runFuzz({ target_url: targetUrl }, {
      onSuccess: (data) => console.log('[AdvancedWebToolsPage] Fuzz success:', data),
      onError: (err: any) => {
        const errorMsg = err?.response?.data?.detail || err?.message || 'Fuzzing failed';
        setError(errorMsg);
        addError(`Fuzzing error: ${errorMsg}`);
      }
    });
  };

  // Helper to render scan results
  const renderScanResults = () => {
    if (!scanResults) return null;

    const hasContent = scanResults.executive_summary || scanResults.final_report || 
      (scanResults.scans && Object.keys(scanResults.scans).length > 0);

    return (
      <div className="mt-4 space-y-4">
        {/* Toggle for raw data view */}
        <div className="flex justify-end">
          <button
            onClick={() => setShowRawData(!showRawData)}
            className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1"
          >
            <ScrollText className="w-3 h-3" />
            {showRawData ? 'Hide Raw Data' : 'Show Raw Data'}
          </button>
        </div>

        {/* Raw data view */}
        {showRawData && (
          <div className="p-4 bg-gray-800/50 rounded-lg">
            <p className="text-xs text-gray-400 mb-2">Debug - Full Response:</p>
            <pre className="text-xs text-gray-500 overflow-x-auto">{JSON.stringify(scanResults, null, 2)}</pre>
          </div>
        )}

        {/* Target info */}
        {scanResults.target && (
          <div className="p-3 bg-blue-500/10 rounded-lg border border-blue-500/30">
            <p className="text-sm text-blue-400 flex items-center gap-2">
              <Globe className="w-4 h-4" />
              Target: <span className="text-white font-mono">{scanResults.target}</span>
            </p>
          </div>
        )}

        {/* Executive Summary */}
        {scanResults.executive_summary && (
          <div className="p-4 bg-cyan-600/20 rounded-lg border border-cyan-500/30">
            <h4 className="text-sm font-semibold text-cyan-300 mb-2 flex items-center gap-2">
              <Shield className="w-4 h-4" />
              AI Executive Summary
            </h4>
            <pre className="text-gray-200 text-sm whitespace-pre-wrap">{scanResults.executive_summary}</pre>
          </div>
        )}

        {/* Final Report */}
        {scanResults.final_report && (
          <div className="p-4 bg-purple-600/20 rounded-lg border border-purple-500/30">
            <h4 className="text-sm font-semibold text-purple-300 mb-2 flex items-center gap-2">
              <Terminal className="w-4 h-4" />
              AI Security Assessment
            </h4>
            <pre className="text-gray-200 text-sm whitespace-pre-wrap">{scanResults.final_report}</pre>
          </div>
        )}

        {/* Individual Scans */}
        {scanResults.scans && Object.entries(scanResults.scans).map(([key, value]: [string, any]) => (
          <div key={key} className="p-4 bg-gray-800/50 rounded-lg border border-gray-700">
            <h4 className="text-sm font-semibold text-white mb-2 flex items-center gap-2">
              <Search className="w-4 h-4 text-cyan-400" />
              {key.toUpperCase()} Scan Results
            </h4>
            <pre className="text-gray-300 text-xs overflow-x-auto">{JSON.stringify(value, null, 2)}</pre>
          </div>
        ))}

        {/* Handle any other direct properties */}
        {Object.entries(scanResults)
          .filter(([key]) => !['target', 'executive_summary', 'final_report', 'scans'].includes(key))
          .map(([key, value]: [string, any]) => (
            <div key={key} className="p-4 bg-gray-800/50 rounded-lg border border-gray-700">
              <h4 className="text-sm font-semibold text-white mb-2">{key.toUpperCase()}</h4>
              <pre className="text-gray-300 text-xs overflow-x-auto">{typeof value === 'string' ? value : JSON.stringify(value, null, 2)}</pre>
            </div>
          ))}

        {/* No data found */}
        {!hasContent && (
          <div className="p-4 bg-yellow-500/10 rounded-lg border border-yellow-500/30">
            <h4 className="text-sm font-semibold text-yellow-400 mb-2 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" />
              No Scan Results Found
            </h4>
            <p className="text-gray-300 text-sm">The scan completed but no results were returned in the expected format.</p>
            <p className="text-xs text-gray-500 mt-2">Available keys: {Object.keys(scanResults).join(', ')}</p>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white flex items-center gap-3">
        <Globe className="w-6 h-6 text-cyan-400" />
        Advanced Web Security Tools
      </h1>

      <div className="flex gap-2">
        {['scan', 'jwt', 'fuzz'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab as any)}
            className={`px-4 py-2 rounded-lg ${activeTab === tab ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/50' : 'bg-gray-800/50 text-gray-400'}`}
          >
            {tab.toUpperCase()}
          </button>
        ))}
      </div>

      {activeTab === 'scan' && (
        <div className="glass-panel p-6 space-y-4">
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Search className="w-5 h-5" />
            Web Application Scanner
          </h3>
          
          <input
            type="text"
            value={targetUrl}
            onChange={(e) => setTargetUrl(e.target.value)}
            placeholder="https://target.com"
            className="input-field"
          />
          
          <select value={scanType} onChange={(e) => setScanType(e.target.value)} className="input-field">
            <option value="full">Full Assessment</option>
            <option value="zap">OWASP ZAP Scan</option>
            <option value="nosql">NoSQL Injection</option>
            <option value="xss">XSS Testing</option>
            <option value="ssrf">SSRF Testing</option>
          </select>

          <button onClick={handleScan} disabled={!targetUrl || isScanning} className="btn-primary w-full">
            {isScanning ? <><Loader2 className="w-4 h-4 animate-spin" />Scanning...</> : 'Start Scan'}
          </button>

          {error && activeTab === 'scan' && (
            <div className="p-4 bg-red-600/20 border border-red-500/50 rounded-lg">
              <p className="text-red-300 text-sm flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                Error: {error}
              </p>
            </div>
          )}

          {/* Real-time Log Console */}
          <LogConsole 
            logs={logs} 
            isOpen={isLogOpen} 
            onClose={closeLogs}
            title="Web Scan Logs"
          />

          {renderScanResults()}
        </div>
      )}

      {activeTab === 'jwt' && (
        <div className="glass-panel p-6 space-y-4">
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Key className="w-5 h-5" />
            JWT Token Analyzer
          </h3>
          
          <textarea
            value={jwtToken}
            onChange={(e) => setJwtToken(e.target.value)}
            placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            className="input-field h-32 resize-none font-mono text-sm"
          />

          <button onClick={handleJWT} disabled={!jwtToken || isAnalyzing} className="btn-primary w-full">
            {isAnalyzing ? <><Loader2 className="w-4 h-4 animate-spin" />Analyzing...</> : 'Analyze JWT'}
          </button>

          {error && activeTab === 'jwt' && (
            <div className="p-4 bg-red-600/20 border border-red-500/50 rounded-lg">
              <p className="text-red-300 text-sm flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                Error: {error}
              </p>
            </div>
          )}

          {/* Real-time Log Console */}
          <LogConsole 
            logs={logs} 
            isOpen={isLogOpen} 
            onClose={closeLogs}
            title="JWT Analysis Logs"
          />

          {jwtResults && (
            <div className="mt-4 space-y-3">
              {/* Toggle for raw data view */}
              <div className="flex justify-end">
                <button
                  onClick={() => setShowRawData(!showRawData)}
                  className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1"
                >
                  <ScrollText className="w-3 h-3" />
                  {showRawData ? 'Hide Raw Data' : 'Show Raw Data'}
                </button>
              </div>

              {/* Raw data view */}
              {showRawData && (
                <div className="p-3 bg-gray-800/50 rounded-lg">
                  <p className="text-xs text-gray-400 mb-2">Debug - Full Response:</p>
                  <pre className="text-xs text-gray-500 overflow-x-auto">{JSON.stringify(jwtResults, null, 2)}</pre>
                </div>
              )}

              {/* Structured JWT data */}
              {jwtResults.analysis ? (
                <div className="space-y-3">
                  <div className="p-3 bg-gray-800/50 rounded-lg border border-gray-700">
                    <p className="text-xs text-gray-400 mb-1">Header:</p>
                    <pre className="text-green-400 text-xs">{JSON.stringify(jwtResults.analysis.header, null, 2)}</pre>
                  </div>
                  <div className="p-3 bg-gray-800/50 rounded-lg border border-gray-700">
                    <p className="text-xs text-gray-400 mb-1">Payload:</p>
                    <pre className="text-cyan-400 text-xs">{JSON.stringify(jwtResults.analysis.payload, null, 2)}</pre>
                  </div>
                  {jwtResults.analysis.issues && jwtResults.analysis.issues.length > 0 && (
                    <div className="p-3 bg-red-600/20 rounded-lg border border-red-500/30">
                      <p className="text-xs text-red-300 mb-1 flex items-center gap-1">
                        <AlertTriangle className="w-3 h-3" />Security Issues Found:
                      </p>
                      <ul className="list-disc list-inside text-gray-200 text-xs">
                        {jwtResults.analysis.issues.map((issue: string, idx: number) => <li key={idx}>{issue}</li>)}
                      </ul>
                    </div>
                  )}
                  {jwtResults.analysis.issues && jwtResults.analysis.issues.length === 0 && (
                    <div className="p-3 bg-green-600/20 rounded-lg border border-green-500/30">
                      <p className="text-xs text-green-300 flex items-center gap-1">
                        <Shield className="w-3 h-3" />
                        No security issues detected
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="p-3 bg-yellow-500/10 rounded-lg border border-yellow-500/30">
                  <p className="text-yellow-400 text-sm">JWT analysis data not in expected format</p>
                  <p className="text-gray-500 text-xs mt-1">Available keys: {Object.keys(jwtResults).join(', ')}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {activeTab === 'fuzz' && (
        <div className="glass-panel p-6 space-y-4">
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Terminal className="w-5 h-5" />
            Web Fuzzing (Wfuzz)
          </h3>
          <input
            type="text"
            value={targetUrl}
            onChange={(e) => setTargetUrl(e.target.value)}
            placeholder="https://target.com/FUZZ"
            className="input-field"
          />
          <button onClick={handleFuzz} disabled={!targetUrl || isFuzzing} className="btn-primary w-full">
            {isFuzzing ? <><Loader2 className="w-4 h-4 animate-spin" />Fuzzing...</> : 'Start Fuzzing'}
          </button>

          {error && activeTab === 'fuzz' && (
            <div className="p-4 bg-red-600/20 border border-red-500/50 rounded-lg">
              <p className="text-red-300 text-sm flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                Error: {error}
              </p>
            </div>
          )}

          {/* Real-time Log Console */}
          <LogConsole 
            logs={logs} 
            isOpen={isLogOpen} 
            onClose={closeLogs}
            title="Fuzzing Logs"
          />

          {fuzzResults && (
            <div className="mt-4 space-y-4">
              {/* Toggle for raw data view */}
              <div className="flex justify-end">
                <button
                  onClick={() => setShowRawData(!showRawData)}
                  className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1"
                >
                  <ScrollText className="w-3 h-3" />
                  {showRawData ? 'Hide Raw Data' : 'Show Raw Data'}
                </button>
              </div>

              {/* Raw data view */}
              {showRawData && (
                <div className="p-4 bg-gray-800/50 rounded-lg">
                  <p className="text-xs text-gray-400 mb-2">Debug - Full Response:</p>
                  <pre className="text-xs text-gray-500 overflow-x-auto">{JSON.stringify(fuzzResults, null, 2)}</pre>
                </div>
              )}

              <div className="p-4 bg-gray-800/50 rounded-lg border border-gray-700">
                <h4 className="text-sm font-semibold text-white mb-2">Fuzzing Results</h4>
                <pre className="text-gray-300 text-xs overflow-x-auto">{JSON.stringify(fuzzResults, null, 2)}</pre>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AdvancedWebToolsPage;
