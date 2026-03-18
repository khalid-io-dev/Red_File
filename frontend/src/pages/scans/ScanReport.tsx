import { useParams, useNavigate } from 'react-router-dom';
import { Loader2, ArrowLeft, Download } from 'lucide-react';
import { useScan } from '../../hooks/useScans';
import { useFindings } from '../../hooks/useFindings';
import { useCredentials } from '../../hooks/useCredentials';

export default function ScanReport() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: scan, isLoading } = useScan(Number(id));
  const { data: findingsData } = useFindings({ scan_id: Number(id) });
  const { data: credentialsData } = useCredentials({ scan_id: Number(id) });

  if (isLoading) return <div className="flex justify-center p-8"><Loader2 className="w-8 h-8 animate-spin" /></div>;
  if (!scan) return <div className="p-8 text-center">Scan not found</div>;

  const findings = findingsData?.findings || [];
  const credentials = credentialsData?.credentials || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/scans')} className="p-2 hover:bg-white/10 rounded-lg">
            <ArrowLeft className="w-5 h-5" />
          </button>
          <h1 className="text-2xl font-bold">Scan Report</h1>
        </div>
        <button className="px-4 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center gap-2">
          <Download className="w-4 h-4" /> Export PDF
        </button>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 space-y-6">
        <div>
          <h2 className="text-xl font-bold mb-4">Executive Summary</h2>
          <div className="grid grid-cols-4 gap-4">
            <div className="bg-white/5 rounded-lg p-4">
              <div className="text-gray-400 text-sm">Target</div>
              <div className="font-mono">{scan.target}</div>
            </div>
            <div className="bg-white/5 rounded-lg p-4">
              <div className="text-gray-400 text-sm">Scan Type</div>
              <div className="capitalize">{scan.scan_type}</div>
            </div>
            <div className="bg-white/5 rounded-lg p-4">
              <div className="text-gray-400 text-sm">Findings</div>
              <div className="text-2xl font-bold">{findings.length}</div>
            </div>
            <div className="bg-white/5 rounded-lg p-4">
              <div className="text-gray-400 text-sm">Credentials</div>
              <div className="text-2xl font-bold">{credentials.length}</div>
            </div>
          </div>
        </div>

        <div>
          <h2 className="text-xl font-bold mb-4">Findings Summary</h2>
          <div className="space-y-2">
            {findings.slice(0, 10).map((finding: any) => (
              <div key={finding.id} className="bg-white/5 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="font-semibold">{finding.title}</div>
                  <span className={`px-2 py-0.5 rounded text-xs ${
                    finding.severity === 'critical' ? 'bg-red-500/20 text-red-400' :
                    finding.severity === 'high' ? 'bg-orange-500/20 text-orange-400' :
                    finding.severity === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-blue-500/20 text-blue-400'
                  }`}>{finding.severity}</span>
                </div>
                <div className="text-sm text-gray-400">{finding.description}</div>
              </div>
            ))}
          </div>
        </div>

        {credentials.length > 0 && (
          <div>
            <h2 className="text-xl font-bold mb-4">Discovered Credentials</h2>
            <div className="space-y-2">
              {credentials.slice(0, 5).map((cred: any) => (
                <div key={cred.id} className="bg-white/5 rounded-lg p-4 flex items-center justify-between">
                  <div className="font-mono text-sm">{cred.username}:{cred.password}</div>
                  <div className="text-sm text-gray-400">{cred.service}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
