import { Loader2, Plus, Play } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useScans, useCreateScan } from '../../hooks/useScans';

export default function ScanTemplates() {
  const navigate = useNavigate();
  const createScan = useCreateScan();

  const templates = [
    { id: 1, name: 'Quick Network Scan', type: 'quick', description: 'Fast port scan with service detection', tools: ['nmap'] },
    { id: 2, name: 'Deep Vulnerability Scan', type: 'deep', description: 'Comprehensive vulnerability assessment', tools: ['nmap', 'nikto', 'sqlmap'] },
    { id: 3, name: 'Web Application Test', type: 'web', description: 'Full web app security testing', tools: ['nikto', 'sqlmap', 'xsstrike'] },
    { id: 4, name: 'Passive Reconnaissance', type: 'passive', description: 'OSINT and passive information gathering', tools: ['theHarvester', 'whois'] },
    { id: 5, name: 'Cloud Security Audit', type: 'cloud', description: 'AWS/Azure/GCP security assessment', tools: ['prowler', 'cloudsploit'] },
    { id: 6, name: 'Container Security Scan', type: 'container', description: 'Docker and Kubernetes security', tools: ['trivy', 'kube-bench'] }
  ];

  const handleUseTemplate = (template: any) => {
    createScan.mutate({
      target: '',
      scan_type: template.type,
      options: { template: template.name }
    }, {
      onSuccess: (data) => navigate(`/scans/${data.id}`)
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Scan Templates</h1>
        <button onClick={() => navigate('/scans/create')} className="px-4 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center gap-2">
          <Plus className="w-4 h-4" /> Create Custom
        </button>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {templates.map((template) => (
          <div key={template.id} className="bg-white/5 backdrop-blur-sm rounded-lg p-6 hover:bg-white/10">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-lg font-bold mb-1">{template.name}</h3>
                <p className="text-sm text-gray-400">{template.description}</p>
              </div>
              <button onClick={() => handleUseTemplate(template)} disabled={createScan.isPending} className="px-3 py-1.5 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center gap-2 text-sm">
                <Play className="w-3 h-3" /> Use
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {template.tools.map((tool) => (
                <span key={tool} className="px-2 py-1 bg-white/5 rounded text-xs font-mono">{tool}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
