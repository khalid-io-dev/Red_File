import React, { useState } from 'react';
import { Activity, Server, Network, Clock, TrendingUp, TrendingDown, AlertTriangle } from 'lucide-react';

const ContinuousMonitor: React.FC = () => {
  const [isMonitoring, setIsMonitoring] = useState(true);
  const [metrics] = useState([
    { id: '1', name: 'Network Throughput', value: 245, unit: 'Mbps', trend: 'up', threshold: 500, status: 'normal' },
    { id: '2', name: 'CPU Usage', value: 72, unit: '%', trend: 'stable', threshold: 80, status: 'warning' },
    { id: '3', name: 'Memory Usage', value: 64, unit: '%', trend: 'up', threshold: 85, status: 'normal' },
    { id: '4', name: 'Disk I/O', value: 45, unit: 'MB/s', trend: 'stable', threshold: 200, status: 'normal' },
    { id: '5', name: 'Active Connections', value: 1247, unit: 'conn', trend: 'down', threshold: 5000, status: 'normal' },
    { id: '6', name: 'Packet Loss', value: 0.5, unit: '%', trend: 'up', threshold: 1, status: 'warning' }
  ]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'critical': return 'bg-red-600';
      case 'warning': return 'bg-yellow-500';
      default: return 'bg-green-500';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return <TrendingUp className="w-4 h-4 text-green-400" />;
      case 'down': return <TrendingDown className="w-4 h-4 text-red-400" />;
      default: return <Activity className="w-4 h-4 text-gray-400" />;
    }
  };

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Activity className="w-8 h-8 text-green-500" />
          <div>
            <h1 className="text-2xl font-bold text-white">Continuous Monitoring</h1>
            <p className="text-gray-400">Real-time security and system monitoring</p>
          </div>
        </div>
        <button onClick={() => setIsMonitoring(!isMonitoring)} className={`flex items-center gap-2 rounded px-4 py-2 text-sm ${isMonitoring ? 'bg-red-600' : 'bg-green-600'} text-white`}>
          <Activity className={`w-4 h-4 ${isMonitoring ? 'animate-pulse' : ''}`} />
          {isMonitoring ? 'Pause' : 'Resume'}
        </button>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-6">
        {metrics.map(metric => (
          <div key={metric.id} className="bg-gray-800 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-400 text-sm">{metric.name}</span>
              {getTrendIcon(metric.trend)}
            </div>
            <div className="flex items-end justify-between">
              <span className="text-3xl font-bold text-white">{metric.value}</span>
              <span className="text-gray-500 text-sm">{metric.unit}</span>
            </div>
            <div className="mt-2 h-2 bg-gray-700 rounded-full overflow-hidden">
              <div className={`h-full rounded-full ${getStatusColor(metric.status)}`} style={{ width: `${Math.min((metric.value / metric.threshold) * 100, 100)}%` }}></div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-8">
          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="text-white font-medium mb-4 flex items-center gap-2"><Network className="w-5 h-5 text-green-500" />Active Targets</h3>
            <div className="space-y-2">
              {[
                { name: 'Production Servers', count: 12, status: 'healthy' },
                { name: 'Development Servers', count: 8, status: 'healthy' },
                { name: 'Network Devices', count: 24, status: 'warning' },
                { name: 'Database Servers', count: 6, status: 'healthy' }
              ].map((target, i) => (
                <div key={i} className="flex items-center justify-between p-3 bg-gray-700 rounded">
                  <div className="flex items-center gap-3">
                    <Server className="w-5 h-5 text-blue-400" />
                    <span className="text-white">{target.name}</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-gray-400">{target.count} hosts</span>
                    <span className={`w-3 h-3 rounded-full ${target.status === 'healthy' ? 'bg-green-500' : 'bg-yellow-500'}`}></span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="col-span-4">
          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="text-white font-medium mb-4 flex items-center gap-2"><Clock className="w-5 h-5 text-yellow-500" />Live Events</h3>
            <div className="space-y-3">
              {[
                { time: '14:35:22', type: 'info', msg: 'Network scan completed' },
                { time: '14:34:15', type: 'warning', msg: 'CPU usage above 70%' },
                { time: '14:33:00', type: 'error', msg: 'Connection timeout' }
              ].map((event, i) => (
                <div key={i} className="flex items-start gap-3 p-2 bg-gray-700 rounded">
                  <AlertTriangle className={`w-4 h-4 ${event.type === 'error' ? 'text-red-400' : event.type === 'warning' ? 'text-yellow-400' : 'text-blue-400'}`} />
                  <div>
                    <p className="text-white text-sm">{event.msg}</p>
                    <p className="text-gray-500 text-xs">{event.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContinuousMonitor;
