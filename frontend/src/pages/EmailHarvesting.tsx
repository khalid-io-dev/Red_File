import { useState } from 'react';
import { Loader2, Mail, Search, Download } from 'lucide-react';

export default function EmailHarvesting() {
  const [target, setTarget] = useState('');

  const emails = [
    { email: 'admin@example.com', source: 'LinkedIn', verified: true, role: 'Administrator' },
    { email: 'contact@example.com', source: 'Website', verified: true, role: 'Contact' },
    { email: 'support@example.com', source: 'Website', verified: true, role: 'Support' },
    { email: 'john.doe@example.com', source: 'GitHub', verified: false, role: 'Developer' },
    { email: 'jane.smith@example.com', source: 'LinkedIn', verified: true, role: 'Manager' }
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Email Harvesting</h1>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
        <div className="flex gap-2">
          <input type="text" value={target} onChange={(e) => setTarget(e.target.value)} placeholder="example.com" className="flex-1 px-4 py-2 bg-white/5 rounded-lg" />
          <button className="px-6 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center gap-2">
            <Search className="w-4 h-4" /> Harvest
          </button>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Total Emails</div>
          <div className="text-2xl font-bold">{emails.length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Verified</div>
          <div className="text-2xl font-bold text-green-400">{emails.filter(e => e.verified).length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Sources</div>
          <div className="text-2xl font-bold">{new Set(emails.map(e => e.source)).size}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <button className="w-full px-4 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center justify-center gap-2 text-sm">
            <Download className="w-4 h-4" /> Export
          </button>
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        <div className="p-4 border-b border-white/10">
          <h2 className="text-lg font-bold">Discovered Emails</h2>
        </div>
        <div className="divide-y divide-white/10">
          {emails.map((item, idx) => (
            <div key={idx} className="p-4 hover:bg-white/5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Mail className="w-5 h-5 text-cyan-400" />
                  <div>
                    <div className="font-mono text-cyan-400">{item.email}</div>
                    <div className="text-sm text-gray-400">{item.role} • {item.source}</div>
                  </div>
                </div>
                {item.verified && (
                  <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs">Verified</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
