import React from 'react';
import { useFindings } from '../hooks/useFindings';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ArrowLeft, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/ui/Button';

export default function FindingsAnalysis() {
  const navigate = useNavigate();
  const { data: findings = [], isLoading } = useFindings({});

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  // Prepare data for charts
  const severityData = [
    { name: 'Critical', value: findings.filter((f: any) => f.severity === 'critical').length, fill: '#dc2626' },
    { name: 'High', value: findings.filter((f: any) => f.severity === 'high').length, fill: '#f97316' },
    { name: 'Medium', value: findings.filter((f: any) => f.severity === 'medium').length, fill: '#eab308' },
    { name: 'Low', value: findings.filter((f: any) => f.severity === 'low').length, fill: '#3b82f6' },
  ];

  const toolData = findings.reduce((acc: any, f: any) => {
    const existing = acc.find((item: any) => item.name === f.tool);
    if (existing) {
      existing.count += 1;
    } else {
      acc.push({ name: f.tool || 'Unknown', count: 1 });
    }
    return acc;
  }, []);

  const statusData = [
    { name: 'Open', value: findings.filter((f: any) => f.status === 'open').length, fill: '#ef4444' },
    { name: 'In Progress', value: findings.filter((f: any) => f.status === 'in_progress').length, fill: '#f59e0b' },
    { name: 'Resolved', value: findings.filter((f: any) => f.status === 'resolved').length, fill: '#10b981' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="secondary" onClick={() => navigate('/findings')}>
          <ArrowLeft className="w-5 h-5" />
        </Button>
        <div>
          <h1 className="text-3xl font-bold text-white">Findings Analysis</h1>
          <p className="text-gray-400 mt-1">Visual analysis of security findings</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-lg bg-gray-900/50 border border-cyan-500/20">
          <p className="text-sm text-gray-400">Total Findings</p>
          <p className="text-2xl font-bold text-cyan-400">{findings.length}</p>
        </div>
        <div className="p-4 rounded-lg bg-gray-900/50 border border-red-600/20">
          <p className="text-sm text-gray-400">Critical</p>
          <p className="text-2xl font-bold text-red-600">{severityData[0].value}</p>
        </div>
        <div className="p-4 rounded-lg bg-gray-900/50 border border-orange-500/20">
          <p className="text-sm text-gray-400">High</p>
          <p className="text-2xl font-bold text-orange-500">{severityData[1].value}</p>
        </div>
        <div className="p-4 rounded-lg bg-gray-900/50 border border-green-500/20">
          <p className="text-sm text-gray-400">Resolved</p>
          <p className="text-2xl font-bold text-green-500">{statusData[2].value}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="p-6 rounded-lg bg-gray-900/50 border border-gray-800">
          <h2 className="text-xl font-bold text-white mb-4">Severity Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={severityData} cx="50%" cy="50%" labelLine={false} label={({ name, value }) => `${name}: ${value}`} outerRadius={80} dataKey="value">
                {severityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="p-6 rounded-lg bg-gray-900/50 border border-gray-800">
          <h2 className="text-xl font-bold text-white mb-4">Status Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={statusData} cx="50%" cy="50%" labelLine={false} label={({ name, value }) => `${name}: ${value}`} outerRadius={80} dataKey="value">
                {statusData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="p-6 rounded-lg bg-gray-900/50 border border-gray-800">
        <h2 className="text-xl font-bold text-white mb-4">Findings by Tool</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={toolData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
            <XAxis dataKey="name" stroke="#999" />
            <YAxis stroke="#999" />
            <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #444' }} />
            <Bar dataKey="count" fill="#06b6d4" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
