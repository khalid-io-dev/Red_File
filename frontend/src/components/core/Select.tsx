import React from 'react';
import { ChevronDown } from 'lucide-react';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  options: Array<{ value: string; label: string }>;
  fullWidth?: boolean;
}

export default function Select({
  label,
  error,
  options,
  fullWidth = false,
  className = '',
  ...props
}: SelectProps) {
  return (
    <div className={`${fullWidth ? 'w-full' : ''}`}>
      {label && (
        <label className="block text-sm font-medium text-[var(--text-secondary)] mb-2">
          {label}
        </label>
      )}
      
      <div className="relative">
        <select
          className={`
            w-full
            pl-4 pr-10 py-2
            bg-gray-900
            border ${error ? 'border-red-500' : 'border-gray-700'}
            rounded-lg
            text-gray-200
            focus:outline-none
            focus:border-cyan-500
            focus:ring-2
            focus:ring-cyan-500
            focus:ring-opacity-20
            transition-all
            appearance-none
            cursor-pointer
            disabled:opacity-50
            disabled:cursor-not-allowed
            ${className}
          `}
          {...props}
        >
          {options.map(option => (
            <option key={option.value} value={option.value} className="bg-gray-900 text-gray-200">
              {option.label}
            </option>
          ))}
        </select>
        
        <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-[var(--text-tertiary)]">
          <ChevronDown className="w-5 h-5" />
        </div>
      </div>
      
      {error && (
        <p className="mt-1.5 text-sm text-[var(--error)]">{error}</p>
      )}
    </div>
  );
}
