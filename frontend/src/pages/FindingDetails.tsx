import { useParams, useNavigate } from 'react-router-dom';
import { useFinding, useUpdateFinding } from '../hooks/useFindings';
import { ArrowLeft, AlertTriangle, Loader2, CheckCircle } from 'lucide-react';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

export default function FindingDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: finding, isLoading } = useFinding(Number(id));
  const updateFinding = useUpdateFinding();

  const handleStatusChange = async (status: string) => {
    await updateFinding.mutateAsync({ id: Number(id), data: { status } });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  if (!finding) return <p className="text-center text-gray-500 py-8">Finding not found</p>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="secondary" onClick={() => navigate('/findings')}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-white">{finding.title}</h1>
            <p className="text-gray-400 mt-1">Finding Details</p>
          </div>
        </div>
        <div className="flex gap-3">
          <Button onClick={() => handleStatusChange('resolved')} disabled={updateFinding.isPending}>
            <CheckCircle className="w-4 h-4 mr-2" />
            Mark Resolved
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-panel p-4">
          <p className="text-sm text-gray-400">Severity</p>
          <Badge variant={finding.severity}>{finding.severity}</Badge>
        </div>
        <div className="glass-panel p-4">
          <p className="text-sm text-gray-400">Status</p>
          <Badge variant={finding.status === 'resolved' ? 'success' : 'warning'}>{finding.status}</Badge>
        </div>
        <div className="glass-panel p-4">
          <p className="text-sm text-gray-400">Tool</p>
          <p className="text-gray-300">{finding.tool}</p>
        </div>
        <div className="glass-panel p-4">
          <p className="text-sm text-gray-400">Target</p>
          <p className="text-gray-300 font-mono text-sm">{finding.target}</p>
        </div>
      </div>

      <div className="glass-panel p-6">
        <h2 className="text-xl font-bold text-white mb-4">Description</h2>
        <p className="text-gray-300">{finding.description}</p>
      </div>

      {finding.evidence && (
        <div className="glass-panel p-6">
          <h2 className="text-xl font-bold text-white mb-4">Evidence</h2>
          <pre className="text-sm text-gray-300 bg-gray-900/50 p-4 rounded-lg overflow-x-auto">
            {finding.evidence}
          </pre>
        </div>
      )}

      {finding.remediation && (
        <div className="glass-panel p-6">
          <h2 className="text-xl font-bold text-white mb-4">Remediation</h2>
          <p className="text-gray-300">{finding.remediation}</p>
        </div>
      )}
    </div>
  );
}
