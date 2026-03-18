import React, { useState } from 'react';
import { AlertTriangle, Clock, User, Shield, Filter, Search, CheckCircle, XCircle } from 'lucide-react';

interface Incident {
  id: string;
  title: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  status: 'open' | 'investigating' | 'resolved' | 'closed';
  type: string;
  source: string;
  timestamp: string;
  assignee: string | null;
  description: string;
}

const Incidents: React.FC = () => {
  const [incidents] = useState<Incident[]>([
    { id: 'INC-001', title: 'Unauthorized Access Attempt', severity: 'critical', status: 'open', type: 'Authentication', source: 'SIEM', timestamp: '2024-01-15 14:32:00', assignee: null, description: 'Multiple failed login attempts from unknown IPs.' },
    { id: 'INC-002', title: 'Suspicious Network Traffic', severity: 'high', status: 'investigating', type: 'Network', source: 'IDS', timestamp: '2024-01-15 13:45:00', assignee: 'John Doe', description: 'Unusual outbound traffic from workstation.' },
    { id: 'INC-003', title: 'Malware Detected', severity: 'critical', status: 'investigating', type: 'Malware', source: 'Antivirus', timestamp: '2024-01-15 12:20:00', assignee: 'Jane Smith', description: 'Trojan.GenericKD signature detected.' },
    { id: 'INC-004', title: 'Data Exfiltration Alert', severity: 'high', status: 'open', type: 'Data Breach', source: 'DLP', timestamp: '2024-01-15 11:55:00', assignee: null, description: 'Large data transfer detected outside hours.' }
  ]);

  const [filter, setFilter] = useState<string>('all');
  const [search, setSearch] = useState<string>('');
  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null);

  const filteredIncidents = incidents.filter(i => {
    const matchesFilter = filter === 'all' || i.status === filter;
    const matchesSearch = i.title.toLowerCase().includes(search.toLowerCase()) || i.id.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-600';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-blue-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'open': return <XCircle className="w-4 h-4 text-red-400" />;
      case 'investigating': return <Clock className="w-4 h-4 text-yellow-400" />;
      case 'resolved': return <CheckCircle className="w-4 h-4 text-green-400" />;
      default: return null;
    }
  };

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <AlertTriangle className="w-8 h-8 text-red-500" />
          <div>
            <h1 className="text-2xl font-bold text-white">Incident Response</h1>
            <p className="text-gray-400">Track and manage security incidents</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-800 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <span className="text-gray-400">Open</span>
            <XCircle className="w-5 h-5 text-red-400" />
          </div>
          <p className="text-3xl font-bold text-white mt-2">{incidents.filter(i => i.status === 'open').length}</p>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <span className="text-gray-400">Investigating</span>
            <Clock className="w-5 h-5 text-yellow-400" />
          </div>
          <p className="text-3xl font-bold text-white mt-2">{incidents.filter(i => i.status === 'investigating').length}</p>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <span className="text-gray-400">Resolved</span>
            <CheckCircle className="w-5 h-5 text-green-400" />
          </div>
          <p className="text-3xl font-bold text-white mt-2">{incidents.filter(i => i.status === 'resolved').length}</p>
        </div>
        <div className="bg-gray-800 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <span className="text-gray-400">Critical</span>
            <AlertTriangle className="w-5 h-5 text-red-500" />
          </div>
          <p className="text-3xl font-bold text-white mt-2">{incidents.filter(i => i.severity === 'critical').length}</p>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-7">
          <div className="bg-gray-800 rounded-lg p-4">
            <div className="flex items-center gap-4 mb-4">
              <div className="flex items-center gap-2 bg-gray-700 rounded p-1">
                {['all', 'open', 'investigating', 'resolved'].map(f => (
                  <button key={f} onClick={() => setFilter(f)} className={`px-3 py-1 text-sm rounded capitalize ${filter === f ? 'bg-red-600 text-white' : 'text-gray-400 hover:text-white'}`}>
                    {f}
                  </button>
                ))}
              </div>
              <div className="flex items-center gap-2 flex-1">
                <Search className="w-5 h-5 text-gray-400" />
                <input type="text" placeholder="Search incidents..." value={search} onChange={(e) => setSearch(e.target.value)} className="flex-1 bg-gray-700 text-white rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-500" />
              </div>
            </div>

            <div className="space-y-2">
              {filteredIncidents.map(incident => (
                <div key={incident.id} onClick={() => setSelectedIncident(incident)} className={`p-4 rounded cursor-pointer transition-colors ${selectedIncident?.id === incident.id ? 'bg-red-600' : 'bg-gray-700 hover:bg-gray-600'}`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className={`w-2 h-2 rounded-full ${getSeverityColor(incident.severity)}`}></span>
                      <div>
                        <p className="text-white font-medium">{incident.title}</p>
                        <p className="text-gray-400 text-sm">{incident.id} - {incident.type}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      {getStatusIcon(incident.status)}
                      <span className="text-gray-400 text-sm">{incident.timestamp}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="col-span-5">
          <div className="bg-gray-800 rounded-lg p-4">
            {selectedIncident ? (
              <>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-white font-medium">{selectedIncident.id}</h3>
                  <span className={`text-xs px-2 py-1 rounded ${getSeverityColor(selectedIncident.severity)} text-white`}>
                    {selectedIncident.severity}
                  </span>
                </div>
                <h4 className="text-white text-lg mb-2">{selectedIncident.title}</h4>
                <p className="text-gray-400 text-sm mb-4">{selectedIncident.description}</p>
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Clock className="w-4 h-4 text-gray-500" />
                    <span className="text-gray-400 text-sm">Timestamp:</span>
                    <span className="text-white text-sm">{selectedIncident.timestamp}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <User className="w-4 h-4 text-gray-500" />
                    <span className="text-gray-400 text-sm">Assignee:</span>
                    <span className="text-white text-sm">{selectedIncident.assignee || 'Unassigned'}</span>
                  </div>
                </div>
                <div className="mt-6 flex gap-2">
                  <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white rounded px-4 py-2 text-sm">Investigate</button>
                  <button className="flex-1 bg-green-600 hover:bg-green-700 text-white rounded px-4 py-2 text-sm">Resolve</button>
                </div>
              </>
            ) : (
              <div className="flex flex-col items-center justify-center h-[300px] text-gray-400">
                <AlertTriangle className="w-12 h-12 mb-4 text-gray-600" />
                <p>Select an incident to view details</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Incidents;
