import React, { useState } from 'react';

interface Tab {
  id: string;
  label: string;
  icon?: React.ReactNode;
  badge?: number;
}

interface TabsProps {
  tabs: Tab[];
  defaultTab?: string;
  onChange?: (tabId: string) => void;
  children: React.ReactNode;
}

export default function Tabs({ tabs, defaultTab, onChange, children }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id);

  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId);
    onChange?.(tabId);
  };

  return (
    <div>
      <div className="border-b border-[var(--border-primary)]">
        <div className="flex gap-1">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => handleTabChange(tab.id)}
              className={`
                flex items-center gap-2 px-4 py-3
                font-medium text-sm
                border-b-2 transition-all
                ${activeTab === tab.id
                  ? 'border-[var(--cyber-cyan)] text-[var(--cyber-cyan)]'
                  : 'border-transparent text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:border-[var(--border-secondary)]'
                }
              `}
            >
              {tab.icon}
              {tab.label}
              {tab.badge !== undefined && (
                <span className="px-2 py-0.5 text-xs rounded-full bg-[var(--bg-tertiary)] text-[var(--text-secondary)]">
                  {tab.badge}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>
      
      <div className="mt-6">
        {children}
      </div>
    </div>
  );
}
