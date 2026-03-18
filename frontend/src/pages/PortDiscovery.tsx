import { Loader2, Search, Shield, AlertTriangle } from 'lucide-react';
import { useState } from 'react';

export default function PortDiscovery() {
  const [filter, setFilter] = useState('all');

  const ports = [
    { port: 22, service: 'SSH', state: 'open', version: 'OpenSSH 8.2', risk: 'low' },
    { port: 80, service: 'HTTP', state: 'open', version: 'Apache 2.4.41', risk: 'medium' },
    { port: 443, service: 'HTTPS', state: 'open', version: 'Apache 2.4.41', risk: 'low' },
    { port: 3306, service: 'MySQL', state: 'open', version: 'MySQL 5.7', risk: 'high' },
    { port: 8080, service: 'HTTP-Proxy', state: 'open', version: 'Tomcat 9.0', risk: 'medium' },
    { port: 21, service: 'FTP', state: 'filtered', version: 'Unknown', risk: 'high' },
    { port: 23, service: 'Telnet', state: 'closed', version: 'N/A', risk: 'critical' },
    { port: 445, service: 'SMB', state: 'open', version: 'Samba 4.11', risk: 'high' }
  ];

  const filteredPorts = filter === 'all' ? ports : ports.filter(p => p.state === filter);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Port Discovery</h1>
        <select value={filter} onChange={(e) => setFilter(e.target.value)} className="px-4 py-2 bg-white/5 rounded-lg">
          <option value="all">All Ports</option>
          <option value="open">Open</option>
          <option value="filtered">Filtered</option>
          <option value="closed">Closed</option>
        </select>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Total Ports</div>
          <div className="text-2xl font-bold">{ports.length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Open</div>
          <div className="text-2xl font-bold text-green-400">{ports.filter(p => p.state === 'open').length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Filtered</div>
          <div className="text-2xl font-bold text-yellow-400">{ports.filter(p => p.state === 'filtered').length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">High Risk</div>
          <div className="text-2xl font-bold text-red-400">{ports.filter(p => p.risk === 'high' || p.risk === 'critical').length}</div>
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        <div className="divide-y divide-white/10">
          {filteredPorts.map((port) => (
            <div key={port.port} className="p-4 hover:bg-white/5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 bg-cyan-500/20 rounded-lg flex items-center justify-center">
                    <div className="text-center">
                      <div className="text-xl font-bold text-cyan-400">{port.port}</div>
                      <div className="text-xs text-gray-400">TCP</div>
                    </div>
                  </div>
                  <div>
                    <div className="font-semibold text-lg">{port.service}</div>
                    <div className="text-sm text-gray-400">{port.version}</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`px-3 py-1 rounded text-sm ${
                    port.state === 'open' ? 'bg-green-500/20 text-green-400' :
                    port.state === 'filtered' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-gray-500/20 text-gray-400'
                  }`}>{port.state}</span>
                  <span className={`px-3 py-1 rounded text-sm ${
                    port.risk === 'critical' ? 'bg-red-500/20 text-red-400' :
                    port.risk === 'high' ? 'bg-orange-500/20 text-orange-400' :
                    port.risk === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-blue-500/20 text-blue-400'
                  }`}>{port.risk}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
