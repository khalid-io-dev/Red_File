import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  className = '',
  disabled,
  ...props
}) => {
  const baseClasses = `
    inline-flex items-center justify-center gap-2 font-medium rounded-lg
    transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900
    disabled:opacity-50 disabled:cursor-not-allowed
  `;

  const variantClasses = {
    primary: `
      bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400
      text-white shadow-lg shadow-red-500/30 hover:shadow-red-500/50
      focus:ring-red-500
    `,
    secondary: `
      bg-gray-800 hover:bg-gray-700 text-gray-100
      border border-gray-700 hover:border-red-500/30
      focus:ring-gray-500
    `,
    danger: `
      bg-gradient-to-r from-red-700 to-red-600 hover:from-red-600 hover:to-red-500
      text-white shadow-lg shadow-red-600/40 hover:shadow-red-600/60
      focus:ring-red-600
    `,
    ghost: `
      bg-transparent hover:bg-red-500/10 text-gray-300 hover:text-red-400
      focus:ring-gray-500
    `,
    outline: `
      bg-transparent border border-red-500/50 text-red-400
      hover:bg-red-500/10 hover:border-red-500
      focus:ring-red-500
    `,
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      ) : leftIcon}
      {children}
      {!isLoading && rightIcon}
    </button>
  );
};

export default Button;

// ═══════════════════════════════════════════════════════════════════════════════
// ICON BUTTON
// ═══════════════════════════════════════════════════════════════════════════════

interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  icon: React.ReactNode;
  variant?: 'ghost' | 'solid';
  size?: 'sm' | 'md' | 'lg';
  tooltip?: string;
}

export const IconButton: React.FC<IconButtonProps> = ({
  icon,
  variant = 'ghost',
  size = 'md',
  tooltip,
  className = '',
  ...props
}) => {
  const baseClasses = 'rounded-lg transition-all duration-200 focus:outline-none';

  const variantClasses = {
    ghost: 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50',
    solid: 'bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-white border border-gray-700',
  };

  const sizeClasses = {
    sm: 'p-1.5',
    md: 'p-2',
    lg: 'p-3',
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      title={tooltip}
      {...props}
    >
      {icon}
    </button>
  );
};
