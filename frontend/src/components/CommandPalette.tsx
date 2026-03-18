import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Target, Rocket, FileText, Settings, Zap } from 'lucide-react';

interface Command {
  id: string;
  label: string;
  icon: any;
  action: () => void;
  keywords: string[];
}

export default function CommandPalette() {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const navigate = useNavigate();
  const inputRef = useRef<HTMLInputElement>(null);

  const commands: Command[] = [
    { id: 'new-scan', label: 'New Scan', icon: Target, action: () => navigate('/scans'), keywords: ['scan', 'new', 'create'] },
    { id: 'new-campaign', label: 'New Campaign', icon: Rocket, action: () => navigate('/campaigns'), keywords: ['campaign', 'new', 'create'] },
    { id: 'execute-chain', label: 'Execute Attack Chain', icon: Zap, action: () => navigate('/attack-chain'), keywords: ['attack', 'chain', 'execute'] },
    { id: 'view-findings', label: 'View Findings', icon: Search, action: () => navigate('/findings'), keywords: ['findings', 'vulnerabilities'] },
    { id: 'view-reports', label: 'View Reports', icon: FileText, action: () => navigate('/reports'), keywords: ['reports', 'export'] },
    { id: 'settings', label: 'Settings', icon: Settings, action: () => navigate('/settings'), keywords: ['settings', 'config'] },
  ];

  const filteredCommands = commands.filter(cmd =>
    cmd.label.toLowerCase().includes(search.toLowerCase()) ||
    cmd.keywords.some(k => k.includes(search.toLowerCase()))
  );

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(true);
      }
      if (e.key === 'Escape') {
        setIsOpen(false);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  const executeCommand = (cmd: Command) => {
    cmd.action();
    setIsOpen(false);
    setSearch('');
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 bg-black/50 backdrop-blur-sm">
      <div className="w-full max-w-2xl glass-panel border-2 border-cyan-500/30 shadow-2xl">
        <div className="p-4 border-b border-gray-700">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              ref={inputRef}
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Type a command or search..."
              className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:border-cyan-500 focus:outline-none"
            />
          </div>
        </div>

        <div className="max-h-96 overflow-y-auto p-2">
          {filteredCommands.length === 0 ? (
            <div className="p-8 text-center text-gray-500">No commands found</div>
          ) : (
            filteredCommands.map((cmd) => {
              const Icon = cmd.icon;
              return (
                <button
                  key={cmd.id}
                  onClick={() => executeCommand(cmd)}
                  className="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-800 text-left transition-colors"
                >
                  <Icon className="w-5 h-5 text-cyan-400" />
                  <span className="text-gray-300">{cmd.label}</span>
                </button>
              );
            })
          )}
        </div>

        <div className="p-3 border-t border-gray-700 flex items-center justify-between text-xs text-gray-500">
          <span>Press ESC to close</span>
          <span>Cmd+K to open</span>
        </div>
      </div>
    </div>
  );
}
