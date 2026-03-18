import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Menu, X, Search, Bell, User, Settings } from 'lucide-react';
import Sidebar from './Sidebar';

export default function AppShell() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] flex">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-[280px]' : 'w-[80px]'} bg-[var(--bg-secondary)] border-r border-[var(--border-primary)] transition-all duration-300 flex flex-col`}>
        <div className="h-16 flex items-center justify-between px-6 border-b border-[var(--border-primary)]">
          {sidebarOpen && (
            <h1 className="text-xl font-bold text-[var(--cyber-cyan)] font-[var(--font-display)]">
              SecureSight
            </h1>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 hover:bg-[var(--bg-tertiary)] rounded-lg transition-colors"
          >
            {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
        
        <Sidebar collapsed={!sidebarOpen} />
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <header className="h-16 bg-[var(--bg-secondary)] border-b border-[var(--border-primary)] flex items-center justify-between px-6">
          <div className="flex items-center gap-4 flex-1 max-w-2xl">
            <Search className="w-5 h-5 text-[var(--text-tertiary)]" />
            <input
              type="text"
              placeholder="Search anything..."
              className="flex-1 bg-[var(--bg-tertiary)] border border-[var(--border-primary)] rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-[var(--border-focus)]"
            />
          </div>
          
          <div className="flex items-center gap-4">
            <button className="p-2 hover:bg-[var(--bg-tertiary)] rounded-lg transition-colors relative">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-[var(--critical)] rounded-full"></span>
            </button>
            <button className="p-2 hover:bg-[var(--bg-tertiary)] rounded-lg transition-colors">
              <Settings className="w-5 h-5" />
            </button>
            <button className="flex items-center gap-2 p-2 hover:bg-[var(--bg-tertiary)] rounded-lg transition-colors">
              <User className="w-5 h-5" />
              <span className="text-sm">Admin</span>
            </button>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
