import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date) {
  return new Date(date).toLocaleString();
}

export function formatDuration(seconds: number) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return `${h}h ${m}m ${s}s`;
}

export function getSeverityColor(severity: string) {
  const colors = {
    critical: 'text-red-600 bg-red-500/10',
    high: 'text-red-500 bg-red-500/10',
    medium: 'text-yellow-500 bg-yellow-500/10',
    low: 'text-blue-500 bg-blue-500/10',
    info: 'text-cyan-500 bg-cyan-500/10',
  };
  return colors[severity.toLowerCase() as keyof typeof colors] || colors.info;
}

export function getStatusColor(status: string) {
  const colors = {
    pending: 'text-gray-500 bg-gray-500/10',
    running: 'text-cyan-500 bg-cyan-500/10',
    completed: 'text-green-500 bg-green-500/10',
    failed: 'text-red-500 bg-red-500/10',
    paused: 'text-yellow-500 bg-yellow-500/10',
  };
  return colors[status.toLowerCase() as keyof typeof colors] || colors.pending;
}

export function truncate(str: string, length: number) {
  return str.length > length ? str.substring(0, length) + '...' : str;
}

export function downloadFile(content: string, filename: string, type: string) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
