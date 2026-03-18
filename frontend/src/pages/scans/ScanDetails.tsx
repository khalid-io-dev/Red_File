import { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Loader2, ArrowLeft, Square, Trash2, Terminal, Activity } from 'lucide-react';
import { useScan, useStopScan, useDeleteScan } from '../../hooks/useScans';
import StatusBadge from '../../components/ui/StatusBadge';

interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
}

interface ProgressUpdate {
  progress: number;
  status: string;
}

export default function ScanDetails() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: scan, isLoading, refetch } = useScan(Number(id));
  const stopScan = useStopScan();
  const deleteScan = useDeleteScan();
  
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('PENDING');
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token || !id) return;

    const ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`);
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      ws.send(JSON.stringify({ action: 'subscribe', topic: `scan_${id}` }));
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'log') {
        setLogs(prev => [...prev, {
          timestamp: data.timestamp,
          level: data.level,
          message: data.message
        }]);
      } else if (data.type === 'progress') {
        setProgress(data.progress);
        setStatus(data.status);
        refetch();
      }
    };

    ws.onerror = () => setIsConnected(false);
    ws.onclose = () => setIsConnected(false);

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [id, refetch]);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  if (isLoading) return <div className="flex justify-center p-8"><Loader2 className="w-8 h-8 animate-spin" /></div>;
  if (!scan) return <div className="p-8 text-center">Scan not found</div>;

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'error': return 'text-red-400';
      case 'warning': return 'text-yellow-400';
      case 'success': return 'text-green-400';
      default: return 'text-cyan-400';
    }
  };

  const getLevelIcon = (level: string) => {
    switch (level) {
      case 'error': return '✗';
      case 'warning': return '⚠';
      case 'success': return '✓';
      default: return '→';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/scans')} className="p-2 hover:bg-white/10 rounded-lg transition">
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="text-2xl font-bold">{scan.target_url}</h1>
            <p className="text-gray-400">{scan.scan_type} scan</p>
          </div>
        </div>
        <div className="flex gap-2">
          {(status === 'RUNNING' || scan.status === 'running') && (
            <button 
              onClick={() => stopScan.mutate(scan.id)} 
              className="px-4 py-2 bg-yellow-500/20 hover:bg-yellow-500/30 rounded-lg flex items-center gap-2 transition"
            >
              <Square className="w-4 h-4" /> Stop
            </button>
          )}
          <button 
            onClick={() => deleteScan.mutate(scan.id, { onSuccess: () => navigate('/scans') })} 
            className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 rounded-lg flex items-center gap-2 transition"
          >
            <Trash2 className="w-4 h-4" /> Delete
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
          <div className="text-gray-400 text-sm mb-1">Status</div>
          <StatusBadge status={status.toLowerCase() || scan.status} />
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
          <div className="text-gray-400 text-sm mb-1">Progress</div>
          <div className="text-2xl font-bold">{progress}%</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
          <div className="text-gray-400 text-sm mb-1">Connection</div>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`} />
            <span className="text-sm">{isConnected ? 'Live' : 'Disconnected'}</span>
          </div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
          <div className="text-gray-400 text-sm mb-1">Log Entries</div>
          <div className="text-2xl font-bold">{logs.length}</div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-cyan-400" />
            <span className="font-semibold">Scan Progress</span>
          </div>
          <span className="text-sm text-gray-400">{progress}%</span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Real-time Logs */}
      <div className="bg-black/40 backdrop-blur-sm rounded-lg border border-white/10 overflow-hidden">
        <div className="bg-white/5 px-4 py-3 border-b border-white/10 flex items-center gap-2">
          <Terminal className="w-4 h-4 text-cyan-400" />
          <span className="font-semibold">Live Execution Logs</span>
          {isConnected && (
            <span className="ml-auto text-xs text-green-400 flex items-center gap-1">
              <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
              LIVE
            </span>
          )}
        </div>
        <div className="p-4 font-mono text-sm h-96 overflow-y-auto space-y-1">
          {logs.length === 0 ? (
            <div className="text-gray-500 text-center py-8">
              Waiting for scan to start...
            </div>
          ) : (
            logs.map((log, idx) => (
              <div key={idx} className="flex gap-3 hover:bg-white/5 px-2 py-1 rounded">
                <span className="text-gray-500 text-xs">
                  {new Date(log.timestamp).toLocaleTimeString()}
                </span>
                <span className={getLevelColor(log.level)}>
                  {getLevelIcon(log.level)}
                </span>
                <span className={getLevelColor(log.level)}>
                  {log.message}
                </span>
              </div>
            ))
          )}
          <div ref={logsEndRef} />
        </div>
      </div>
    </div>
  );
}
