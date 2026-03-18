import React from 'react';
import { Loader2 } from 'lucide-react';

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  color?: 'cyan' | 'white' | 'gray';
  fullScreen?: boolean;
  label?: string;
}

export default function Spinner({ 
  size = 'md', 
  color = 'cyan',
  fullScreen = false,
  label 
}: SpinnerProps) {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  };

  const colors = {
    cyan: 'text-[var(--cyber-cyan)]',
    white: 'text-white',
    gray: 'text-[var(--text-tertiary)]'
  };

  const spinner = (
    <div className="flex flex-col items-center gap-3">
      <Loader2 className={`${sizes[size]} ${colors[color]} animate-spin`} />
      {label && (
        <p className="text-sm text-[var(--text-secondary)]">{label}</p>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-[var(--bg-primary)]/80 backdrop-blur-sm z-50">
        {spinner}
      </div>
    );
  }

  return spinner;
}
