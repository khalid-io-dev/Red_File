import { Loader2, Shield, Plus, Edit, Trash2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function SecurityPolicies() {
  const navigate = useNavigate();

  const policies = [
    { id: 1, name: 'Password Policy', category: 'Authentication', status: 'active', rules: 5 },
    { id: 2, name: 'Access Control Policy', category: 'Authorization', status: 'active', rules: 8 },
    { id: 3, name: 'Data Encryption Policy', category: 'Data Protection', status: 'active', rules: 6 },
    { id: 4, name: 'Incident Response Policy', category: 'Security Operations', status: 'active', rules: 12 },
    { id: 5, name: 'Network Security Policy', category: 'Network', status: 'draft', rules: 10 }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Security Policies</h1>
        <button className="px-4 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center gap-2">
          <Plus className="w-4 h-4" /> Create Policy
        </button>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Total Policies</div>
          <div className="text-2xl font-bold">{policies.length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Active</div>
          <div className="text-2xl font-bold text-green-400">{policies.filter(p => p.status === 'active').length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Draft</div>
          <div className="text-2xl font-bold text-yellow-400">{policies.filter(p => p.status === 'draft').length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Total Rules</div>
          <div className="text-2xl font-bold">{policies.reduce((sum, p) => sum + p.rules, 0)}</div>
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        <div className="divide-y divide-white/10">
          {policies.map((policy) => (
            <div key={policy.id} className="p-4 hover:bg-white/5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-cyan-500/20 rounded-lg flex items-center justify-center">
                    <Shield className="w-5 h-5 text-cyan-400" />
                  </div>
                  <div>
                    <div className="font-semibold">{policy.name}</div>
                    <div className="text-sm text-gray-400">{policy.category} • {policy.rules} rules</div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-1 rounded text-xs ${
                    policy.status === 'active' ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'
                  }`}>{policy.status}</span>
                  <button className="p-2 hover:bg-white/10 rounded">
                    <Edit className="w-4 h-4" />
                  </button>
                  <button className="p-2 hover:bg-red-500/20 rounded">
                    <Trash2 className="w-4 h-4 text-red-400" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
