import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

interface TimelineChartProps {
  data: Array<{
    date: string;
    scans: number;
    findings: number;
  }>;
}

export default function TimelineChart({ data }: TimelineChartProps) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
        <XAxis dataKey="date" stroke="#9ca3af" />
        <YAxis stroke="#9ca3af" />
        <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }} />
        <Legend />
        <Line type="monotone" dataKey="scans" stroke="#06b6d4" strokeWidth={2} />
        <Line type="monotone" dataKey="findings" stroke="#f59e0b" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
}
