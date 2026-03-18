import { useState } from 'react';
import { Loader2, Search, Globe, ExternalLink } from 'lucide-react';

export default function DomainIntelligence() {
  const [domain, setDomain] = useState('');

  const subdomains = [
    { name: 'www.example.com', ip: '192.168.1.10', status: 'active' },
    { name: 'api.example.com', ip: '192.168.1.20', status: 'active' },
    { name: 'mail.example.com', ip: '192.168.1.30', status: 'active' },
    { name: 'ftp.example.com', ip: '192.168.1.40', status: 'inactive' },
    { name: 'dev.example.com', ip: '192.168.1.50', status: 'active' }
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Domain Intelligence</h1>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 space-y-4">
        <div className="flex gap-2">
          <input type="text" value={domain} onChange={(e) => setDomain(e.target.value)} placeholder="example.com" className="flex-1 px-4 py-2 bg-white/5 rounded-lg" />
          <button className="px-6 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center gap-2">
            <Search className="w-4 h-4" /> Enumerate
          </button>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Subdomains Found</div>
          <div className="text-2xl font-bold">{subdomains.length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Active</div>
          <div className="text-2xl font-bold text-green-400">{subdomains.filter(s => s.status === 'active').length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Unique IPs</div>
          <div className="text-2xl font-bold">{new Set(subdomains.map(s => s.ip)).size}</div>
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        <div className="p-4 border-b border-white/10">
          <h2 className="text-lg font-bold">Discovered Subdomains</h2>
        </div>
        <div className="divide-y divide-white/10">
          {subdomains.map((subdomain, idx) => (
            <div key={idx} className="p-4 hover:bg-white/5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Globe className="w-5 h-5 text-cyan-400" />
                  <div>
                    <div className="font-mono text-cyan-400">{subdomain.name}</div>
                    <div className="text-sm text-gray-400">{subdomain.ip}</div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-1 rounded text-xs ${subdomain.status === 'active' ? 'bg-green-500/20 text-green-400' : 'bg-gray-500/20 text-gray-400'}`}>
                    {subdomain.status}
                  </span>
                  <a href={`http://${subdomain.name}`} target="_blank" rel="noopener noreferrer" className="p-2 hover:bg-white/10 rounded">
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
