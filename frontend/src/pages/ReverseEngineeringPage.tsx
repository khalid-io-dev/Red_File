import { useState, useEffect } from 'react';
import { Upload, FileCode, Cpu, Terminal, Loader2, AlertTriangle, ScrollText } from 'lucide-react';
import { useUploadBinary, useRETools } from '../hooks/useAdvancedTools';
import { useLogs } from '../hooks/useLogs';
import Badge from '../components/ui/Badge';
import LogConsole from '../components/ui/LogConsole';

interface AnalysisResult {
  analysis?: {
    final_report?: string;
    analyses?: Record<string, {
      ai_insights?: string;
      output?: string;
    }>;
  };
  // Direct result structure (not nested under analysis)
  final_report?: string;
  analyses?: Record<string, any>;
  file_path?: string;
  [key: string]: any;
}

interface ToolsData {
  tools: string[];
}

const ReverseEngineeringPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [analysisType, setAnalysisType] = useState('full');
  const [error, setError] = useState<string | null>(null);
  const [showRawData, setShowRawData] = useState(false);

  const { logs, isLogOpen, addInfo, addSuccess, addWarning, addError, clearLogs, openLogs, closeLogs } = useLogs();
  
  const { mutate: uploadBinary, data: results, isPending: isUploading, error: mutationError } = useUploadBinary();
  const { data: toolsData, error: toolsError } = useRETools();
  const tools = toolsData as ToolsData | undefined;
  const analysisResults = results as AnalysisResult | undefined;

  // Log errors for debugging
  useEffect(() => {
    if (mutationError) {
      console.error('[ReverseEngineeringPage] Mutation error:', mutationError);
      addError(`Upload failed: ${mutationError.message || 'Unknown error'}`);
    }
  }, [mutationError, addError]);

  useEffect(() => {
    if (toolsError) {
      console.error('[ReverseEngineeringPage] Tools fetch error:', toolsError);
      addWarning(`Failed to fetch tools: ${toolsError.message || 'Unknown error'}`);
    }
  }, [toolsError, addWarning]);

  // Log analysis results when they arrive
  useEffect(() => {
    if (analysisResults) {
      addSuccess('Analysis completed successfully!');
      
      if (analysisResults.file_path) {
        addInfo(`File saved to: ${analysisResults.file_path}`);
      }
      
      // Check what data we received
      if (analysisResults.analysis) {
        addInfo('Analysis data structure: nested under "analysis" key');
        if (analysisResults.analysis.final_report) {
          addSuccess('AI Security Assessment report received');
        }
        if (analysisResults.analysis.analyses) {
          const analysisKeys = Object.keys(analysisResults.analysis.analyses);
          addInfo(`Individual analyses received: ${analysisKeys.join(', ')}`);
        }
      } else if (analysisResults.final_report || analysisResults.analyses) {
        addInfo('Analysis data structure: direct (not nested)');
        if (analysisResults.final_report) {
          addSuccess('AI Security Assessment report received');
        }
        if (analysisResults.analyses) {
          const analysisKeys = Object.keys(analysisResults.analyses);
          addInfo(`Individual analyses received: ${analysisKeys.join(', ')}`);
        }
      } else {
        addWarning('No recognizable analysis data structure found');
        addInfo(`Available keys: ${Object.keys(analysisResults).join(', ')}`);
      }
    }
  }, [analysisResults, addInfo, addSuccess, addWarning]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      addInfo(`File selected: ${selectedFile.name} (${(selectedFile.size / 1024).toFixed(2)} KB)`);
    }
  };

  const analyzeFile = () => {
    if (file) {
      setError(null);
      clearLogs();
      openLogs();
      addInfo(`Starting analysis for file: ${file.name}`);
      addInfo(`Analysis type: ${analysisType}`);
      
      uploadBinary({ file, analysis_type: analysisType }, {
        onSuccess: (data) => {
          console.log('[ReverseEngineeringPage] Analysis success:', data);
        },
        onError: (err: any) => {
          console.error('[ReverseEngineeringPage] Analysis error:', err);
          const errorMsg = err?.response?.data?.detail || err?.message || 'An error occurred during analysis';
          setError(errorMsg);
          addError(`Analysis failed: ${errorMsg}`);
        }
      });
    }
  };

  // Helper to safely render analysis data
  const renderAnalysisContent = () => {
    if (!analysisResults) return null;

    const hasNestedAnalysis = analysisResults.analysis && (
      analysisResults.analysis.final_report || 
      (analysisResults.analysis.analyses && Object.keys(analysisResults.analysis.analyses).length > 0)
    );

    const hasDirectAnalysis = analysisResults.final_report || 
      (analysisResults.analyses && Object.keys(analysisResults.analyses).length > 0);

    return (
      <div className="space-y-4">
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
          <div className="glass-panel p-4 bg-gray-800/50">
            <p className="text-xs text-gray-400 mb-2">Debug - Full Response:</p>
            <pre className="text-xs text-gray-500 overflow-x-auto">{JSON.stringify(analysisResults, null, 2)}</pre>
          </div>
        )}

        {/* Nested analysis structure */}
        {hasNestedAnalysis && (
          <>
            {analysisResults.analysis?.final_report && (
              <div className="glass-panel p-6">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <Cpu className="w-5 h-5 text-cyan-400" />
                  AI Security Assessment
                </h3>
                <pre className="text-gray-200 whitespace-pre-wrap text-sm">{analysisResults.analysis.final_report}</pre>
              </div>
            )}

            {analysisResults.analysis?.analyses && Object.entries(analysisResults.analysis.analyses).map(([key, value]: [string, any]) => (
              <div key={key} className="glass-panel p-6">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <Terminal className="w-5 h-5 text-cyan-400" />
                  {key.toUpperCase()} Analysis
                </h3>

                {value.ai_insights && (
                  <div className="mb-4 p-4 bg-cyan-600/20 rounded-lg">
                    <p className="text-sm font-semibold text-cyan-300 mb-2">AI Insights:</p>
                    <p className="text-gray-200">{value.ai_insights}</p>
                  </div>
                )}

                <pre className="text-gray-300 text-sm overflow-x-auto">{value.output || 'No output available'}</pre>
              </div>
            ))}
          </>
        )}

        {/* Direct analysis structure */}
        {hasDirectAnalysis && (
          <>
            {analysisResults.final_report && (
              <div className="glass-panel p-6">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <Cpu className="w-5 h-5 text-cyan-400" />
                  AI Security Assessment
                </h3>
                <pre className="text-gray-200 whitespace-pre-wrap text-sm">{analysisResults.final_report}</pre>
              </div>
            )}

            {analysisResults.analyses && Object.entries(analysisResults.analyses).map(([key, value]: [string, any]) => (
              <div key={key} className="glass-panel p-6">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                  <Terminal className="w-5 h-5 text-cyan-400" />
                  {key.toUpperCase()} Analysis
                </h3>
                {value.ai_insights && (
                  <div className="mb-4 p-4 bg-cyan-600/20 rounded-lg">
                    <p className="text-sm font-semibold text-cyan-300 mb-2">AI Insights:</p>
                    <p className="text-gray-200">{value.ai_insights}</p>
                  </div>
                )}
                <pre className="text-gray-300 text-sm overflow-x-auto">{typeof value === 'string' ? value : JSON.stringify(value, null, 2)}</pre>
              </div>
            ))}
          </>
        )}

        {/* No data found */}
        {!hasNestedAnalysis && !hasDirectAnalysis && (
          <div className="glass-panel p-6 bg-yellow-500/10 border border-yellow-500/30">
            <h3 className="text-lg font-semibold text-yellow-400 mb-2 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" />
              No Analysis Data Found
            </h3>
            <p className="text-gray-300 mb-2">The response was received but no recognizable analysis data was found.</p>
            <p className="text-sm text-gray-400">Available keys in response:</p>
            <pre className="text-xs text-gray-500 mt-2">{JSON.stringify(Object.keys(analysisResults), null, 2)}</pre>
          </div>
        )}

        {/* File path display */}
        {analysisResults.file_path && (
          <div className="glass-panel p-4 bg-green-500/10 border border-green-500/30">
            <p className="text-sm text-green-400 flex items-center gap-2">
              <Upload className="w-4 h-4" />
              File uploaded successfully to: <span className="text-gray-300 font-mono">{analysisResults.file_path}</span>
            </p>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <FileCode className="w-6 h-6 text-cyan-400" />
          Reverse Engineering
        </h1>
        {tools && <Badge variant="info">{tools.tools.length} tools available</Badge>}
      </div>

      <div className="glass-panel p-6 space-y-4">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
          <Upload className="w-5 h-5" />
          Upload Binary
        </h3>
        
        <input
          type="file"
          onChange={handleFileUpload}
          className="block w-full text-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-cyan-600 file:text-white hover:file:bg-cyan-700"
        />
        
        <select
          value={analysisType}
          onChange={(e) => setAnalysisType(e.target.value)}
          className="input-field"
        >
          <option value="full">Full Analysis</option>
          <option value="strings">Strings Analysis</option>
          <option value="radare2">Radare2 Disassembly</option>
          <option value="ghidra">Ghidra Decompilation</option>
          <option value="checksec">Security Features Check</option>
        </select>

        <button
          onClick={analyzeFile}
          disabled={!file || isUploading}
          className="btn-primary w-full"
        >
          {isUploading ? <><Loader2 className="w-4 h-4 animate-spin" />Analyzing...</> : 'Analyze Binary'}
        </button>

        {error && (
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
          title="Binary Analysis Logs"
        />
      </div>

      {renderAnalysisContent()}

      {tools && (
        <div className="glass-panel p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Available Tools</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {tools.tools.map((tool: string) => (
              <Badge key={tool} variant="default">{tool}</Badge>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ReverseEngineeringPage;
