import { LucideIcon } from 'lucide-react';
import { motion } from 'framer-motion';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  change?: string;
  color?: string;
}

export default function StatCard({ title, value, icon: Icon, change, color = 'cyan' }: StatCardProps) {
  const colorClasses = {
    cyan: 'from-cyan-500/20 to-cyan-600/20 border-cyan-500/30 text-cyan-400',
    purple: 'from-purple-500/20 to-purple-600/20 border-purple-500/30 text-purple-400',
    red: 'from-red-500/20 to-red-600/20 border-red-500/30 text-red-400',
    green: 'from-green-500/20 to-green-600/20 border-green-500/30 text-green-400',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`relative overflow-hidden rounded-xl bg-gradient-to-br ${colorClasses[color as keyof typeof colorClasses]} border backdrop-blur-xl p-6`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-400 mb-1">{title}</p>
          <p className="text-3xl font-bold">{value}</p>
          {change && (
            <p className="text-xs text-gray-500 mt-2">{change}</p>
          )}
        </div>
        <div className="p-3 rounded-lg bg-gray-900/50">
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </motion.div>
  );
}
