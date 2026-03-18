import { useRef, useEffect } from 'react';
import { Terminal, X } from 'lucide-react';

interface LogEntry {
  timestamp: string;
  level: 'info' | 'success' | 'warning' | 'error';
  message: string;
}

interface LogConsoleProps {
  logs: LogEntry[];
  isOpen: boolean;
  onClose: () => void;
  title?: string;
}

const levelColors = {
  info: 'text-blue-400',
  success: 'text-green-400',
  warning: 'text-yellow-400',
  error: 'text-red-400',
};

const levelBgColors = {
  info: 'bg-blue-500/10',
  success: 'bg-green-500/10',
  warning: 'bg-yellow-500/10',
  error: 'bg-red-500/10',
};

export const LogConsole = ({ logs, isOpen, onClose, title = 'Real-time Logs' }: LogConsoleProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  if (!isOpen) return null;

  return (
    <div className="glass-panel p-4 mt-4 border border-cyan-500/30">
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-sm font-semibold text-cyan-400 flex items-center gap-2">
          <Terminal className="w-4 h-4" />
          {title}
        </h4>
        <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
          <X className="w-4 h-4" />
        </button>
      </div>
      
      <div 
        ref={scrollRef}
        className="h-48 overflow-y-auto font-mono text-xs space-y-1 bg-black/30 rounded-lg p-3"
      >
        {logs.length === 0 ? (
          <p className="text-gray-500 italic">Waiting for logs...</p>
        ) : (
          logs.map((log, index) => (
            <div 
              key={index} 
              className={`flex gap-2 px-2 py-1 rounded ${levelBgColors[log.level]}`}
            >
              <span className="text-gray-500 shrink-0">[{log.timestamp}]</span>
              <span className={`${levelColors[log.level]} shrink-0 uppercase w-16`}>{log.level}</span>
              <span className="text-gray-300 break-all">{log.message}</span>
            </div>
          ))
        )}
      </div>
      
      <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
        <span>{logs.length} entries</span>
        <div className="flex gap-3">
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-blue-400"></span> Info</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-green-400"></span> Success</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-yellow-400"></span> Warning</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-red-400"></span> Error</span>
        </div>
      </div>
    </div>
  );
};

export default LogConsole;
