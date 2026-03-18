import { useParams, useNavigate } from 'react-router-dom';
import { Loader2, ArrowLeft } from 'lucide-react';
import { useComplianceFramework, useComplianceControls } from '../../hooks/useCompliance';

export default function ComplianceControls() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: framework, isLoading: frameworkLoading } = useComplianceFramework(Number(id));
  const { data: controlsData, isLoading: controlsLoading } = useComplianceControls(Number(id));

  if (frameworkLoading || controlsLoading) return <div className="flex justify-center p-8"><Loader2 className="w-8 h-8 animate-spin" /></div>;
  if (!framework) return <div className="p-8 text-center">Framework not found</div>;

  const controls = controlsData?.controls || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <button onClick={() => navigate('/compliance')} className="p-2 hover:bg-white/10 rounded-lg">
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <h1 className="text-2xl font-bold">{framework.name} Controls</h1>
          <p className="text-gray-400">{framework.description}</p>
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        {controls.length > 0 ? (
          <div className="divide-y divide-white/10">
            {controls.map((control: any) => (
              <div key={control.id} className="p-4 hover:bg-white/5">
                <div className="flex items-start justify-between mb-2">
                  <div className="font-mono text-cyan-400">{control.control_id}</div>
                  <span className={`px-2 py-0.5 rounded text-xs ${
                    control.status === 'compliant' ? 'bg-green-500/20 text-green-400' :
                    control.status === 'non_compliant' ? 'bg-red-500/20 text-red-400' :
                    'bg-yellow-500/20 text-yellow-400'
                  }`}>{control.status}</span>
                </div>
                <div className="text-lg font-semibold mb-1">{control.title}</div>
                <div className="text-sm text-gray-400">{control.description}</div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center text-gray-400 py-12">No controls found</div>
        )}
      </div>
    </div>
  );
}
