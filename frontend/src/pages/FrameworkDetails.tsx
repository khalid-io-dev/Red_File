import { useParams, useNavigate } from 'react-router-dom';
import { useComplianceControls } from '../hooks/useCompliance';
import { ArrowLeft, Shield, CheckCircle, XCircle, Loader2 } from 'lucide-react';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

export default function FrameworkDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: controls = [], isLoading } = useComplianceControls(Number(id));

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  const compliantCount = controls.filter(c => c.status === 'compliant').length;
  const nonCompliantCount = controls.filter(c => c.status === 'non_compliant').length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="secondary" onClick={() => navigate('/compliance')}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-white">Framework Controls</h1>
            <p className="text-gray-400 mt-1">Compliance control details</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-panel p-4">
          <p className="text-sm text-gray-400">Total Controls</p>
          <p className="text-2xl font-bold text-cyan-400">{controls.length}</p>
        </div>
        <div className="glass-panel p-4">
          <p className="text-sm text-gray-400">Compliant</p>
          <p className="text-2xl font-bold text-green-400">{compliantCount}</p>
        </div>
        <div className="glass-panel p-4">
          <p className="text-sm text-gray-400">Non-Compliant</p>
          <p className="text-2xl font-bold text-red-400">{nonCompliantCount}</p>
        </div>
      </div>

      <div className="glass-panel rounded-xl overflow-hidden">
        <table className="data-table">
          <thead>
            <tr>
              <th>Control ID</th>
              <th>Title</th>
              <th>Status</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {controls.length > 0 ? (
              controls.map((control) => (
                <tr key={control.id}>
                  <td className="font-mono text-sm">{control.control_id}</td>
                  <td className="font-medium">{control.title}</td>
                  <td>
                    <Badge variant={control.status === 'compliant' ? 'success' : 'danger'}>
                      {control.status === 'compliant' ? (
                        <CheckCircle className="w-3 h-3 mr-1 inline" />
                      ) : (
                        <XCircle className="w-3 h-3 mr-1 inline" />
                      )}
                      {control.status}
                    </Badge>
                  </td>
                  <td className="text-sm text-gray-400">{control.description}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={4} className="text-center py-8 text-gray-500">No controls found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
