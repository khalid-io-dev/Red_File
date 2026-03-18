import React from 'react';
import { Terminal, CheckCircle, XCircle, Loader } from 'lucide-react';

interface ToolExecutionProps {
  tool: string;
  arguments: any;
  result?: any;
  success?: boolean;
  loading?: boolean;
}

export default function ToolExecution({ tool, arguments: args, result, success, loading }: ToolExecutionProps) {
  return (
    <div className="bg-gray-900/50 rounded-xl p-4 border border-cyan-500/30 mb-3">
      <div className="flex items-center gap-2 mb-2">
        <Terminal className="w-4 h-4 text-cyan-400" />
        <span className="text-cyan-300 font-mono text-sm font-semibold">{tool}</span>
        {loading && <Loader className="w-4 h-4 text-cyan-400 animate-spin" />}
        {!loading && success !== undefined && (
          success ? 
            <CheckCircle className="w-4 h-4 text-green-400" /> : 
            <XCircle className="w-4 h-4 text-red-400" />
        )}
      </div>
      
      <div className="text-xs text-gray-400 mb-2">
        <span className="text-gray-500">Arguments:</span>
        <pre className="bg-black/30 p-2 rounded mt-1 overflow-x-auto">
          {JSON.stringify(args, null, 2)}
        </pre>
      </div>
      
      {result && (
        <div className="text-xs text-gray-300">
          <span className="text-gray-500">Result:</span>
          <pre className="bg-black/30 p-2 rounded mt-1 overflow-x-auto max-h-40">
            {typeof result === 'string' ? result.substring(0, 500) : JSON.stringify(result, null, 2).substring(0, 500)}
          </pre>
        </div>
      )}
    </div>
  );
}
