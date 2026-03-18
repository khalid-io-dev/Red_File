import { useState, useEffect } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import {
  Home, Target, Shield, Crosshair, Wrench, Search, FileText, Settings,
  Menu, X, Bell, User, LogOut, Zap, Radio, Database, Terminal,
  Brain, BarChart3, Server, ChevronRight, Command, AlertTriangle,
  Activity, Cpu, HardDrive, Wifi, Clock,
  Eye, Bug, Lock, Network, FileSearch, Users, Layers,
  Cloud, Globe, Box, Radar, Globe2, FileCheck, Map, GlobeLock
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

// Navigation structure with categories
const navigationCategories = [
  {
    name: 'Command',
    items: [
      { name: 'Dashboard', href: '/', icon: Home },
      { name: 'Activity', href: '/command-center/operations', icon: Activity },
    ]
  },
  {
    name: 'Cloud Security',
    items: [
      { name: 'Cloud Dashboard', href: '/cloud-security', icon: Cloud },
      { name: 'AWS Scanner', href: '/cloud/aws', icon: Box },
      { name: 'Azure Scanner', href: '/cloud/azure', icon: Globe },
      { name: 'GCP Scanner', href: '/cloud/gcp', icon: Globe2 },
      { name: 'Container Scanner', href: '/cloud/containers', icon: Box },
      { name: 'Kubernetes Scanner', href: '/cloud/kubernetes', icon: Map },
    ]
  },
  {
    name: 'SIEM & Monitoring',
    items: [
      { name: 'SIEM Dashboard', href: '/siem', icon: Radar },
      { name: 'SIEM Connector', href: '/siem/connector', icon: Network },
      { name: 'Query Builder', href: '/siem/query', icon: Terminal },
      { name: 'SIEM Dashboards', href: '/siem/dashboards', icon: BarChart3 },
      { name: 'Alert Rules', href: '/siem/alerts', icon: AlertTriangle },
    ]
  },
  {
    name: 'Threat Intel',
    items: [
      { name: 'Threat Dashboard', href: '/threat-intel', icon: Eye },
      { name: 'IOC Analyzer', href: '/threat-intel/ioc', icon: Target },
      { name: 'Threat Actors', href: '/threat-intel/actors', icon: Users },
      { name: 'CVE Browser', href: '/threat-intel/cve', icon: Shield },
    ]
  },
  {
    name: 'Defense & Monitoring',
    items: [
      { name: 'Alerts Dashboard', href: '/defense/alerts', icon: AlertTriangle },
      { name: 'Incident Response', href: '/defense/incidents', icon: Activity },
      { name: 'SOAR Playbooks', href: '/defense/playbooks', icon: FileText },
      { name: 'Honeypot Manager', href: '/defense/honeypot', icon: Radio },
      { name: 'Honeypots', href: '/honeypots', icon: Radio },
      { name: 'IDS/IPS', href: '/ids-ips', icon: Shield },
    ]
  },
  {
    name: 'Offensive Security',
    items: [
      { name: 'Exploit Library', href: '/offensive/exploits', icon: Bug },
      { name: 'Evasion Studio', href: '/offensive/evasion', icon: Lock },
      { name: 'Payload Generator', href: '/offensive/payloads', icon: Zap },
      { name: 'Attack Chains List', href: '/offensive/chains', icon: Layers },
      { name: 'MITRE Matrix', href: '/offensive/mitre', icon: Shield },
      { name: 'Scans', href: '/scans', icon: Target },
      { name: 'OWASP Testing', href: '/owasp', icon: Shield },
      { name: 'Exploits', href: '/exploits', icon: Bug },
      { name: 'Payloads', href: '/payloads', icon: Zap },
      { name: 'Campaigns', href: '/campaigns', icon: Crosshair },
      { name: 'Chain Executor', href: '/attack-chains/executor', icon: Layers },
      { name: 'Campaign Reasoning', href: '/campaigns/reasoning', icon: Brain },
      { name: 'Social Engineering', href: '/social-engineering', icon: Users },
      { name: 'Email Crafting', href: '/social-engineering/email-craft', icon: FileText },
    ]
  },
  {
    name: 'Intelligence & Analytics',
    items: [
      { name: 'Report Generator', href: '/intel/reports', icon: FileText },
      { name: 'Executive Dashboard', href: '/intel/executive', icon: BarChart3 },
      { name: 'Compliance Reports', href: '/intel/compliance', icon: FileCheck },
      { name: 'Vulnerability Dashboard', href: '/vulnerabilities', icon: AlertTriangle },
      { name: 'CVE Explorer', href: '/cve-explorer', icon: Search },
      { name: 'Reports', href: '/reports', icon: FileText },
      { name: 'MITRE', href: '/mitre', icon: Layers },
      { name: 'Analytics', href: '/kpi', icon: BarChart3 },
    ]
  },
  {
    name: 'Asset Management',
    items: [
      { name: 'Asset Inventory', href: '/assets/inventory', icon: Server },
      { name: 'Asset Discovery', href: '/assets/discovery', icon: Radar },
      { name: 'Network Topology', href: '/assets/topology', icon: Network },
      { name: 'Assets', href: '/assets', icon: Server },
    ]
  },
  {
    name: 'Reconnaissance',
    items: [
      { name: 'OSINT Hub', href: '/recon/osint', icon: Eye },
      { name: 'Network Scan', href: '/recon/network', icon: Network },
      { name: 'DNS Intel', href: '/recon/dns', icon: FileSearch },
      { name: 'Investigation History', href: '/recon/history', icon: Clock },
    ]
  },
  {
    name: 'AI Ops',
    items: [
      { name: 'Assistant', href: '/ai/assistant', icon: Brain },
      { name: 'Task Execution', href: '/ai/task-execution', icon: Zap },
      { name: 'MITRE Integration', href: '/ai/mitre-integration', icon: Shield },
      { name: 'Reasoning Engine', href: '/ai/reasoning-engine', icon: Cpu },
      { name: 'Agents', href: '/ai/agents', icon: Terminal },
    ]
  },
  {
    name: 'System',
    items: [
      { name: 'System Settings', href: '/config/settings', icon: Settings },
      { name: 'Security Policies', href: '/config/policies', icon: Lock },
      { name: 'User Management', href: '/config/users', icon: Users },
      { name: 'Reverse Engineering', href: '/advanced-tools/reverse-engineering', icon: Terminal },
      { name: 'Web Tools', href: '/advanced-tools/web-tools', icon: Wrench },
      { name: 'Network Tools', href: '/advanced-tools/network-tools', icon: Network },
    ]
  },
];

// System status mock data
const systemStatus = {
  cpu: 42,
  memory: 67,
  activeScans: 3,
  threats: 12,
  uptime: '14d 7h'
};

export default function MainLayout() {
  const [sidebarExpanded, setSidebarExpanded] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setSearchOpen(true);
      }
      if (e.key === 'Escape') {
        setSearchOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      {/* ═══════════════════════════════════════════════════════════════════
          COLLAPSIBLE SIDEBAR
          ═══════════════════════════════════════════════════════════════════ */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 flex flex-col bg-gray-900/80 backdrop-blur-xl 
                    border-r border-gray-800/50 transition-all duration-300 ease-in-out
                    ${sidebarExpanded ? 'w-64' : 'w-16'}`}
        onMouseEnter={() => setSidebarExpanded(true)}
        onMouseLeave={() => setSidebarExpanded(false)}
      >
        {/* Logo */}
        <div className="flex items-center h-16 px-4 border-b border-gray-800/50">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-red-600 to-red-900 flex items-center justify-center glow-red">
              <Shield className="w-5 h-5 text-red-100" />
            </div>
            <span className={`font-bold text-lg gradient-text whitespace-nowrap transition-opacity duration-200
                             ${sidebarExpanded ? 'opacity-100' : 'opacity-0 w-0'}`}>
              SecureSight
            </span>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4 overflow-y-auto overflow-x-hidden custom-scrollbar">
          {navigationCategories.map((category) => (
            <div key={category.name} className="mb-4">
              <div className={`px-4 mb-2 text-[10px] font-bold uppercase tracking-wider text-gray-500 
                              transition-opacity duration-200 ${sidebarExpanded ? 'opacity-100' : 'opacity-0'}`}>
                {category.name}
              </div>
              {category.items.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.href ||
                  (item.href !== '/' && location.pathname.startsWith(item.href));
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center gap-3 mx-2 px-3 py-2.5 rounded-lg transition-all duration-200 group
                               ${isActive
                        ? 'bg-red-500/15 text-red-400 border border-red-500/30'
                        : 'text-gray-400 hover:bg-red-500/10 hover:text-red-300'}`}
                    title={!sidebarExpanded ? item.name : undefined}
                  >
                    <Icon className={`w-5 h-5 flex-shrink-0 ${isActive ? 'text-red-400' : 'group-hover:text-red-400'}`} />
                    <span className={`text-sm font-medium whitespace-nowrap transition-opacity duration-200
                                     ${sidebarExpanded ? 'opacity-100' : 'opacity-0 w-0'}`}>
                      {item.name}
                    </span>
                    {isActive && sidebarExpanded && (
                      <ChevronRight className="w-4 h-4 ml-auto text-red-500" />
                    )}
                  </Link>
                );
              })}
            </div>
          ))}
        </nav>

        {/* Sidebar Footer - System Status */}
        <div className={`p-3 border-t border-gray-800/50 transition-opacity duration-200
                        ${sidebarExpanded ? 'opacity-100' : 'opacity-0'}`}>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="flex items-center gap-1.5 text-gray-400">
              <Cpu className="w-3 h-3" />
              <span>{systemStatus.cpu}%</span>
            </div>
            <div className="flex items-center gap-1.5 text-gray-400">
              <HardDrive className="w-3 h-3" />
              <span>{systemStatus.memory}%</span>
            </div>
          </div>
        </div>
      </aside>

      {/* ═══════════════════════════════════════════════════════════════════
          MAIN CONTENT AREA
          ═══════════════════════════════════════════════════════════════════ */}
      <div className="pl-16 min-h-screen flex flex-col">
        {/* ───────────────────────────────────────────────────────────────────
            TOP COMMAND BAR
            ─────────────────────────────────────────────────────────────────── */}
        <header className="sticky top-0 z-40 h-14 bg-gray-900/70 backdrop-blur-xl border-b border-gray-800/50">
          <div className="flex items-center justify-between h-full px-6">
            {/* Left: Breadcrumb & Status */}
            <div className="flex items-center gap-6">
              {/* System Status Indicators */}
              <div className="flex items-center gap-4 text-xs">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full status-online"></span>
                  <span className="text-gray-400">System Online</span>
                </div>
                <div className="hidden md:flex items-center gap-2 text-gray-500">
                  <Target className="w-3.5 h-3.5" />
                  <span>{systemStatus.activeScans} Active Scans</span>
                </div>
                <div className="hidden md:flex items-center gap-2 text-red-400">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>{systemStatus.threats} Threats</span>
                </div>
              </div>
            </div>

            {/* Center: Search */}
            <button
              onClick={() => setSearchOpen(true)}
              className="hidden md:flex items-center gap-3 px-4 py-1.5 bg-gray-800/50 border border-gray-700/50 
                         rounded-lg text-gray-400 hover:border-gray-600 hover:text-gray-300 transition-all"
            >
              <Search className="w-4 h-4" />
              <span className="text-sm">Search commands...</span>
              <kbd className="px-1.5 py-0.5 bg-gray-700/50 rounded text-[10px] font-mono">⌘K</kbd>
            </button>

            {/* Right: User & Actions */}
            <div className="flex items-center gap-3">
              {/* Time */}
              <div className="hidden lg:flex items-center gap-2 text-xs text-gray-500">
                <Clock className="w-3.5 h-3.5" />
                <span className="font-mono">
                  {currentTime.toLocaleTimeString('en-US', { hour12: false })}
                </span>
              </div>

              {/* Notifications */}
              <button className="relative p-2 text-gray-400 hover:text-gray-200 hover:bg-gray-800/50 rounded-lg transition-all">
                <Bell className="w-5 h-5" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
              </button>

              {/* User Menu */}
              <div className="flex items-center gap-3 pl-3 border-l border-gray-800">
                <div className="flex items-center gap-2 px-3 py-1.5 bg-gray-800/50 rounded-lg border border-gray-700/50">
                  <div className="w-6 h-6 rounded-full bg-gradient-to-br from-cyan-500 to-purple-600 flex items-center justify-center">
                    <span className="text-xs font-bold text-white">
                      {user?.email?.charAt(0).toUpperCase() || 'U'}
                    </span>
                  </div>
                  <span className="hidden md:block text-sm text-gray-300 max-w-32 truncate">
                    {user?.email || 'Operator'}
                  </span>
                </div>

                <button
                  onClick={handleLogout}
                  className="p-2 text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all"
                  title="Logout"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* ───────────────────────────────────────────────────────────────────
            PAGE CONTENT
            ─────────────────────────────────────────────────────────────────── */}
        <main className="flex-1 p-6">
          <div className="max-w-[1800px] mx-auto animate-fade-in">
            <Outlet />
          </div>
        </main>

        {/* ───────────────────────────────────────────────────────────────────
            FOOTER STATUS BAR
            ─────────────────────────────────────────────────────────────────── */}
        <footer className="h-8 px-6 bg-gray-900/50 border-t border-gray-800/50 flex items-center justify-between text-xs text-gray-500">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5">
              <Wifi className="w-3 h-3 text-green-500" />
              <span>Connected</span>
            </div>
            <span>|</span>
            <span>Uptime: {systemStatus.uptime}</span>
          </div>
          <div className="flex items-center gap-4">
            <span>SecureSight v2.0</span>
            <span>|</span>
            <span>© 2024 Red Team Framework</span>
          </div>
        </footer>
      </div>

      {/* ═══════════════════════════════════════════════════════════════════
          SEARCH MODAL (Command Palette)
          ═══════════════════════════════════════════════════════════════════ */}
      {searchOpen && (
        <div
          className="fixed inset-0 z-[100] flex items-start justify-center pt-[20vh] bg-black/60 backdrop-blur-sm"
          onClick={() => setSearchOpen(false)}
        >
          <div
            className="w-full max-w-xl bg-gray-900 border border-gray-700 rounded-xl shadow-2xl overflow-hidden animate-fade-in"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center gap-3 px-4 py-3 border-b border-gray-800">
              <Search className="w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search commands, pages, or actions..."
                className="flex-1 bg-transparent text-gray-100 placeholder-gray-500 outline-none"
                autoFocus
              />
              <kbd className="px-2 py-1 bg-gray-800 rounded text-xs text-gray-400">ESC</kbd>
            </div>
            <div className="p-2 max-h-80 overflow-y-auto">
              <div className="px-3 py-2 text-xs font-semibold text-gray-500 uppercase">Quick Actions</div>
              {[
                { name: 'New Scan', icon: Target, href: '/scans/create' },
                { name: 'View Reports', icon: FileText, href: '/reports' },
                { name: 'AI Assistant', icon: Brain, href: '/ai/assistant' },
                { name: 'System Settings', icon: Settings, href: '/settings' },
              ].map((action) => {
                const Icon = action.icon;
                return (
                  <button
                    key={action.name}
                    onClick={() => { navigate(action.href); setSearchOpen(false); }}
                    className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
                  >
                    <Icon className="w-4 h-4 text-gray-500" />
                    <span>{action.name}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
