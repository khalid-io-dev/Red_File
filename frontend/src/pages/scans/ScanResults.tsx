import { useParams, useNavigate } from 'react-router-dom';
import { Loader2, ArrowLeft, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import { useScan } from '../../hooks/useScans';
import { useFindings } from '../../hooks/useFindings';

export default function ScanResults() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: scan, isLoading } = useScan(Number(id));
  const { data: findingsData } = useFindings({ scan_id: Number(id) });

  if (isLoading) return <div className="flex justify-center p-8"><Loader2 className="w-8 h-8 animate-spin" /></div>;
  if (!scan) return <div className="p-8 text-center">Scan not found</div>;

  const findings = findingsData?.findings || [];
  const criticalCount = findings.filter((f: any) => f.severity === 'critical').length;
  const highCount = findings.filter((f: any) => f.severity === 'high').length;
  const mediumCount = findings.filter((f: any) => f.severity === 'medium').length;
  const lowCount = findings.filter((f: any) => f.severity === 'low').length;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <button onClick={() => navigate('/scans')} className="p-2 hover:bg-white/10 rounded-lg">
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <h1 className="text-2xl font-bold">Scan Results</h1>
          <p className="text-gray-400">{scan.target} - {scan.scan_type}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <h2 className="text-lg font-bold mb-4">Scan Status</h2>
          <div className="flex items-center gap-3 mb-4">
            {scan.status === 'completed' ? (
              <CheckCircle className="w-8 h-8 text-green-400" />
            ) : scan.status === 'failed' ? (
              <XCircle className="w-8 h-8 text-red-400" />
            ) : (
              <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
            )}
            <div>
              <div className="text-xl font-bold capitalize">{scan.status}</div>
              <div className="text-sm text-gray-400">Progress: {scan.progress || 0}%</div>
            </div>
          </div>
          <div className="w-full bg-white/5 rounded-full h-2">
            <div className="bg-cyan-500 h-2 rounded-full" style={{ width: `${scan.progress || 0}%` }} />
          </div>
        </div>

        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <h2 className="text-lg font-bold mb-4">Findings Distribution</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-red-500 rounded-full" />
                <span className="text-sm">Critical</span>
              </div>
              <span className="font-bold text-red-400">{criticalCount}</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-orange-500 rounded-full" />
                <span className="text-sm">High</span>
              </div>
              <span className="font-bold text-orange-400">{highCount}</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-yellow-500 rounded-full" />
                <span className="text-sm">Medium</span>
              </div>
              <span className="font-bold text-yellow-400">{mediumCount}</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-blue-500 rounded-full" />
                <span className="text-sm">Low</span>
              </div>
              <span className="font-bold text-blue-400">{lowCount}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
        <h2 className="text-lg font-bold mb-4">Top Findings</h2>
        {findings.length > 0 ? (
          <div className="space-y-3">
            {findings.slice(0, 5).map((finding: any) => (
              <div key={finding.id} onClick={() => navigate(`/findings/${finding.id}`)} className="bg-white/5 rounded-lg p-4 hover:bg-white/10 cursor-pointer">
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <AlertTriangle className={`w-5 h-5 ${
                      finding.severity === 'critical' ? 'text-red-400' :
                      finding.severity === 'high' ? 'text-orange-400' :
                      finding.severity === 'medium' ? 'text-yellow-400' :
                      'text-blue-400'
                    }`} />
                    <div className="font-semibold">{finding.title}</div>
                  </div>
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
        ) : (
          <div className="text-center text-gray-400 py-8">No findings detected</div>
        )}
      </div>
    </div>
  );
}
