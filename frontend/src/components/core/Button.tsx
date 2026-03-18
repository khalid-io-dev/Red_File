import React from 'react';
import { LucideIcon } from 'lucide-react';

// Backwards compatible Button component that matches the old API
// Old pages use: icon={IconComponent} 
// New pages use: leftIcon={<Icon />}

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  icon?: LucideIcon | React.ReactNode; // Old API
  leftIcon?: React.ReactNode; // New API
  rightIcon?: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  icon: Icon,
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

  // Determine the icon to show (support both old and new API)
  let iconToShow = leftIcon;
  if (!iconToShow && Icon) {
    if (React.isValidElement(Icon)) {
      iconToShow = Icon;
    } else if (typeof Icon === 'function' || typeof Icon === 'object') {
      const IconComponent = Icon as React.ElementType;
      iconToShow = <IconComponent className="w-4 h-4" />;
    }
  }

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
      ) : iconToShow}
      {children}
      {!isLoading && rightIcon}
    </button>
  );
};

export default Button;
