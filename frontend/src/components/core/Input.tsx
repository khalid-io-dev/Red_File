import React from 'react';
import { LucideIcon } from 'lucide-react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  icon?: LucideIcon | React.ReactNode;
}

const Input: React.FC<InputProps> = ({
  label,
  error,
  icon: Icon,
  className = '',
  ...props
}) => {
  // Determine the icon to show
  let iconToShow = null;
  if (Icon) {
    if (React.isValidElement(Icon)) {
      iconToShow = React.cloneElement(Icon as React.ReactElement, {
        className: `absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500 ${(Icon as any).props?.className || ''}`
      });
    } else {
      const IconComponent = Icon as React.ElementType;
      iconToShow = <IconComponent className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />;
    }
  }

  return (
    <div className={className}>
      {label && (
        <label className="block text-sm font-medium text-gray-400 mb-2">
          {label}
        </label>
      )}
      <div className="relative">
        {iconToShow}
        <input
          className={`
            w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg 
            text-gray-100 placeholder-gray-500 
            focus:outline-none focus:border-cyan-500/50 focus:ring-2 focus:ring-cyan-500/20
            transition-all duration-200
            ${Icon ? 'pl-12' : ''}
            ${error ? 'border-red-500/50' : ''}
          `.trim()}
          {...props}
        />
      </div>
      {error && (
        <p className="mt-1 text-sm text-red-400">{error}</p>
      )}
    </div>
  );
};

export default Input;
