import { useState } from 'react';
import { Loader2, Search, Globe, Code, Shield } from 'lucide-react';

export default function WebRecon() {
  const [url, setUrl] = useState('');

  const findings = [
    { category: 'Technology', icon: Code, items: ['Apache 2.4.41', 'PHP 7.4', 'MySQL 5.7', 'jQuery 3.5.1'] },
    { category: 'Security Headers', icon: Shield, items: ['X-Frame-Options: DENY', 'X-Content-Type-Options: nosniff', 'Missing: CSP'] },
    { category: 'Cookies', icon: Globe, items: ['PHPSESSID (HttpOnly)', 'session_token (Secure)'] }
  ];

  const endpoints = [
    { path: '/admin', status: 403, method: 'GET' },
    { path: '/api/v1', status: 200, method: 'GET' },
    { path: '/login', status: 200, method: 'GET' },
    { path: '/backup', status: 404, method: 'GET' }
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Web Reconnaissance</h1>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
        <div className="flex gap-2">
          <input type="text" value={url} onChange={(e) => setUrl(e.target.value)} placeholder="https://example.com" className="flex-1 px-4 py-2 bg-white/5 rounded-lg" />
          <button className="px-6 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center gap-2">
            <Search className="w-4 h-4" /> Analyze
          </button>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {findings.map((finding) => (
          <div key={finding.category} className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <finding.icon className="w-5 h-5 text-cyan-400" />
              <h3 className="font-bold">{finding.category}</h3>
            </div>
            <div className="space-y-2">
              {finding.items.map((item, idx) => (
                <div key={idx} className="text-sm text-gray-300 bg-white/5 rounded px-3 py-2">{item}</div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        <div className="p-4 border-b border-white/10">
          <h2 className="text-lg font-bold">Discovered Endpoints</h2>
        </div>
        <div className="divide-y divide-white/10">
          {endpoints.map((endpoint, idx) => (
            <div key={idx} className="p-4 hover:bg-white/5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs font-mono">{endpoint.method}</span>
                  <span className="font-mono text-cyan-400">{endpoint.path}</span>
                </div>
                <span className={`px-2 py-1 rounded text-xs ${
                  endpoint.status === 200 ? 'bg-green-500/20 text-green-400' :
                  endpoint.status === 403 ? 'bg-orange-500/20 text-orange-400' :
                  'bg-gray-500/20 text-gray-400'
                }`}>{endpoint.status}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
