import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, Target, Shield, Swords, Eye, Bot, BarChart3, 
  Lock, FolderOpen, Settings, ChevronDown, ChevronRight 
} from 'lucide-react';

interface NavItem {
  label: string;
  icon: React.ReactNode;
  path?: string;
  children?: NavItem[];
}

export default function Sidebar({ collapsed }: { collapsed: boolean }) {
  const location = useLocation();
  const [expanded, setExpanded] = useState<string[]>(['command-center']);

  const navItems: NavItem[] = [
    {
      label: 'Command Center',
      icon: <Home className="w-5 h-5" />,
      children: [
        { label: 'Executive', icon: null, path: '/command-center/executive' },
        { label: 'Operations', icon: null, path: '/command-center/operations' },
        { label: 'Analytics', icon: null, path: '/command-center/analytics' }
      ]
    },
    {
      label: 'Reconnaissance',
      icon: <Target className="w-5 h-5" />,
      children: [
        { label: 'OSINT Hub', icon: null, path: '/recon/osint' },
        { label: 'Network Mapping', icon: null, path: '/recon/network' },
        { label: 'Web Recon', icon: null, path: '/recon/web' },
        { label: 'Investigation History', icon: null, path: '/recon/history' }
      ]
    },
    {
      label: 'Vulnerability Assessment',
      icon: <Shield className="w-5 h-5" />,
      children: [
        { label: 'Scan Management', icon: null, path: '/scans' },
        { label: 'Vulnerabilities', icon: null, path: '/vulnerabilities' },
        { label: 'Cloud Security', icon: null, path: '/cloud-security' }
      ]
    },
    {
      label: 'Exploitation',
      icon: <Swords className="w-5 h-5" />,
      children: [
        { label: 'Exploit Database', icon: null, path: '/exploits' },
        { label: 'Attack Chains', icon: null, path: '/chains' },
        { label: 'Attack Chain Executor', icon: null, path: '/attack-chains/executor' },
        { label: 'Campaigns', icon: null, path: '/campaigns' },
        { label: 'Campaign Reasoning', icon: null, path: '/campaigns/reasoning' }
      ]
    },
    {
      label: 'Defense & Monitoring',
      icon: <Eye className="w-5 h-5" />,
      children: [
        { label: 'Honeypots', icon: null, path: '/honeypots' },
        { label: 'IDS/IPS', icon: null, path: '/ids-ips' },
        { label: 'Threat Intel', icon: null, path: '/threat-intel' }
      ]
    },
    {
      label: 'AI Operations',
      icon: <Bot className="w-5 h-5" />,
      children: [
        { label: 'AI Assistant', icon: null, path: '/ai/assistant' },
        { label: 'Task Execution', icon: null, path: '/ai/task-execution' },
        { label: 'MITRE Integration', icon: null, path: '/ai/mitre-integration' },
        { label: 'Reasoning Engine', icon: null, path: '/ai/reasoning-engine' },
        { label: 'Agents', icon: null, path: '/ai/agents' },
        { label: 'Analysis', icon: null, path: '/ai/analysis' }
      ]
    },
    {
      label: 'Intelligence',
      icon: <BarChart3 className="w-5 h-5" />,
      children: [
        { label: 'Findings', icon: null, path: '/findings' },
        { label: 'Credentials', icon: null, path: '/credentials' },
        { label: 'Reports', icon: null, path: '/reports' },
        { label: 'MITRE ATT&CK', icon: null, path: '/mitre' }
      ]
    },
    {
      label: 'Offensive Security',
      icon: <Lock className="w-5 h-5" />,
      children: [
        { label: 'Payload Generator', icon: null, path: '/payloads' },
        { label: 'Social Engineering', icon: null, path: '/social-engineering' },
        { label: 'Email Crafting', icon: null, path: '/social-engineering/email-craft' },
        { label: 'Reverse Engineering', icon: null, path: '/advanced-tools/reverse-engineering' },
        { label: 'Web Tools', icon: null, path: '/advanced-tools/web-tools' },
        { label: 'Network Tools', icon: null, path: '/advanced-tools/network-tools' },
        { label: 'Obfuscation Lab', icon: null, path: '/obfuscation' }
      ]
    },
    {
      label: 'Asset Management',
      icon: <FolderOpen className="w-5 h-5" />,
      children: [
        { label: 'Assets', icon: null, path: '/assets' },
        { label: 'Tools', icon: null, path: '/tools' },
        { label: 'Users', icon: null, path: '/users' }
      ]
    },
    { label: 'Settings', icon: <Settings className="w-5 h-5" />, path: '/settings' }
  ];

  const toggleExpand = (label: string) => {
    setExpanded(prev => 
      prev.includes(label) ? prev.filter(l => l !== label) : [...prev, label]
    );
  };

  const isActive = (path?: string) => path && location.pathname === path;

  return (
    <nav className="flex-1 p-4 overflow-y-auto">
      <div className="space-y-1">
        {navItems.map((item) => (
          <div key={item.label}>
            {item.children ? (
              <>
                <button
                  onClick={() => toggleExpand(item.label)}
                  className="w-full flex items-center justify-between px-3 py-2 text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-tertiary)] rounded-lg transition-all"
                >
                  <div className="flex items-center gap-3">
                    {item.icon}
                    {!collapsed && <span className="text-sm font-medium">{item.label}</span>}
                  </div>
                  {!collapsed && (
                    expanded.includes(item.label) ? 
                      <ChevronDown className="w-4 h-4" /> : 
                      <ChevronRight className="w-4 h-4" />
                  )}
                </button>
                {!collapsed && expanded.includes(item.label) && (
                  <div className="ml-8 mt-1 space-y-1">
                    {item.children.map((child) => (
                      <Link
                        key={child.label}
                        to={child.path!}
                        className={`block px-3 py-2 text-sm rounded-lg transition-all ${
                          isActive(child.path)
                            ? 'bg-[var(--cyber-cyan)]/10 text-[var(--cyber-cyan)] font-medium'
                            : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-tertiary)]'
                        }`}
                      >
                        {child.label}
                      </Link>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <Link
                to={item.path!}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-all ${
                  isActive(item.path)
                    ? 'bg-[var(--cyber-cyan)]/10 text-[var(--cyber-cyan)]'
                    : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-tertiary)]'
                }`}
              >
                {item.icon}
                {!collapsed && <span className="text-sm font-medium">{item.label}</span>}
              </Link>
            )}
          </div>
        ))}
      </div>
    </nav>
  );
}
