import { useState } from 'react';
import { Loader2, Search, Database } from 'lucide-react';

export default function DNSIntelligence() {
  const [domain, setDomain] = useState('');

  const records = [
    { type: 'A', name: 'example.com', value: '192.168.1.10', ttl: 3600 },
    { type: 'A', name: 'www.example.com', value: '192.168.1.10', ttl: 3600 },
    { type: 'MX', name: 'example.com', value: 'mail.example.com (10)', ttl: 3600 },
    { type: 'TXT', name: 'example.com', value: 'v=spf1 include:_spf.google.com ~all', ttl: 3600 },
    { type: 'NS', name: 'example.com', value: 'ns1.example.com', ttl: 86400 },
    { type: 'NS', name: 'example.com', value: 'ns2.example.com', ttl: 86400 },
    { type: 'CNAME', name: 'api.example.com', value: 'example.com', ttl: 3600 }
  ];

  const recordTypes = ['A', 'MX', 'TXT', 'NS', 'CNAME'];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">DNS Intelligence</h1>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
        <div className="flex gap-2">
          <input type="text" value={domain} onChange={(e) => setDomain(e.target.value)} placeholder="example.com" className="flex-1 px-4 py-2 bg-white/5 rounded-lg" />
          <button className="px-6 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center gap-2">
            <Search className="w-4 h-4" /> Query
          </button>
        </div>
      </div>

      <div className="grid grid-cols-5 gap-4">
        {recordTypes.map((type) => (
          <div key={type} className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
            <div className="text-gray-400 text-sm">{type} Records</div>
            <div className="text-2xl font-bold">{records.filter(r => r.type === type).length}</div>
          </div>
        ))}
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        <div className="p-4 border-b border-white/10">
          <h2 className="text-lg font-bold">DNS Records</h2>
        </div>
        <div className="divide-y divide-white/10">
          {records.map((record, idx) => (
            <div key={idx} className="p-4 hover:bg-white/5">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3 flex-1">
                  <span className="px-2 py-1 bg-cyan-500/20 text-cyan-400 rounded text-xs font-mono">{record.type}</span>
                  <div className="flex-1">
                    <div className="font-mono text-sm text-cyan-400 mb-1">{record.name}</div>
                    <div className="text-sm text-gray-300">{record.value}</div>
                  </div>
                </div>
                <div className="text-sm text-gray-400">TTL: {record.ttl}s</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
