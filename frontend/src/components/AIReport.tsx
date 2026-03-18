import React, { useState } from 'react';
import { FileText, Download, Loader, AlertCircle } from 'lucide-react';
import axios from 'axios';

interface AIReportProps {
  scanId: number;
}

export default function AIReport({ scanId }: AIReportProps) {
  const [report, setReport] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const generateReport = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post(
        'http://localhost:8000/api/v1/rag/report',
        { scan_id: scanId },
        { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } }
      );
      setReport(response.data.report);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = () => {
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `scan-${scanId}-report.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl border border-white/20 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <FileText className="w-6 h-6 text-cyan-400" />
          <h2 className="text-xl font-bold text-white">AI Report</h2>
        </div>
        
        {!report && (
          <button onClick={generateReport} disabled={loading} className="bg-cyan-500 hover:bg-cyan-600 disabled:bg-gray-600 text-white px-4 py-2 rounded-lg">
            {loading ? <><Loader className="w-4 h-4 animate-spin inline mr-2" />Generating...</> : 'Generate'}
          </button>
        )}
        
        {report && (
          <button onClick={downloadReport} className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg">
            <Download className="w-4 h-4 inline mr-2" />Download
          </button>
        )}
      </div>

      {error && (
        <div className="bg-red-500/20 border border-red-500/30 rounded-lg p-4 mb-4">
          <AlertCircle className="w-5 h-5 text-red-400 inline mr-2" />
          <span className="text-red-200">{error}</span>
        </div>
      )}

      {report && (
        <div className="bg-gray-900/50 rounded-lg p-6 text-gray-200 whitespace-pre-wrap">
          {report}
        </div>
      )}
    </div>
  );
}
