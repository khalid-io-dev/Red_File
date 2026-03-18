import { ReactNode } from 'react';
import { cn } from '../../lib/utils';

interface CardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
}

export default function Card({ children, className, hover = false }: CardProps) {
  return (
    <div
      className={cn(
        'rounded-xl bg-gray-900/50 backdrop-blur-xl border border-cyan-500/20 p-6',
        hover && 'hover:border-cyan-400/50 transition-all cursor-pointer',
        className
      )}
    >
      {children}
    </div>
  );
}
