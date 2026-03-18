import { useState } from 'react';
import { useCreateCampaign } from '../../hooks/useCampaigns';
import Modal from '../ui/Modal';
import Button from '../ui/Button';

interface CreateCampaignModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function CreateCampaignModal({ isOpen, onClose }: CreateCampaignModalProps) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [targets, setTargets] = useState('');
  const [chainType, setChainType] = useState<'web' | 'network'>('web');
  const createCampaign = useCreateCampaign();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createCampaign.mutateAsync({
      name,
      description,
      targets: targets.split('\n').filter(t => t.trim()),
      chain_type: chainType,
    });
    onClose();
    setName('');
    setDescription('');
    setTargets('');
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Create New Campaign">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Campaign Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:border-cyan-500 focus:outline-none"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:border-cyan-500 focus:outline-none"
            rows={3}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Targets (one per line)</label>
          <textarea
            value={targets}
            onChange={(e) => setTargets(e.target.value)}
            className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:border-cyan-500 focus:outline-none font-mono text-sm"
            rows={5}
            placeholder="example.com&#10;192.168.1.1&#10;target.local"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Attack Chain Type</label>
          <select
            value={chainType}
            onChange={(e) => setChainType(e.target.value as 'web' | 'network')}
            className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:border-cyan-500 focus:outline-none"
          >
            <option value="web">Web Attack Chain</option>
            <option value="network">Network Attack Chain</option>
          </select>
        </div>

        <div className="flex justify-end gap-3 pt-4">
          <Button type="button" variant="secondary" onClick={onClose}>Cancel</Button>
          <Button type="submit" disabled={createCampaign.isPending}>
            {createCampaign.isPending ? 'Creating...' : 'Create Campaign'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
