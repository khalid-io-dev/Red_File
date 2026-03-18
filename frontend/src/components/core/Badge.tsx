import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const variantStyles = {
  primary: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
  secondary: 'bg-gray-700 text-gray-300 border-gray-600',
  success: 'bg-green-500/10 text-green-400 border-green-500/30',
  danger: 'bg-red-500/10 text-red-400 border-red-500/30',
  warning: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
  info: 'bg-purple-500/10 text-purple-400 border-purple-500/30',
};

const sizeStyles = {
  sm: 'px-1.5 py-0.5 text-[10px]',
  md: 'px-2 py-0.5 text-xs',
  lg: 'px-2.5 py-1 text-sm',
};

const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  className = ''
}) => {
  return (
    <span className={`
      inline-flex items-center justify-center rounded font-medium border
      ${variantStyles[variant]} ${sizeStyles[size]} ${className}
    `.trim()}>
      {children}
    </span>
  );
};

export default Badge;
