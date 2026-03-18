import { useState, useRef, useEffect } from 'react';
import { Check, ChevronDown } from 'lucide-react';

interface MultiSelectProps {
  options: string[];
  selected: string[];
  onChange: (selected: string[]) => void;
  placeholder?: string;
}

export default function MultiSelect({ options, selected, onChange, placeholder = 'Select...' }: MultiSelectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const toggleOption = (option: string) => {
    if (selected.includes(option)) {
      onChange(selected.filter(s => s !== option));
    } else {
      onChange([...selected, option]);
    }
  };

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 text-left flex items-center justify-between hover:border-cyan-500 focus:outline-none focus:border-cyan-500"
      >
        <span>{selected.length > 0 ? `${selected.length} selected` : placeholder}</span>
        <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute z-10 w-full mt-1 bg-gray-800 border border-gray-700 rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {options.map(option => (
            <button
              key={option}
              onClick={() => toggleOption(option)}
              className="w-full px-4 py-2 text-left hover:bg-gray-700 flex items-center justify-between text-gray-300"
            >
              <span>{option}</span>
              {selected.includes(option) && <Check className="w-4 h-4 text-cyan-400" />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
