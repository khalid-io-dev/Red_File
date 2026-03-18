import React from 'react';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  icon?: React.ReactNode;
  trend?: {
    value: number;
    direction: 'up' | 'down';
  };
  color?: 'cyan' | 'red' | 'green' | 'purple' | 'amber';
  className?: string;
}

const colorConfig = {
  cyan: {
    iconBg: 'bg-cyan-500/10',
    iconColor: 'text-cyan-500',
    valueColor: 'text-cyan-400',
    border: 'border-l-cyan-500',
    glow: 'hover:shadow-[0_0_20px_rgba(6,182,212,0.15)]'
  },
  red: {
    iconBg: 'bg-red-500/10',
    iconColor: 'text-red-500',
    valueColor: 'text-red-400',
    border: 'border-l-red-500',
    glow: 'hover:shadow-[0_0_20px_rgba(239,68,68,0.15)]'
  },
  green: {
    iconBg: 'bg-green-500/10',
    iconColor: 'text-green-500',
    valueColor: 'text-green-400',
    border: 'border-l-green-500',
    glow: 'hover:shadow-[0_0_20px_rgba(34,197,94,0.15)]'
  },
  purple: {
    iconBg: 'bg-purple-500/10',
    iconColor: 'text-purple-500',
    valueColor: 'text-purple-400',
    border: 'border-l-purple-500',
    glow: 'hover:shadow-[0_0_20px_rgba(168,85,247,0.15)]'
  },
  amber: {
    iconBg: 'bg-amber-500/10',
    iconColor: 'text-amber-500',
    valueColor: 'text-amber-400',
    border: 'border-l-amber-500',
    glow: 'hover:shadow-[0_0_20px_rgba(245,158,11,0.15)]'
  },
};

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  icon,
  trend,
  color = 'cyan',
  className = ''
}) => {
  const config = colorConfig[color];

  return (
    <div className={`
      glass-panel p-5 rounded-xl border-l-4 ${config.border}
      transition-all duration-300 ${config.glow}
      ${className}
    `}>
      <div className="flex items-start justify-between mb-4">
        {icon && (
          <div className={`w-10 h-10 rounded-lg ${config.iconBg} flex items-center justify-center ${config.iconColor}`}>
            {icon}
          </div>
        )}
        {trend && (
          <div className={`flex items-center gap-1 text-xs font-medium 
                          ${trend.direction === 'up' ? 'text-green-400' : 'text-red-400'}`}>
            {trend.direction === 'up'
              ? <ArrowUpRight className="w-3.5 h-3.5" />
              : <ArrowDownRight className="w-3.5 h-3.5" />
            }
            <span>{trend.value}%</span>
          </div>
        )}
      </div>

      <div>
        <p className={`text-3xl font-bold tracking-tight ${config.valueColor}`}>
          {value}
        </p>
        <p className="text-sm text-gray-400 mt-1">{title}</p>
      </div>
    </div>
  );
};

export default StatCard;
