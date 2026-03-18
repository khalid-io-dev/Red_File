import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface ToolDistributionProps {
  data: Record<string, number>;
}

export default function ToolDistribution({ data }: ToolDistributionProps) {
  const chartData = Object.entries(data)
    .map(([tool, count]) => ({ tool, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
        <XAxis dataKey="tool" stroke="#9ca3af" angle={-45} textAnchor="end" height={80} />
        <YAxis stroke="#9ca3af" />
        <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }} />
        <Bar dataKey="count" fill="#06b6d4" />
      </BarChart>
    </ResponsiveContainer>
  );
}
