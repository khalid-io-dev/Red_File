import { Download, CheckCircle, Loader2 } from 'lucide-react';
import { useCredentials } from '../hooks/useCredentials';
import DataTable from '../components/ui/DataTable';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

export default function Credentials() {
  const { data: credentials = [], isLoading } = useCredentials();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  const columns = [
    { key: 'username', label: 'Username', render: (c: any) => <span className="font-mono text-cyan-400">{c.username}</span> },
    { key: 'password', label: 'Password', render: (c: any) => <span className="font-mono text-gray-300">{c.password}</span> },
    { key: 'service', label: 'Service', render: (c: any) => <Badge variant="info">{c.service || 'Unknown'}</Badge> },
    { key: 'target', label: 'Target' },
    {
      key: 'actions',
      label: 'Actions',
      render: () => (
        <Button size="sm" variant="ghost">
          <CheckCircle className="w-4 h-4 mr-1" />
          Test
        </Button>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Credentials</h1>
          <p className="text-gray-400 mt-1">Harvested credentials</p>
        </div>
        <Button>
          <Download className="w-5 h-5 mr-2" />
          Export CSV
        </Button>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="p-4 rounded-lg bg-gray-900/50 border border-cyan-500/20">
          <p className="text-sm text-gray-400">Total Credentials</p>
          <p className="text-2xl font-bold text-cyan-400">{credentials.length}</p>
        </div>
        <div className="p-4 rounded-lg bg-gray-900/50 border border-green-500/20">
          <p className="text-sm text-gray-400">Validated</p>
          <p className="text-2xl font-bold text-green-400">{credentials.filter((c: any) => c.is_valid).length}</p>
        </div>
        <div className="p-4 rounded-lg bg-gray-900/50 border border-purple-500/20">
          <p className="text-sm text-gray-400">Unique Targets</p>
          <p className="text-2xl font-bold text-purple-400">{new Set(credentials.map((c: any) => c.target)).size}</p>
        </div>
        <div className="p-4 rounded-lg bg-gray-900/50 border border-cyan-500/20">
          <p className="text-sm text-gray-400">Services</p>
          <p className="text-2xl font-bold text-cyan-400">{new Set(credentials.map((c: any) => c.service)).size}</p>
        </div>
      </div>

      <DataTable data={credentials} columns={columns} />
    </div>
  );
}
