import { Loader2, Server, Code, Database, Globe } from 'lucide-react';

export default function ServiceDetection() {
  const services = [
    { id: 1, host: '192.168.1.10', port: 22, service: 'SSH', version: 'OpenSSH 8.2p1 Ubuntu', banner: 'SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5', cpe: 'cpe:/a:openbsd:openssh:8.2p1' },
    { id: 2, host: '192.168.1.10', port: 80, service: 'HTTP', version: 'Apache httpd 2.4.41', banner: 'Apache/2.4.41 (Ubuntu)', cpe: 'cpe:/a:apache:http_server:2.4.41' },
    { id: 3, host: '192.168.1.10', port: 443, service: 'HTTPS', version: 'Apache httpd 2.4.41', banner: 'Apache/2.4.41 (Ubuntu) OpenSSL/1.1.1f', cpe: 'cpe:/a:apache:http_server:2.4.41' },
    { id: 4, host: '192.168.1.20', port: 3306, service: 'MySQL', version: 'MySQL 5.7.38', banner: '5.7.38-0ubuntu0.18.04.1', cpe: 'cpe:/a:mysql:mysql:5.7.38' },
    { id: 5, host: '192.168.1.30', port: 445, service: 'SMB', version: 'Samba 4.11.6', banner: 'Samba 4.11.6-Ubuntu', cpe: 'cpe:/a:samba:samba:4.11.6' }
  ];

  const getServiceIcon = (service: string) => {
    if (service.includes('HTTP')) return <Globe className="w-5 h-5 text-cyan-400" />;
    if (service.includes('SQL')) return <Database className="w-5 h-5 text-green-400" />;
    if (service.includes('SSH') || service.includes('SMB')) return <Server className="w-5 h-5 text-blue-400" />;
    return <Code className="w-5 h-5 text-purple-400" />;
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Service Detection</h1>

      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Services Found</div>
          <div className="text-2xl font-bold">{services.length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Unique Hosts</div>
          <div className="text-2xl font-bold">{new Set(services.map(s => s.host)).size}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Web Services</div>
          <div className="text-2xl font-bold">{services.filter(s => s.service.includes('HTTP')).length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Database Services</div>
          <div className="text-2xl font-bold">{services.filter(s => s.service.includes('SQL')).length}</div>
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        <div className="divide-y divide-white/10">
          {services.map((service) => (
            <div key={service.id} className="p-4 hover:bg-white/5">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 bg-white/5 rounded-lg flex items-center justify-center flex-shrink-0">
                  {getServiceIcon(service.service)}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="font-mono text-cyan-400">{service.host}:{service.port}</span>
                    <span className="px-2 py-0.5 bg-cyan-500/20 text-cyan-400 rounded text-xs">{service.service}</span>
                  </div>
                  <div className="text-sm text-gray-300 mb-1">{service.version}</div>
                  <div className="text-xs text-gray-400 font-mono mb-1">Banner: {service.banner}</div>
                  <div className="text-xs text-gray-500 font-mono">CPE: {service.cpe}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
