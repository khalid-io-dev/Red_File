import { Loader2, Eye, Shield, Database, Globe } from 'lucide-react';

export default function PassiveRecon() {
  const tools = [
    { name: 'WHOIS Lookup', description: 'Domain registration information', icon: Database, status: 'ready' },
    { name: 'DNS Enumeration', description: 'DNS records and subdomains', icon: Globe, status: 'ready' },
    { name: 'Certificate Transparency', description: 'SSL/TLS certificate logs', icon: Shield, status: 'ready' },
    { name: 'Shodan Search', description: 'Internet-connected devices', icon: Eye, status: 'ready' }
  ];

  const results = [
    { tool: 'WHOIS', data: 'Registrar: GoDaddy | Created: 2020-01-15', timestamp: '1 min ago' },
    { tool: 'DNS', data: 'Found 12 subdomains: api, www, mail, ftp...', timestamp: '3 min ago' },
    { tool: 'Certificate', data: '5 certificates found for *.example.com', timestamp: '5 min ago' }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Passive Reconnaissance</h1>
        <p className="text-gray-400">Non-intrusive information gathering</p>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {tools.map((tool) => (
          <div key={tool.name} className="bg-white/5 backdrop-blur-sm rounded-lg p-6 hover:bg-white/10">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-cyan-500/20 rounded-lg flex items-center justify-center">
                <tool.icon className="w-6 h-6 text-cyan-400" />
              </div>
              <div className="flex-1">
                <div className="font-bold mb-1">{tool.name}</div>
                <div className="text-sm text-gray-400 mb-3">{tool.description}</div>
                <button className="px-4 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg text-sm">
                  Run Tool
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        <div className="p-4 border-b border-white/10">
          <h2 className="text-lg font-bold">Recent Results</h2>
        </div>
        {results.length > 0 ? (
          <div className="divide-y divide-white/10">
            {results.map((result, idx) => (
              <div key={idx} className="p-4 hover:bg-white/5">
                <div className="flex items-center justify-between mb-2">
                  <span className="px-2 py-1 bg-cyan-500/20 text-cyan-400 rounded text-sm">{result.tool}</span>
                  <span className="text-sm text-gray-400">{result.timestamp}</span>
                </div>
                <div className="text-sm text-gray-300">{result.data}</div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center text-gray-400 py-12">No results yet</div>
        )}
      </div>
    </div>
  );
}
