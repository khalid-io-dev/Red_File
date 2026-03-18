import { useState } from 'react';
import { Plus, Play, Trash2, Eye, RefreshCw } from 'lucide-react';
import { useScans, useCreateScan, useDeleteScan } from '../hooks/useScans';
import DataTable from '../components/ui/DataTable';
import Badge from '../components/ui/Badge';
import Button from '../components/ui/Button';
import Modal from '../components/ui/Modal';
import ProgressBar from '../components/ui/ProgressBar';
import { Scan } from '../types/scan';
import { useNavigate } from 'react-router-dom';

export default function EnhancedScans() {
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [target, setTarget] = useState('');
  const [scanType, setScanType] = useState<'quick' | 'deep' | 'passive'>('quick');
  
  const navigate = useNavigate();
  const { data: scans = [], isLoading, refetch } = useScans();
  const createScan = useCreateScan();
  const deleteScan = useDeleteScan();

  const handleCreateScan = async (e: React.FormEvent) => {
    e.preventDefault();
    await createScan.mutateAsync({ target, scan_type: scanType });
    setCreateModalOpen(false);
    setTarget('');
  };

  const columns = [
    { key: 'target', label: 'Target', render: (s: Scan) => <span className="font-mono text-cyan-400">{s.target}</span> },
    { key: 'scan_type', label: 'Type', render: (s: Scan) => <Badge variant="info">{s.scan_type}</Badge> },
    { 
      key: 'status', 
      label: 'Status', 
      render: (s: Scan) => (
        <div className="flex items-center gap-2">
          <Badge variant={s.status === 'completed' ? 'success' : s.status === 'running' ? 'info' : 'default'}>
            {s.status}
          </Badge>
          {s.status === 'running' && <RefreshCw className="w-4 h-4 text-cyan-400 animate-spin" />}
        </div>
      )
    },
    { 
      key: 'progress', 
      label: 'Progress', 
      render: (s: Scan) => s.status === 'running' ? <ProgressBar value={s.progress} showLabel={false} /> : <span>{s.progress}%</span>
    },
    { key: 'created_at', label: 'Created', render: (s: Scan) => new Date(s.created_at).toLocaleString() },
    {
      key: 'actions',
      label: 'Actions',
      render: (s: Scan) => (
        <div className="flex items-center gap-2">
          <Button size="sm" variant="ghost" onClick={() => navigate(`/scans/${s.id}`)}>
            <Eye className="w-4 h-4" />
          </Button>
          <Button size="sm" variant="danger" onClick={() => deleteScan.mutate(s.id)}>
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Scans</h1>
          <p className="text-gray-400 mt-1">Manage security scans</p>
        </div>
        <div className="flex gap-3">
          <Button variant="secondary" onClick={() => refetch()}>
            <RefreshCw className="w-5 h-5 mr-2" />
            Refresh
          </Button>
          <Button onClick={() => setCreateModalOpen(true)} className="cyber-glow">
            <Plus className="w-5 h-5 mr-2" />
            New Scan
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-panel p-4 rounded-lg">
          <p className="text-sm text-gray-400">Total Scans</p>
          <p className="text-2xl font-bold text-cyan-400">{scans.length}</p>
        </div>
        <div className="glass-panel p-4 rounded-lg">
          <p className="text-sm text-gray-400">Running</p>
          <p className="text-2xl font-bold text-cyan-400">{scans.filter(s => s.status === 'running').length}</p>
        </div>
        <div className="glass-panel p-4 rounded-lg">
          <p className="text-sm text-gray-400">Completed</p>
          <p className="text-2xl font-bold text-green-400">{scans.filter(s => s.status === 'completed').length}</p>
        </div>
        <div className="glass-panel p-4 rounded-lg">
          <p className="text-sm text-gray-400">Failed</p>
          <p className="text-2xl font-bold text-red-400">{scans.filter(s => s.status === 'failed').length}</p>
        </div>
      </div>

      {isLoading ? (
        <div className="text-center py-12 text-gray-400">Loading scans...</div>
      ) : (
        <DataTable data={scans} columns={columns} />
      )}

      <Modal isOpen={createModalOpen} onClose={() => setCreateModalOpen(false)} title="Create New Scan">
        <form onSubmit={handleCreateScan} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Target</label>
            <input
              type="text"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              placeholder="example.com or 192.168.1.1"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:border-cyan-500 focus:outline-none"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Scan Type</label>
            <select
              value={scanType}
              onChange={(e) => setScanType(e.target.value as any)}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:border-cyan-500 focus:outline-none"
            >
              <option value="quick">Quick Scan</option>
              <option value="deep">Deep Scan</option>
              <option value="passive">Passive Scan</option>
            </select>
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="secondary" onClick={() => setCreateModalOpen(false)}>Cancel</Button>
            <Button type="submit" disabled={createScan.isPending}>
              {createScan.isPending ? 'Creating...' : 'Create Scan'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
