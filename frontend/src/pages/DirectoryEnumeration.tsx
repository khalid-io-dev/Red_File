import { useState } from 'react';
import { Loader2, Search, Folder, File, Lock } from 'lucide-react';

export default function DirectoryEnumeration() {
  const [target, setTarget] = useState('');
  const [wordlist, setWordlist] = useState('common.txt');

  const directories = [
    { path: '/admin', status: 403, size: '-', type: 'directory' },
    { path: '/api', status: 200, size: '-', type: 'directory' },
    { path: '/backup', status: 200, size: '-', type: 'directory' },
    { path: '/config.php', status: 403, size: '2.1 KB', type: 'file' },
    { path: '/uploads', status: 200, size: '-', type: 'directory' },
    { path: '/robots.txt', status: 200, size: '156 B', type: 'file' },
    { path: '/.git', status: 403, size: '-', type: 'directory' },
    { path: '/phpinfo.php', status: 200, size: '68 KB', type: 'file' }
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Directory Enumeration</h1>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 space-y-4">
        <div className="flex gap-2">
          <input type="text" value={target} onChange={(e) => setTarget(e.target.value)} placeholder="https://example.com" className="flex-1 px-4 py-2 bg-white/5 rounded-lg" />
          <select value={wordlist} onChange={(e) => setWordlist(e.target.value)} className="px-4 py-2 bg-white/5 rounded-lg">
            <option value="common.txt">common.txt</option>
            <option value="big.txt">big.txt</option>
            <option value="directory-list-2.3-medium.txt">directory-list-2.3-medium.txt</option>
          </select>
          <button className="px-6 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center gap-2">
            <Search className="w-4 h-4" /> Enumerate
          </button>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Total Found</div>
          <div className="text-2xl font-bold">{directories.length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Accessible</div>
          <div className="text-2xl font-bold text-green-400">{directories.filter(d => d.status === 200).length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Forbidden</div>
          <div className="text-2xl font-bold text-orange-400">{directories.filter(d => d.status === 403).length}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Directories</div>
          <div className="text-2xl font-bold">{directories.filter(d => d.type === 'directory').length}</div>
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        <div className="p-4 border-b border-white/10">
          <h2 className="text-lg font-bold">Discovered Paths</h2>
        </div>
        <div className="divide-y divide-white/10">
          {directories.map((dir, idx) => (
            <div key={idx} className="p-4 hover:bg-white/5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {dir.type === 'directory' ? (
                    <Folder className="w-5 h-5 text-cyan-400" />
                  ) : (
                    <File className="w-5 h-5 text-blue-400" />
                  )}
                  <div>
                    <div className="font-mono text-cyan-400">{dir.path}</div>
                    <div className="text-sm text-gray-400">{dir.size}</div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {dir.status === 403 && <Lock className="w-4 h-4 text-orange-400" />}
                  <span className={`px-2 py-1 rounded text-xs ${
                    dir.status === 200 ? 'bg-green-500/20 text-green-400' :
                    'bg-orange-500/20 text-orange-400'
                  }`}>{dir.status}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
