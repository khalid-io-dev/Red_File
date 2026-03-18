import { Loader2, Search, Globe, Mail, Users, FileText } from 'lucide-react';
import { useState } from 'react';

export default function OSINTHub() {
  const [target, setTarget] = useState('');

  const sources = [
    { name: 'Domain Intelligence', icon: Globe, count: 45, status: 'active' },
    { name: 'Email Harvesting', icon: Mail, count: 128, status: 'active' },
    { name: 'Social Media', icon: Users, count: 89, status: 'active' },
    { name: 'Document Metadata', icon: FileText, count: 23, status: 'idle' }
  ];

  const recentFindings = [
    { type: 'email', value: 'admin@example.com', source: 'LinkedIn', timestamp: '2 min ago' },
    { type: 'domain', value: 'api.example.com', source: 'Certificate Transparency', timestamp: '5 min ago' },
    { type: 'person', value: 'John Doe - CEO', source: 'LinkedIn', timestamp: '8 min ago' },
    { type: 'document', value: 'company-report-2024.pdf', source: 'Google Dorks', timestamp: '12 min ago' }
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">OSINT Hub</h1>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
        <div className="flex gap-2">
          <input type="text" value={target} onChange={(e) => setTarget(e.target.value)} placeholder="Enter target domain or organization..." className="flex-1 px-4 py-3 bg-white/5 rounded-lg" />
          <button className="px-6 py-3 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center gap-2 font-semibold">
            <Search className="w-5 h-5" /> Start OSINT
          </button>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4">
        {sources.map((source) => (
          <div key={source.name} className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <source.icon className="w-4 h-4 text-cyan-400" />
              <div className="text-gray-400 text-sm">{source.name}</div>
            </div>
            <div className="text-2xl font-bold">{source.count}</div>
            <div className={`text-xs mt-1 ${source.status === 'active' ? 'text-green-400' : 'text-gray-400'}`}>{source.status}</div>
          </div>
        ))}
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        <div className="p-4 border-b border-white/10">
          <h2 className="text-lg font-bold">Recent Findings</h2>
        </div>
        <div className="divide-y divide-white/10">
          {recentFindings.map((finding, idx) => (
            <div key={idx} className="p-4 hover:bg-white/5">
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="px-2 py-0.5 bg-cyan-500/20 text-cyan-400 rounded text-xs">{finding.type}</span>
                    <span className="font-mono text-sm">{finding.value}</span>
                  </div>
                  <div className="text-sm text-gray-400">Source: {finding.source}</div>
                </div>
                <div className="text-sm text-gray-400">{finding.timestamp}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
