import React from 'react';

interface ProgressProps {
  value: number;
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'success' | 'warning' | 'error';
  showLabel?: boolean;
  label?: string;
}

export default function Progress({ 
  value, 
  max = 100, 
  size = 'md',
  variant = 'default',
  showLabel = false,
  label
}: ProgressProps) {
  const percentage = Math.min((value / max) * 100, 100);

  const sizes = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3'
  };

  const variants = {
    default: 'bg-[var(--cyber-cyan)]',
    success: 'bg-[var(--success)]',
    warning: 'bg-[var(--warning)]',
    error: 'bg-[var(--error)]'
  };

  return (
    <div className="w-full">
      {(showLabel || label) && (
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-[var(--text-secondary)]">{label}</span>
          {showLabel && (
            <span className="text-sm font-medium text-[var(--text-primary)]">
              {Math.round(percentage)}%
            </span>
          )}
        </div>
      )}
      <div className={`w-full ${sizes[size]} bg-[var(--bg-tertiary)] rounded-full overflow-hidden`}>
        <div
          className={`${sizes[size]} ${variants[variant]} rounded-full transition-all duration-300`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
