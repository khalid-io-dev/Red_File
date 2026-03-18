import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCreateCampaign } from '../hooks/useCampaigns';
import { Plus, X, Loader2 } from 'lucide-react';
import Button from '../components/ui/Button';

export default function CreateCampaign() {
  const navigate = useNavigate();
  const createCampaign = useCreateCampaign();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    targets: [''],
    scan_type: 'quick',
  });
  const [error, setError] = useState<string | null>(null);

  const addTarget = () => setFormData({ ...formData, targets: [...formData.targets, ''] });
  const removeTarget = (idx: number) => setFormData({ ...formData, targets: formData.targets.filter((_, i) => i !== idx) });
  const updateTarget = (idx: number, value: string) => {
    const newTargets = [...formData.targets];
    newTargets[idx] = value;
    setFormData({ ...formData, targets: newTargets });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      // Filter empty targets
      const targets = formData.targets.filter(t => t.trim());
      if (targets.length === 0) {
        setError('At least one target is required');
        return;
      }

      await createCampaign.mutateAsync({
        ...formData,
        targets
      });
      navigate('/campaigns');
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to create campaign. Please try again.');
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white">Create Campaign</h1>

      {error && (
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-lg flex items-center gap-2">
          <X className="w-5 h-5" />
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="glass-panel p-6 rounded-xl space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Campaign Name</label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Description</label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
            rows={3}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Targets</label>
          {formData.targets.map((target, idx) => (
            <div key={idx} className="flex gap-2 mb-2">
              <input
                type="text"
                value={target}
                onChange={(e) => updateTarget(idx, e.target.value)}
                placeholder="192.168.1.0/24 or example.com"
                className="flex-1 px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
                required
              />
              {formData.targets.length > 1 && (
                <button type="button" onClick={() => removeTarget(idx)} className="p-2 text-red-400 hover:bg-red-500/10 rounded-lg">
                  <X className="w-5 h-5" />
                </button>
              )}
            </div>
          ))}
          <button type="button" onClick={addTarget} className="text-cyan-400 text-sm flex items-center gap-1 mt-2">
            <Plus className="w-4 h-4" /> Add Target
          </button>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Scan Type</label>
          <select
            value={formData.scan_type}
            onChange={(e) => setFormData({ ...formData, scan_type: e.target.value })}
            className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
          >
            <option value="quick">Quick Scan</option>
            <option value="deep">Deep Scan</option>
            <option value="passive">Passive Scan</option>
          </select>
        </div>
        <div className="flex gap-3">
          <Button type="submit" disabled={createCampaign.isPending}>
            {createCampaign.isPending ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
            Create Campaign
          </Button>
          <Button variant="ghost" onClick={() => navigate('/campaigns')} type="button">Cancel</Button>
        </div>
      </form>
    </div>
  );
}
