import React from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import CyberBackground from './CyberBackground';
import clsx from 'clsx';
import { 
  Cloud, 
  Shield, 
  Search, 
  Activity, 
  Target, 
  Server, 
  Settings,
  Database,
  Box,
  Lock,
  AlertTriangle,
  Radar,
  FileText,
  Network,
  Terminal,
  Users,
  Globe
} from 'lucide-react';

export default function Layout() {
  const { user } = useAuth();
  const location = useLocation();

  // Logout function from the original Layout
  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  const navItems = [
    { section: 'Main Module', items: [
      { to: '/', label: 'Dashboard', icon: <Activity className="w-5 h-5" /> },
      { to: '/scans', label: 'Active Scans', icon: <Search className="w-5 h-5" /> },
      { to: '/owasp', label: 'OWASP Testing', icon: <Shield className="w-5 h-5" /> },
      { to: '/agent', label: 'AI Agent', icon: <Target className="w-5 h-5" /> },
    ]},
    { section: 'Cloud Security', items: [
      { to: '/cloud-security', label: 'Cloud Dashboard', icon: <Cloud className="w-5 h-5" /> },
      { to: '/cloud/aws', label: 'AWS Scanner', icon: <Box className="w-5 h-5" /> },
      { to: '/cloud/azure', label: 'Azure Scanner', icon: <Globe className="w-5 h-5" /> },
      { to: '/cloud/gcp', label: 'GCP Scanner', icon: <Database className="w-5 h-5" /> },
      { to: '/cloud/containers', label: 'Container Scanner', icon: <Box className="w-5 h-5" /> },
      { to: '/cloud/kubernetes', label: 'Kubernetes Scanner', icon: <Network className="w-5 h-5" /> },
    ]},
    { section: 'SIEM & Monitoring', items: [
      { to: '/siem', label: 'SIEM Dashboard', icon: <Radar className="w-5 h-5" /> },
      { to: '/siem/connector', label: 'SIEM Connector', icon: <Network className="w-5 h-5" /> },
      { to: '/siem/query', label: 'Query Builder', icon: <Terminal className="w-5 h-5" /> },
      { to: '/siem/dashboards', label: 'SIEM Dashboards', icon: <Activity className="w-5 h-5" /> },
      { to: '/siem/alerts', label: 'Alert Rules', icon: <AlertTriangle className="w-5 h-5" /> },
    ]},
    { section: 'Threat Intel', items: [
      { to: '/threat-intel', label: 'Threat Dashboard', icon: <Search className="w-5 h-5" /> },
      { to: '/threat-intel/ioc', label: 'IOC Analyzer', icon: <Target className="w-5 h-5" /> },
      { to: '/threat-intel/actors', label: 'Threat Actors', icon: <AlertTriangle className="w-5 h-5" /> },
      { to: '/threat-intel/cve', label: 'CVE Browser', icon: <Shield className="w-5 h-5" /> },
    ]},
    { section: 'Defense & Monitoring', items: [
      { to: '/defense/alerts', label: 'Alerts Dashboard', icon: <AlertTriangle className="w-5 h-5" /> },
      { to: '/defense/incidents', label: 'Incident Response', icon: <Activity className="w-5 h-5" /> },
      { to: '/defense/playbooks', label: 'SOAR Playbooks', icon: <FileText className="w-5 h-5" /> },
      { to: '/defense/honeypot', label: 'Honeypot Manager', icon: <Radar className="w-5 h-5" /> },
    ]},
    { section: 'Offensive Security', items: [
      { to: '/offensive/exploits', label: 'Exploit Library', icon: <Target className="w-5 h-5" /> },
      { to: '/offensive/evasion', label: 'Evasion Studio', icon: <Lock className="w-5 h-5" /> },
      { to: '/offensive/payloads', label: 'Payload Generator', icon: <Terminal className="w-5 h-5" /> },
      { to: '/offensive/chains', label: 'Attack Chains', icon: <Network className="w-5 h-5" /> },
      { to: '/offensive/mitre', label: 'MITRE Matrix', icon: <Shield className="w-5 h-5" /> },
    ]},
    { section: 'Intelligence & Analytics', items: [
      { to: '/intel/reports', label: 'Report Generator', icon: <FileText className="w-5 h-5" /> },
      { to: '/intel/executive', label: 'Executive Dashboard', icon: <Activity className="w-5 h-5" /> },
      { to: '/intel/compliance', label: 'Compliance Reports', icon: <Shield className="w-5 h-5" /> },
      { to: '/vulnerabilities', label: 'Vulnerability Dashboard', icon: <AlertTriangle className="w-5 h-5" /> },
      { to: '/cve-explorer', label: 'CVE Explorer', icon: <Search className="w-5 h-5" /> },
    ]},
    { section: 'Asset Management', items: [
      { to: '/assets/inventory', label: 'Asset Inventory', icon: <Server className="w-5 h-5" /> },
      { to: '/assets/discovery', label: 'Asset Discovery', icon: <Radar className="w-5 h-5" /> },
      { to: '/assets/topology', label: 'Network Topology', icon: <Network className="w-5 h-5" /> },
    ]},
    { section: 'Configuration', items: [
      { to: '/config/settings', label: 'System Settings', icon: <Settings className="w-5 h-5" /> },
      { to: '/config/policies', label: 'Security Policies', icon: <Lock className="w-5 h-5" /> },
      { to: '/config/users', label: 'User Management', icon: <Users className="w-5 h-5" /> },
    ]},
    { section: 'Threat Intel (Legacy)', items: [
      { to: '/analysis', label: 'Malware Analysis', icon: <AlertTriangle className="w-5 h-5" /> },
      { to: '/honeypots', label: 'Honeypots', icon: <Radar className="w-5 h-5" /> },
    ]},
  ];

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 flex overflow-hidden relative">
      <CyberBackground />

      {/* Sidebar - Glassmorphism */}
      <aside className="w-72 bg-gray-900/60 backdrop-blur-xl border-r border-gray-800 flex flex-col z-20 shadow-[5px_0_30px_rgba(0,0,0,0.5)]">
        <div className="p-8 pb-4">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-10 h-10 rounded-xl bg-cyan-900/30 border border-cyan-500/50 shadow-[0_0_15px_rgba(8,145,178,0.4)] flex items-center justify-center">
              <span className="text-xl">🛡️</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight leading-none">Secure<span className="text-cyan-400">Sight</span></h1>
              <p className="text-[10px] text-cyan-500/80 uppercase tracking-[0.2em] font-bold mt-1">Defense System</p>
            </div>
          </div>
        </div>

        <nav className="flex-1 px-4 space-y-2 overflow-y-auto custom-scrollbar">
          {navItems.map((section) => (
            <React.Fragment key={section.section}>
              <div className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4 px-4 mt-6">{section.section}</div>
              {section.items.map((item) => (
                <NavLink 
                  key={item.to} 
                  to={item.to} 
                  active={location.pathname === item.to || location.pathname.startsWith(item.to + '/')}
                  icon={item.icon}
                >
                  {item.label}
                </NavLink>
              ))}
            </React.Fragment>
          ))}
        </nav>

        <div className="p-4 mt-auto border-t border-gray-800/50 bg-gray-900/50 backdrop-blur-sm">
          <div className="flex items-center gap-3 mb-4 p-3 rounded-lg bg-gray-950/50 border border-gray-800">
            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-cyan-600 to-blue-700 flex items-center justify-center font-bold text-sm shadow-lg text-white">
              {user?.email?.charAt(0).toUpperCase()}
            </div>
            <div className="overflow-hidden">
              <p className="text-sm font-medium text-gray-200 truncate">{user?.full_name || 'Operator'}</p>
              <p className="text-[10px] text-gray-500 truncate" title={user?.email}>{user?.email}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 text-sm py-2.5 rounded-lg border border-red-900/30 text-red-400 hover:bg-red-950/50 hover:border-red-800 hover:text-red-300 transition-all duration-200"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
            Terminate Session
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto relative z-10 p-8 custom-scrollbar">
        <div className="max-w-7xl mx-auto animate-fade-in">
          <Outlet />
        </div>
      </main>
    </div>
  );
}

const NavLink = ({ to, children, icon, active }: { to: string; children: React.ReactNode; icon: React.ReactNode; active: boolean }) => {
  return (
    <Link
      to={to}
      className={clsx(
        "flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 group relative overflow-hidden",
        active
          ? "text-white bg-cyan-900/30 border border-cyan-500/30 shadow-[0_0_15px_rgba(8,145,178,0.2)]"
          : "text-gray-400 hover:bg-gray-800/50 hover:text-cyan-300"
      )}
    >
      {active && <div className="absolute left-0 top-0 bottom-0 w-1 bg-cyan-500 shadow-[0_0_10px_rgba(6,182,212,0.8)]"></div>}
      <span className={clsx("transition-colors", active ? "text-cyan-400" : "text-gray-500 group-hover:text-cyan-400")}>
        {icon}
      </span>
      <span className="font-medium tracking-wide text-sm">{children}</span>
    </Link>
  );
};
