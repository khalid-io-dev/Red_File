import React from 'react';
import { AlertCircle, CheckCircle, Info, AlertTriangle, X } from 'lucide-react';

interface AlertProps {
  variant?: 'info' | 'success' | 'warning' | 'error';
  title?: string;
  children: React.ReactNode;
  onClose?: () => void;
}

export default function Alert({ variant = 'info', title, children, onClose }: AlertProps) {
  const variants = {
    info: {
      bg: 'bg-[var(--info)]/10',
      border: 'border-[var(--info)]/30',
      text: 'text-[var(--info)]',
      icon: Info
    },
    success: {
      bg: 'bg-[var(--success)]/10',
      border: 'border-[var(--success)]/30',
      text: 'text-[var(--success)]',
      icon: CheckCircle
    },
    warning: {
      bg: 'bg-[var(--warning)]/10',
      border: 'border-[var(--warning)]/30',
      text: 'text-[var(--warning)]',
      icon: AlertTriangle
    },
    error: {
      bg: 'bg-[var(--error)]/10',
      border: 'border-[var(--error)]/30',
      text: 'text-[var(--error)]',
      icon: AlertCircle
    }
  };

  const { bg, border, text, icon: Icon } = variants[variant];

  return (
    <div className={`${bg} border ${border} rounded-lg p-4`}>
      <div className="flex gap-3">
        <Icon className={`w-5 h-5 ${text} flex-shrink-0 mt-0.5`} />
        <div className="flex-1">
          {title && (
            <h4 className={`font-semibold ${text} mb-1`}>{title}</h4>
          )}
          <div className="text-sm text-[var(--text-secondary)]">{children}</div>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="text-[var(--text-tertiary)] hover:text-[var(--text-primary)] transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>
    </div>
  );
}
