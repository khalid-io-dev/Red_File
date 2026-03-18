import { useState } from 'react';
import { Search, Download, AlertTriangle, Loader2, BarChart3 } from 'lucide-react';
import { useFindings } from '../hooks/useFindings';
import { useNavigate } from 'react-router-dom';
import DataTable from '../components/ui/DataTable';
import Badge from '../components/ui/Badge';
import Button from '../components/ui/Button';
import EmptyState from '../components/ui/EmptyState';
import AdvancedFilter from '../components/filters/AdvancedFilter';
import { Finding } from '../types/finding';
import { formatDate } from '../lib/utils';

export default function Findings() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<any>({});

  const { data: findings = [], isLoading } = useFindings(filters);

  const filteredFindings = findings.filter((f: Finding) => {
    const matchesSearch = f.title.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesSearch;
  });

  const stats = {
    total: findings.length,
    critical: findings.filter((f: Finding) => f.severity === 'critical').length,
    high: findings.filter((f: Finding) => f.severity === 'high').length,
    medium: findings.filter((f: Finding) => f.severity === 'medium').length,
    low: findings.filter((f: Finding) => f.severity === 'low').length,
  };

  const columns = [
    {
      key: 'severity',
      label: 'Severity',
      render: (f: Finding) => <Badge variant={f.severity}>{f.severity.toUpperCase()}</Badge>,
    },
    {
      key: 'title',
      label: 'Finding',
      render: (f: Finding) => (
        <div>
          <p className="font-medium text-gray-300">{f.title}</p>
          <p className="text-xs text-gray-500">{f.tool}</p>
        </div>
      ),
    },
    { key: 'target', label: 'Target' },
    { key: 'created_at', label: 'Discovered', render: (f: Finding) => formatDate(f.created_at) },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Findings</h1>
          <p className="text-gray-400 mt-1">Security vulnerabilities</p>
        </div>
        <div className="flex gap-2">
          <AdvancedFilter
            onApply={setFilters}
            onClear={() => setFilters({})}
            onExport={() => window.open('/api/v1/findings/export', '_blank')}
          />
          <Button onClick={() => navigate('/findings/analysis')} icon={<BarChart3 className="w-5 h-5" />}>
            View Graph Analysis
          </Button>
          <Button>
            <Download className="w-5 h-5 mr-2" />
            Export
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-5 gap-4">
        <div className="p-4 rounded-lg bg-gray-900/50 border border-cyan-500/20">
          <p className="text-sm text-gray-400">Total</p>
          <p className="text-2xl font-bold text-cyan-400">{stats.total}</p>
        </div>
        <div className="p-4 rounded-lg bg-gray-900/50 border border-red-600/20">
          <p className="text-sm text-gray-400">Critical</p>
          <p className="text-2xl font-bold text-red-600">{stats.critical}</p>
        </div>
        <div className="p-4 rounded-lg bg-gray-900/50 border border-red-500/20">
          <p className="text-sm text-gray-400">High</p>
          <p className="text-2xl font-bold text-red-500">{stats.high}</p>
        </div>
        <div className="p-4 rounded-lg bg-gray-900/50 border border-yellow-500/20">
          <p className="text-sm text-gray-400">Medium</p>
          <p className="text-2xl font-bold text-yellow-500">{stats.medium}</p>
        </div>
        <div className="p-4 rounded-lg bg-gray-900/50 border border-blue-500/20">
          <p className="text-sm text-gray-400">Low</p>
          <p className="text-2xl font-bold text-blue-500">{stats.low}</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search findings..."
            className="w-full pl-10 pr-4 py-2 bg-gray-900/50 border border-cyan-500/20 rounded-lg text-gray-300 focus:border-cyan-500 focus:outline-none"
          />
        </div>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
        </div>
      ) : filteredFindings.length === 0 ? (
        <EmptyState
          icon={AlertTriangle}
          title="No findings"
          description={findings.length === 0 ? "No security findings yet. Run scans to discover vulnerabilities." : "No findings match your filters."}
        />
      ) : (
        <div className="cursor-pointer">
          <DataTable 
            data={filteredFindings} 
            columns={columns}
            onRowClick={(finding: Finding) => navigate(`/findings/${finding.id}`)}
          />
        </div>
      )}
    </div>
  );
}
