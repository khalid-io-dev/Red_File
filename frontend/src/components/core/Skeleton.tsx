import React from 'react';

interface SkeletonProps {
  variant?: 'text' | 'circular' | 'rectangular';
  width?: string | number;
  height?: string | number;
  className?: string;
}

export default function Skeleton({ 
  variant = 'text', 
  width, 
  height,
  className = '' 
}: SkeletonProps) {
  const baseStyles = 'animate-pulse bg-[var(--bg-tertiary)]';
  
  const variants = {
    text: 'rounded h-4',
    circular: 'rounded-full',
    rectangular: 'rounded-lg'
  };

  const style = {
    width: width || (variant === 'circular' ? '40px' : '100%'),
    height: height || (variant === 'text' ? '1rem' : variant === 'circular' ? '40px' : '200px')
  };

  return (
    <div 
      className={`${baseStyles} ${variants[variant]} ${className}`}
      style={style}
    />
  );
}

export function SkeletonCard() {
  return (
    <div className="bg-[var(--bg-secondary)] border border-[var(--border-primary)] rounded-xl p-6">
      <Skeleton variant="text" width="60%" className="mb-4" />
      <Skeleton variant="text" width="40%" className="mb-6" />
      <Skeleton variant="rectangular" height="200px" />
    </div>
  );
}

export function SkeletonTable({ rows = 5 }: { rows?: number }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4">
          <Skeleton width="40px" height="40px" variant="circular" />
          <div className="flex-1 space-y-2">
            <Skeleton width="80%" />
            <Skeleton width="60%" />
          </div>
        </div>
      ))}
    </div>
  );
}
