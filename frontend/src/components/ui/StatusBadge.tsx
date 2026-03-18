import React from 'react';

interface StatusBadgeProps {
    status: 'online' | 'offline' | 'warning' | 'critical' | 'running' | 'completed' | 'failed' | 'pending';
    label?: string;
    pulse?: boolean;
    size?: 'sm' | 'md' | 'lg';
}

const statusConfig = {
    online: {
        bg: 'bg-green-500/10',
        text: 'text-green-400',
        border: 'border-green-500/30',
        dot: 'bg-green-500',
        label: 'Online'
    },
    offline: {
        bg: 'bg-gray-500/10',
        text: 'text-gray-400',
        border: 'border-gray-500/30',
        dot: 'bg-gray-500',
        label: 'Offline'
    },
    warning: {
        bg: 'bg-amber-500/10',
        text: 'text-amber-400',
        border: 'border-amber-500/30',
        dot: 'bg-amber-500',
        label: 'Warning'
    },
    critical: {
        bg: 'bg-red-500/10',
        text: 'text-red-400',
        border: 'border-red-500/30',
        dot: 'bg-red-500',
        label: 'Critical'
    },
    running: {
        bg: 'bg-cyan-500/10',
        text: 'text-cyan-400',
        border: 'border-cyan-500/30',
        dot: 'bg-cyan-500',
        label: 'Running'
    },
    completed: {
        bg: 'bg-green-500/10',
        text: 'text-green-400',
        border: 'border-green-500/30',
        dot: 'bg-green-500',
        label: 'Completed'
    },
    failed: {
        bg: 'bg-red-500/10',
        text: 'text-red-400',
        border: 'border-red-500/30',
        dot: 'bg-red-500',
        label: 'Failed'
    },
    pending: {
        bg: 'bg-gray-500/10',
        text: 'text-gray-400',
        border: 'border-gray-500/30',
        dot: 'bg-gray-500',
        label: 'Pending'
    },
};

const sizeConfig = {
    sm: { badge: 'px-1.5 py-0.5 text-[10px]', dot: 'w-1.5 h-1.5' },
    md: { badge: 'px-2 py-1 text-xs', dot: 'w-2 h-2' },
    lg: { badge: 'px-3 py-1.5 text-sm', dot: 'w-2.5 h-2.5' },
};

const StatusBadge: React.FC<StatusBadgeProps> = ({
    status,
    label,
    pulse = true,
    size = 'md'
}) => {
    const config = statusConfig[status] || statusConfig.pending;
    const sizes = sizeConfig[size];
    const displayLabel = label || config.label;

    return (
        <span className={`
      inline-flex items-center gap-1.5 rounded-full font-medium border
      ${config.bg} ${config.text} ${config.border} ${sizes.badge}
    `}>
            <span className={`
        rounded-full ${config.dot} ${sizes.dot}
        ${pulse && ['online', 'running', 'warning', 'critical'].includes(status) ? 'animate-pulse' : ''}
      `} />
            {displayLabel}
        </span>
    );
};

export default StatusBadge;

// ═══════════════════════════════════════════════════════════════════════════════
// SEVERITY BADGE
// ═══════════════════════════════════════════════════════════════════════════════

interface SeverityBadgeProps {
    severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
    size?: 'sm' | 'md' | 'lg';
}

const severityConfig = {
    critical: { bg: 'bg-red-500', text: 'text-white', label: 'CRITICAL' },
    high: { bg: 'bg-orange-500', text: 'text-white', label: 'HIGH' },
    medium: { bg: 'bg-amber-500', text: 'text-black', label: 'MEDIUM' },
    low: { bg: 'bg-cyan-500', text: 'text-white', label: 'LOW' },
    info: { bg: 'bg-gray-500', text: 'text-white', label: 'INFO' },
};

export const SeverityBadge: React.FC<SeverityBadgeProps> = ({ severity, size = 'md' }) => {
    const config = severityConfig[severity];
    const sizes = sizeConfig[size];

    return (
        <span className={`
      inline-flex items-center justify-center rounded font-bold uppercase
      ${config.bg} ${config.text} ${sizes.badge}
    `}>
            {config.label}
        </span>
    );
};
