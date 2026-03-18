import React, { useState } from 'react';
import { Wrench, Terminal, Search, Play, Settings, Shield, Cpu, Database, Globe, Lock } from 'lucide-react';

const AdvancedToolsPage: React.FC = () => {
  const [selectedTool, setSelectedTool] = useState<string | null>(null);
  const [output, setOutput] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const tools = [
    {
      id: 'reverse-engineering',
      name: 'Reverse Engineering',
      description: 'Binary analysis and reverse engineering tools',
      icon: Cpu,
      category: 'Analysis'
    },
    {
      id: 'forensics',
      name: 'Digital Forensics',
      description: 'Forensic analysis and data recovery',
      icon: Database,
      category: 'Forensics'
    },
    {
      id: 'web-tools',
      name: 'Advanced Web Tools',
      description: 'Web application security testing',
      icon: Globe,
      category: 'Web Security'
    },
    {
      id: 'network-tools',
      name: 'Network Tools',
      description: 'Network analysis and manipulation tools',
      icon: Shield,
      category: 'Network'
    },
    {
      id: 'cryptography',
      name: 'Cryptography',
      description: 'Encryption, decryption and cryptanalysis',
      icon: Lock,
      category: 'Crypto'
    }
  ];

  const runTool = (toolId: string) => {
    setLoading(true);
    setSelectedTool(toolId);
    setOutput(`Running ${toolId}...\n\n[+] Initializing tool...\n[+] Loading modules...\n[+] Tool execution simulated.\n[+] Completed in 0.45s`);
    
    setTimeout(() => {
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="p-6">
      <div className="flex items-center gap-3 mb-6">
        <Wrench className="w-8 h-8 text-blue-500" />
        <div>
          <h1 className="text-2xl font-bold text-white">Advanced Tools</h1>
          <p className="text-gray-400">Specialized security tools and utilities</p>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6">
        {/* Tools Grid */}
        <div className="col-span-8">
          <div className="grid grid-cols-3 gap-4">
            {tools.map(tool => (
              <div
                key={tool.id}
                onClick={() => setSelectedTool(tool.id)}
                className={`bg-gray-800 rounded-lg p-4 cursor-pointer transition-all hover:scale-105 ${
                  selectedTool === tool.id ? 'ring-2 ring-blue-500' : ''
                }`}
              >
                <tool.icon className="w-10 h-10 text-blue-400 mb-3" />
                <h3 className="text-white font-medium">{tool.name}</h3>
                <p className="text-gray-400 text-sm mt-1">{tool.description}</p>
                <span className="text-xs text-gray-500 mt-2 block">{tool.category}</span>
              </div>
            ))}
          </div>

          {/* Tool Execution Area */}
          {selectedTool && (
            <div className="mt-6 bg-gray-800 rounded-lg p-4">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <Terminal className="w-5 h-5 text-blue-500" />
                  <h3 className="text-white font-medium">{tools.find(t => t.id === selectedTool)?.name}</h3>
                </div>
                <div className="flex items-center gap-2">
                  <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white rounded px-4 py-2 text-sm">
                    <Settings className="w-4 h-4" />
                    Configure
                  </button>
                  <button
                    onClick={() => runTool(selectedTool)}
                    disabled={loading}
                    className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white rounded px-4 py-2 text-sm disabled:opacity-50"
                  >
                    <Play className="w-4 h-4" />
                    {loading ? 'Running...' : 'Execute'}
                  </button>
                </div>
              </div>

              <div className="bg-gray-900 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Search className="w-4 h-4 text-gray-500" />
                  <input
                    type="text"
                    placeholder="Enter target or parameters..."
                    className="flex-1 bg-gray-800 text-white rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div className="bg-black rounded p-4 mt-4 font-mono text-sm text-green-400 min-h-[200px]">
                  {output || 'Ready to execute...'}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="col-span-4">
          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="text-white font-medium mb-4">Tool Categories</h3>
            <div className="space-y-2">
              {['Analysis', 'Forensics', 'Web Security', 'Network', 'Crypto'].map(cat => (
                <div key={cat} className="flex items-center justify-between p-2 bg-gray-700 rounded">
                  <span className="text-gray-300 text-sm">{cat}</span>
                  <span className="text-blue-400 text-xs">{tools.filter(t => t.category === cat).length}</span>
                </div>
              ))}
            </div>

            <div className="mt-6 pt-4 border-t border-gray-700">
              <h3 className="text-white font-medium mb-4">Recent Activity</h3>
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2 text-gray-400">
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  Reverse Engineering - Completed
                </div>
                <div className="flex items-center gap-2 text-gray-400">
                  <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                  Network Scan - In Progress
                </div>
                <div className="flex items-center gap-2 text-gray-400">
                  <span className="w-2 h-2 bg-gray-500 rounded-full"></span>
                  Forensics Analysis - Pending
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdvancedToolsPage;
