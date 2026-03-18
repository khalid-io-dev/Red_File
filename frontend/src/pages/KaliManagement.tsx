import React, { useState, useEffect } from 'react';
import { Terminal, Server, Cpu, HardDrive, RefreshCw, Power, Settings, Activity, Shield } from 'lucide-react';

interface KaliVMStatus {
  connected: boolean;
  cpu: number;
  memory: number;
  disk: number;
  uptime: string;
  lastSync: string;
}

const KaliManagement: React.FC = () => {
  const [status, setStatus] = useState<KaliVMStatus>({
    connected: true,
    cpu: 45,
    memory: 62,
    disk: 38,
    uptime: '4d 12h 30m',
    lastSync: '2 minutes ago'
  });
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedTool, setSelectedTool] = useState<string>('');
  const [command, setCommand] = useState<string>('');
  const [output, setOutput] = useState<string>('');

  const tools = [
    { id: 'nmap', name: 'Nmap', category: 'Network Scanner' },
    { id: 'metasploit', name: 'Metasploit', category: 'Exploitation' },
    { id: 'burp', name: 'Burp Suite', category: 'Web Security' },
    { id: 'wireshark', name: 'Wireshark', category: 'Network Analysis' },
    { id: 'aircrack', name: 'Aircrack-ng', category: 'Wireless' },
    { id: 'john', name: 'John the Ripper', category: 'Password Cracking' },
    { id: 'sqlmap', name: 'SQLMap', category: 'SQL Injection' },
    { id: 'nikto', name: 'Nikto', category: 'Web Scanner' },
    { id: 'gobuster', name: 'Gobuster', category: 'Directory Busting' },
    { id: 'hydra', name: 'Hydra', category: 'Brute Force' },
    { id: 'responder', name: 'Responder', category: 'Network Attack' },
    { id: 'bloodhound', name: 'BloodHound', category: 'AD Analysis' }
  ];

  const refreshStatus = () => {
    setLoading(true);
    setTimeout(() => {
      setStatus(prev => ({
        ...prev,
        lastSync: 'Just now',
        cpu: Math.floor(Math.random() * 60) + 20,
        memory: Math.floor(Math.random() * 40) + 40
      }));
      setLoading(false);
    }, 1000);
  };

  const executeCommand = () => {
    if (!command.trim()) return;
    setLoading(true);
    setOutput(`[+] Executing: ${command}\n\n[*] Connecting to Kali VM (192.168.56.101)...\n[*] Command execution simulated.\n[+] Output captured.\n\n$ ${command}\nCommand completed successfully.`);
    setTimeout(() => setLoading(false), 1500);
  };

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Terminal className="w-8 h-8 text-purple-500" />
          <div>
            <h1 className="text-2xl font-bold text-white">Kali Linux VM</h1>
            <p className="text-gray-400">Manage your Kali Linux penetration testing environment</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={refreshStatus} disabled={loading} className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white rounded px-4 py-2 text-sm disabled:opacity-50">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
          <button className="flex items-center gap-2 bg-gray-600 hover:bg-gray-700 text-white rounded px-4 py-2 text-sm">
            <Settings className="w-4 h-4" />
            Settings
          </button>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-800 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Server className="w-8 h-8 text-green-500" />
              <div>
                <p className="text-gray-400 text-sm">Status</p>
                <p className={`font-medium ${status.connected ? 'text-green-400' : 'text-red-400'}`}>
                  {status.connected ? 'Connected' : 'Disconnected'}
                </p>
              </div>
            </div>
            <Power className={`w-5 h-5 ${status.connected ? 'text-green-500' : 'text-red-500'}`} />
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-4">
          <div className="flex items-center gap-3 mb-2">
            <Cpu className="w-6 h-6 text-blue-500" />
            <p className="text-gray-400 text-sm">CPU Usage</p>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-2xl font-bold text-white">{status.cpu}%</span>
            <div className="w-24 h-2 bg-gray-700 rounded-full overflow-hidden">
              <div className="h-full bg-blue-500 rounded-full" style={{ width: `${status.cpu}%` }}></div>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-4">
          <div className="flex items-center gap-3 mb-2">
            <Activity className="w-6 h-6 text-yellow-500" />
            <p className="text-gray-400 text-sm">Memory</p>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-2xl font-bold text-white">{status.memory}%</span>
            <div className="w-24 h-2 bg-gray-700 rounded-full overflow-hidden">
              <div className="h-full bg-yellow-500 rounded-full" style={{ width: `${status.memory}%` }}></div>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-4">
          <div className="flex items-center gap-3 mb-2">
            <HardDrive className="w-6 h-6 text-purple-500" />
            <p className="text-gray-400 text-sm">Uptime</p>
          </div>
          <p className="text-2xl font-bold text-white">{status.uptime}</p>
          <p className="text-xs text-gray-500 mt-1">Last sync: {status.lastSync}</p>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-4">
          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="text-white font-medium mb-4 flex items-center gap-2">
              <Shield className="w-5 h-5 text-purple-500" />
              Available Tools
            </h3>
            <div className="space-y-2 max-h-[400px] overflow-y-auto">
              {tools.map(tool => (
                <div
                  key={tool.id}
                  onClick={() => setSelectedTool(tool.id)}
                  className={`p-3 rounded cursor-pointer transition-colors ${
                    selectedTool === tool.id ? 'bg-purple-600' : 'bg-gray-700 hover:bg-gray-600'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-white font-medium">{tool.name}</span>
                    <span className="text-xs text-gray-400">{tool.category}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="col-span-8">
          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="text-white font-medium mb-4">Command Execution</h3>
            <div className="flex items-center gap-2 mb-4">
              <input
                type="text"
                value={command}
                onChange={(e) => setCommand(e.target.value)}
                placeholder="Enter command (e.g., nmap -sV 192.168.1.1)"
                className="flex-1 bg-gray-700 text-white rounded px-4 py-2 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              <button
                onClick={executeCommand}
                disabled={loading || !command.trim()}
                className="bg-purple-600 hover:bg-purple-700 text-white rounded px-6 py-2 text-sm font-medium disabled:opacity-50"
              >
                Execute
              </button>
            </div>

            <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm min-h-[300px]">
              <div className="flex items-center gap-2 text-gray-500 mb-2">
                <Terminal className="w-4 h-4" />
                <span>Output</span>
              </div>
              <pre className="text-green-400 whitespace-pre-wrap">
                {output || 'Ready for command execution...\n\n$ '}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KaliManagement;
