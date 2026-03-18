import React from 'react';
import { ChevronRight, Home } from 'lucide-react';
import { Link } from 'react-router-dom';

interface BreadcrumbItem {
  label: string;
  href?: string;
  icon?: React.ReactNode;
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[];
  showHome?: boolean;
}

export default function Breadcrumbs({ items, showHome = true }: BreadcrumbsProps) {
  return (
    <nav className="flex items-center gap-2 text-sm">
      {showHome && (
        <>
          <Link 
            to="/" 
            className="text-[var(--text-tertiary)] hover:text-[var(--cyber-cyan)] transition-colors"
          >
            <Home className="w-4 h-4" />
          </Link>
          <ChevronRight className="w-4 h-4 text-[var(--text-tertiary)]" />
        </>
      )}
      
      {items.map((item, index) => (
        <React.Fragment key={index}>
          {item.href ? (
            <Link
              to={item.href}
              className="flex items-center gap-1.5 text-[var(--text-tertiary)] hover:text-[var(--cyber-cyan)] transition-colors"
            >
              {item.icon}
              {item.label}
            </Link>
          ) : (
            <span className="flex items-center gap-1.5 text-[var(--text-primary)] font-medium">
              {item.icon}
              {item.label}
            </span>
          )}
          
          {index < items.length - 1 && (
            <ChevronRight className="w-4 h-4 text-[var(--text-tertiary)]" />
          )}
        </React.Fragment>
      ))}
    </nav>
  );
}
