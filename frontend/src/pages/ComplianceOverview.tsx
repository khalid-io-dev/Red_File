import { useComplianceFrameworks } from '../hooks/useCompliance';
import { Shield, Loader2, CheckCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function ComplianceOverview() {
  const { data: frameworks = [], isLoading } = useComplianceFrameworks();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white flex items-center gap-3">
        <Shield className="w-6 h-6 text-cyan-400" />
        Compliance Overview
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {frameworks.map(framework => (
          <Link key={framework.id} to={`/compliance/framework/${framework.id}`}>
            <div className="glass-panel p-6 rounded-xl hover:border-cyan-500/50 transition-all cursor-pointer">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h2 className="text-lg font-bold text-white">{framework.name}</h2>
                  <p className="text-sm text-gray-400">v{framework.version}</p>
                </div>
                <CheckCircle className="w-5 h-5 text-green-400" />
              </div>
              <p className="text-gray-400 text-sm mb-4">{framework.description}</p>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500">Controls</span>
                <span className="text-cyan-400 font-bold">{framework.controls_count}</span>
              </div>
            </div>
          </Link>
        ))}
      </div>
      {frameworks.length === 0 && (
        <p className="text-center text-gray-500 py-12">No compliance frameworks configured</p>
      )}
    </div>
  );
}
