import { useState } from 'react';
import { useSECampaigns, useCreateSECampaign, useSEOSINT } from '../../hooks/useAdvancedTools';
import { Mail, Target, Eye, MousePointer, Loader2, Plus } from 'lucide-react';
import Badge from '../../components/ui/Badge';

export default function SECampaignManager() {
  const [showCreate, setShowCreate] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    target_email: '',
    target_name: '',
    target_company: '',
    template_type: 'urgent_security'
  });

  const { data: campaigns, isLoading, refetch } = useSECampaigns();
  const { mutate: createCampaign, isPending: isCreating } = useCreateSECampaign();
  const { mutate: gatherOSINT, data: osintData, isPending: isGathering } = useSEOSINT();

  const handleCreate = () => {
    createCampaign(formData, {
      onSuccess: () => {
        setShowCreate(false);
        setFormData({ name: '', target_email: '', target_name: '', target_company: '', template_type: 'urgent_security' });
        refetch();
      }
    });
  };

  const templates = [
    { value: 'urgent_security', label: 'Urgent Security Alert' },
    { value: 'password_reset', label: 'Password Reset' },
    { value: 'invoice', label: 'Invoice/Payment' },
    { value: 'hr_notice', label: 'HR Notice' },
    { value: 'it_support', label: 'IT Support' }
  ];

  if (isLoading) {
    return <div className="flex items-center justify-center h-96"><Loader2 className="w-8 h-8 text-cyan-400 animate-spin" /></div>;
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-pink-500/20 to-red-500/20 
                           border border-pink-500/30 flex items-center justify-center">
              <Mail className="w-5 h-5 text-pink-400" />
            </div>
            Social Engineering Campaigns
          </h1>
          <p className="text-gray-400 mt-1 ml-13">Create and manage phishing campaigns with OSINT integration</p>
        </div>
        <button 
          onClick={() => setShowCreate(!showCreate)} 
          className="px-4 py-2 bg-gradient-to-r from-pink-500 to-red-500 hover:from-pink-600 hover:to-red-600 
                     text-white font-semibold rounded-lg transition-all duration-300 flex items-center gap-2 shadow-lg hover:shadow-pink-500/50"
        >
          <Plus className="w-4 h-4" />
          New Campaign
        </button>
      </div>

      {showCreate && (
        <div className="glass-panel p-6 rounded-xl border border-gray-800 hover:border-pink-500/30 transition-all duration-300 space-y-4 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-pink-500/50 to-transparent opacity-50"></div>
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <span className="text-pink-500">✨</span> Create Campaign
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="Campaign Name"
              className="input-field"
            />
            <div className="flex gap-2">
              <input
                type="email"
                value={formData.target_email}
                onChange={(e) => setFormData({ ...formData, target_email: e.target.value })}
                placeholder="target@company.com"
                className="input-field flex-1"
              />
              <button
                onClick={() => gatherOSINT({ target: formData.target_email, target_type: 'email' })}
                disabled={isGathering}
                className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-cyan-400 rounded-lg transition-all duration-300 border border-gray-700 hover:border-cyan-500/50"
              >
                {isGathering ? <Loader2 className="w-4 h-4 animate-spin" /> : <Target className="w-4 h-4" />}
              </button>
            </div>
            <input
              type="text"
              value={formData.target_name}
              onChange={(e) => setFormData({ ...formData, target_name: e.target.value })}
              placeholder="Target Name"
              className="input-field"
            />
            <input
              type="text"
              value={formData.target_company}
              onChange={(e) => setFormData({ ...formData, target_company: e.target.value })}
              placeholder="Company"
              className="input-field"
            />
            <select
              value={formData.template_type}
              onChange={(e) => setFormData({ ...formData, template_type: e.target.value })}
              className="input-field md:col-span-2"
            >
              {templates.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
            </select>
          </div>
          {osintData && (
            <div className="p-4 bg-gradient-to-br from-gray-800/80 to-gray-900/80 rounded-lg border border-cyan-500/30 shadow-lg">
              <pre className="text-xs text-gray-300 overflow-x-auto">{JSON.stringify(osintData, null, 2)}</pre>
            </div>
          )}
          <div className="flex gap-2">
            <button onClick={handleCreate} disabled={isCreating} className="flex-1 px-6 py-3 bg-gradient-to-r from-pink-500 to-red-500 hover:from-pink-600 hover:to-red-600 
                     text-white font-semibold rounded-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed
                     flex items-center justify-center gap-2 shadow-lg hover:shadow-pink-500/50">
              {isCreating ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Create'}
            </button>
            <button onClick={() => setShowCreate(false)} className="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition-all duration-300 border border-gray-700">Cancel</button>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-panel p-5 rounded-xl border border-gray-800 hover:border-cyan-500/30 transition-all duration-300 group">
          <div className="text-gray-400 text-xs uppercase tracking-wider mb-2">Total Campaigns</div>
          <div className="text-3xl font-bold text-white font-mono tracking-tighter group-hover:scale-110 transition-transform">{campaigns?.campaigns?.length || 0}</div>
        </div>
        <div className="glass-panel p-5 rounded-xl border border-gray-800 hover:border-green-500/30 transition-all duration-300 group relative overflow-hidden">
          <div className="absolute right-0 top-0 p-3 opacity-10 text-4xl group-hover:scale-110 transition-transform">✅</div>
          <div className="text-gray-400 text-xs uppercase tracking-wider mb-2">Active</div>
          <div className="text-3xl font-bold text-green-400 font-mono tracking-tighter group-hover:scale-110 transition-transform relative z-10">
            {campaigns?.campaigns?.filter((c: any) => c.status === 'active').length || 0}
          </div>
        </div>
        <div className="glass-panel p-5 rounded-xl border border-gray-800 hover:border-yellow-500/30 transition-all duration-300 group relative overflow-hidden">
          <div className="absolute right-0 top-0 p-3 opacity-10 text-4xl group-hover:scale-110 transition-transform">👁️</div>
          <div className="text-gray-400 text-xs uppercase tracking-wider mb-2">Opened</div>
          <div className="text-3xl font-bold text-yellow-400 font-mono tracking-tighter group-hover:scale-110 transition-transform relative z-10">
            {campaigns?.campaigns?.filter((c: any) => c.email_opened).length || 0}
          </div>
        </div>
        <div className="glass-panel p-5 rounded-xl border border-gray-800 hover:border-red-500/30 transition-all duration-300 group relative overflow-hidden">
          <div className="absolute right-0 top-0 p-3 opacity-10 text-4xl group-hover:scale-110 transition-transform">🖱️</div>
          <div className="text-gray-400 text-xs uppercase tracking-wider mb-2">Clicked</div>
          <div className="text-3xl font-bold text-red-400 font-mono tracking-tighter group-hover:scale-110 transition-transform relative z-10">
            {campaigns?.campaigns?.filter((c: any) => c.link_clicked).length || 0}
          </div>
        </div>
      </div>

      <div className="glass-panel rounded-xl overflow-hidden border border-gray-800">
        <div className="p-4 border-b border-gray-800 bg-gray-900/50 flex items-center gap-2">
          <span className="text-pink-500">📧</span>
          <h3 className="font-semibold text-gray-200">Campaign Tracking</h3>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Campaign</th>
              <th>Target</th>
              <th>Status</th>
              <th>Opened</th>
              <th>Clicked</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {campaigns?.campaigns?.length > 0 ? (
              campaigns.campaigns.map((c: any) => (
                <tr key={c.id} className="hover:bg-pink-900/5 transition-colors group">
                  <td className="font-medium">{c.name}</td>
                  <td className="text-gray-400">{c.target}</td>
                  <td><Badge variant={c.status === 'active' ? 'success' : 'info'}>{c.status}</Badge></td>
                  <td>{c.email_opened ? <Eye className="w-4 h-4 text-yellow-400" /> : '-'}</td>
                  <td>{c.link_clicked ? <MousePointer className="w-4 h-4 text-red-400" /> : '-'}</td>
                  <td className="text-gray-400 text-sm">{new Date(c.created_at).toLocaleDateString()}</td>
                </tr>
              ))
            ) : (
              <tr><td colSpan={6} className="text-center py-8 text-gray-500">No campaigns</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
