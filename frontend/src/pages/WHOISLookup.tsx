import { useState } from 'react';
import { Loader2, Search, Info } from 'lucide-react';

export default function WHOISLookup() {
  const [domain, setDomain] = useState('');

  const whoisData = {
    domain: 'example.com',
    registrar: 'GoDaddy.com, LLC',
    created: '1995-08-14',
    expires: '2025-08-13',
    updated: '2024-07-15',
    status: ['clientTransferProhibited', 'clientUpdateProhibited'],
    nameservers: ['ns1.example.com', 'ns2.example.com'],
    registrant: {
      organization: 'Example Organization',
      country: 'US',
      state: 'California',
      email: 'admin@example.com'
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">WHOIS Lookup</h1>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
        <div className="flex gap-2">
          <input type="text" value={domain} onChange={(e) => setDomain(e.target.value)} placeholder="example.com" className="flex-1 px-4 py-2 bg-white/5 rounded-lg" />
          <button className="px-6 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center gap-2">
            <Search className="w-4 h-4" /> Lookup
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 space-y-4">
          <h2 className="text-lg font-bold flex items-center gap-2">
            <Info className="w-5 h-5 text-cyan-400" />
            Domain Information
          </h2>
          <div className="space-y-3">
            <div>
              <div className="text-sm text-gray-400">Domain</div>
              <div className="font-mono text-cyan-400">{whoisData.domain}</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">Registrar</div>
              <div>{whoisData.registrar}</div>
            </div>
            <div className="grid grid-cols-3 gap-3">
              <div>
                <div className="text-sm text-gray-400">Created</div>
                <div className="text-sm">{whoisData.created}</div>
              </div>
              <div>
                <div className="text-sm text-gray-400">Expires</div>
                <div className="text-sm">{whoisData.expires}</div>
              </div>
              <div>
                <div className="text-sm text-gray-400">Updated</div>
                <div className="text-sm">{whoisData.updated}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 space-y-4">
          <h2 className="text-lg font-bold">Registrant Information</h2>
          <div className="space-y-3">
            <div>
              <div className="text-sm text-gray-400">Organization</div>
              <div>{whoisData.registrant.organization}</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">Location</div>
              <div>{whoisData.registrant.state}, {whoisData.registrant.country}</div>
            </div>
            <div>
              <div className="text-sm text-gray-400">Email</div>
              <div className="font-mono text-sm">{whoisData.registrant.email}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
        <h2 className="text-lg font-bold mb-4">Name Servers</h2>
        <div className="space-y-2">
          {whoisData.nameservers.map((ns, idx) => (
            <div key={idx} className="bg-white/5 rounded-lg p-3 font-mono text-sm">{ns}</div>
          ))}
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
        <h2 className="text-lg font-bold mb-4">Domain Status</h2>
        <div className="flex flex-wrap gap-2">
          {whoisData.status.map((status, idx) => (
            <span key={idx} className="px-3 py-1 bg-cyan-500/20 text-cyan-400 rounded text-sm">{status}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
