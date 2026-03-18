import { cn } from '../../lib/utils';

interface SkeletonProps {
  className?: string;
}

export default function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={cn(
        'animate-pulse bg-gray-800/50 rounded',
        className
      )}
    />
  );
}

export function SkeletonCard() {
  return (
    <div className="p-6 rounded-xl bg-gray-900/50 border border-cyan-500/20">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <Skeleton className="w-12 h-12 rounded-lg" />
          <div>
            <Skeleton className="w-24 h-4 mb-2" />
            <Skeleton className="w-16 h-3" />
          </div>
        </div>
      </div>
      <Skeleton className="w-full h-16 mb-4" />
      <Skeleton className="w-20 h-8" />
    </div>
  );
}

export function SkeletonTable() {
  return (
    <div className="space-y-3">
      {[...Array(5)].map((_, i) => (
        <Skeleton key={i} className="w-full h-16" />
      ))}
    </div>
  );
}
