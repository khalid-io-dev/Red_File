import { useState } from 'react';
import { Loader2, Plus, Trash2, Save, ArrowDown } from 'lucide-react';
import { useCreateAttackChain } from '../../hooks/useAttackChains';
import { useNavigate } from 'react-router-dom';

export default function ChainBuilder() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [techniques, setTechniques] = useState<any[]>([]);
  const createChain = useCreateAttackChain();

  const availableTechniques = [
    { id: 'T1595', name: 'Active Scanning', tactic: 'Reconnaissance' },
    { id: 'T1190', name: 'Exploit Public-Facing Application', tactic: 'Initial Access' },
    { id: 'T1059', name: 'Command and Scripting Interpreter', tactic: 'Execution' },
    { id: 'T1078', name: 'Valid Accounts', tactic: 'Persistence' },
    { id: 'T1548', name: 'Abuse Elevation Control Mechanism', tactic: 'Privilege Escalation' },
    { id: 'T1027', name: 'Obfuscated Files or Information', tactic: 'Defense Evasion' },
    { id: 'T1003', name: 'OS Credential Dumping', tactic: 'Credential Access' },
    { id: 'T1083', name: 'File and Directory Discovery', tactic: 'Discovery' },
    { id: 'T1021', name: 'Remote Services', tactic: 'Lateral Movement' },
    { id: 'T1560', name: 'Archive Collected Data', tactic: 'Collection' },
    { id: 'T1041', name: 'Exfiltration Over C2 Channel', tactic: 'Exfiltration' }
  ];

  const addTechnique = (technique: any) => {
    setTechniques([...techniques, { ...technique, order: techniques.length + 1 }]);
  };

  const removeTechnique = (index: number) => {
    setTechniques(techniques.filter((_, i) => i !== index));
  };

  const handleSave = () => {
    createChain.mutate({
      name,
      description,
      techniques: techniques.map(t => ({ technique_id: t.id, name: t.name, order: t.order }))
    }, {
      onSuccess: (data) => navigate(`/attack-chains/${data.id}`)
    });
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Attack Chain Builder</h1>

      <div className="grid grid-cols-2 gap-6">
        <div className="space-y-4">
          <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
            <h2 className="text-lg font-bold mb-4">Chain Details</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Name</label>
                <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="My Attack Chain" className="w-full px-4 py-2 bg-white/5 rounded-lg" />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-2">Description</label>
                <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3} placeholder="Describe the attack chain..." className="w-full px-4 py-2 bg-white/5 rounded-lg" />
              </div>
            </div>
          </div>

          <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
            <h2 className="text-lg font-bold mb-4">Available Techniques</h2>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {availableTechniques.map((technique) => (
                <div key={technique.id} className="bg-white/5 rounded-lg p-3 flex items-center justify-between hover:bg-white/10">
                  <div>
                    <div className="font-mono text-sm text-cyan-400">{technique.id}</div>
                    <div className="text-sm">{technique.name}</div>
                    <div className="text-xs text-gray-400">{technique.tactic}</div>
                  </div>
                  <button onClick={() => addTechnique(technique)} className="px-3 py-1 bg-cyan-500/20 hover:bg-cyan-500/30 rounded text-sm">
                    <Plus className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold">Chain Sequence ({techniques.length})</h2>
            <button onClick={handleSave} disabled={!name || techniques.length === 0 || createChain.isPending} className="px-4 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center gap-2">
              {createChain.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
              Save
            </button>
          </div>
          {techniques.length > 0 ? (
            <div className="space-y-3">
              {techniques.map((technique, index) => (
                <div key={index}>
                  <div className="bg-white/5 rounded-lg p-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-cyan-500/20 rounded-full flex items-center justify-center text-sm font-bold">{index + 1}</div>
                      <div>
                        <div className="font-mono text-sm text-cyan-400">{technique.id}</div>
                        <div className="text-sm">{technique.name}</div>
                      </div>
                    </div>
                    <button onClick={() => removeTechnique(index)} className="p-2 hover:bg-red-500/20 rounded">
                      <Trash2 className="w-4 h-4 text-red-400" />
                    </button>
                  </div>
                  {index < techniques.length - 1 && (
                    <div className="flex justify-center py-1">
                      <ArrowDown className="w-4 h-4 text-gray-400" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-400 py-12">Add techniques to build your attack chain</div>
          )}
        </div>
      </div>
    </div>
  );
}
