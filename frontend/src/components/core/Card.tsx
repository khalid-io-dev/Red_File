import React from 'react';
import { LucideIcon } from 'lucide-react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'glass' | 'solid' | 'glow' | 'threat-critical' | 'threat-high' | 'threat-medium' | 'threat-low';
  hover?: boolean;
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

const Card: React.FC<CardProps> = ({
  children,
  className = '',
  variant = 'glass',
  hover = false,
  padding = 'md'
}) => {
  const baseClasses = 'rounded-xl transition-all duration-300';

  const variantClasses = {
    'glass': 'glass-panel',
    'solid': 'bg-gray-900 border border-gray-800',
    'glow': 'glow-card',
    'threat-critical': 'threat-card-critical',
    'threat-high': 'threat-card-high',
    'threat-medium': 'threat-card-medium',
    'threat-low': 'threat-card-low',
  };

  const paddingClasses = {
    'none': '',
    'sm': 'p-3',
    'md': 'p-5',
    'lg': 'p-6',
  };

  const hoverClasses = hover ? 'hover:border-cyan-500/40 hover:cyber-glow cursor-pointer' : '';

  return (
    <div className={`${baseClasses} ${variantClasses[variant]} ${paddingClasses[padding]} ${hoverClasses} ${className}`}>
      {children}
    </div>
  );
};

export default Card;

// ═══════════════════════════════════════════════════════════════════════════════
// CARD HEADER
// ═══════════════════════════════════════════════════════════════════════════════

interface CardHeaderProps {
  title: string;
  subtitle?: string;
  icon?: React.ReactNode;
  action?: React.ReactNode;
}

export const CardHeader: React.FC<CardHeaderProps> = ({ title, subtitle, icon, action }) => (
  <div className="flex items-center justify-between mb-4 pb-4 border-b border-gray-800/50">
    <div className="flex items-center gap-3">
      {icon && (
        <div className="w-8 h-8 rounded-lg bg-cyan-500/10 flex items-center justify-center text-cyan-400">
          {icon}
        </div>
      )}
      <div>
        <h3 className="text-white font-semibold">{title}</h3>
        {subtitle && <p className="text-sm text-gray-400">{subtitle}</p>}
      </div>
    </div>
    {action}
  </div>
);

// ═══════════════════════════════════════════════════════════════════════════════
// STAT CARD
// ═══════════════════════════════════════════════════════════════════════════════

interface StatCardProps {
  title: string;
  value: string | number;
  icon?: React.ReactNode;
  trend?: {
    value: number;
    direction: 'up' | 'down';
  };
  color?: 'cyan' | 'red' | 'green' | 'purple' | 'amber';
}

const colorMap = {
  cyan: { bg: 'bg-cyan-500/10', text: 'text-cyan-400', border: 'border-cyan-500/30' },
  red: { bg: 'bg-red-500/10', text: 'text-red-400', border: 'border-red-500/30' },
  green: { bg: 'bg-green-500/10', text: 'text-green-400', border: 'border-green-500/30' },
  purple: { bg: 'bg-purple-500/10', text: 'text-purple-400', border: 'border-purple-500/30' },
  amber: { bg: 'bg-amber-500/10', text: 'text-amber-400', border: 'border-amber-500/30' },
};

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  icon,
  trend,
  color = 'cyan'
}) => {
  const colors = colorMap[color];

  return (
    <Card variant="glass" hover className={`border-l-4 ${colors.border}`}>
      <div className="flex items-start justify-between">
        {icon && (
          <div className={`w-10 h-10 rounded-lg ${colors.bg} flex items-center justify-center ${colors.text}`}>
            {icon}
          </div>
        )}
        {trend && (
          <span className={`text-xs font-medium ${trend.direction === 'up' ? 'text-green-400' : 'text-red-400'}`}>
            {trend.direction === 'up' ? '↑' : '↓'} {trend.value}%
          </span>
        )}
      </div>
      <div className="mt-4">
        <p className={`text-3xl font-bold ${colors.text}`}>{value}</p>
        <p className="text-sm text-gray-400 mt-1">{title}</p>
      </div>
    </Card>
  );
};
