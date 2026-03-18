import { Loader2, TrendingUp, TrendingDown, AlertTriangle, Shield, Target } from 'lucide-react';
import { useDashboardStats } from '../../hooks/useDashboard';
import { useFindings } from '../../hooks/useFindings';
import { useScans } from '../../hooks/useScans';

export default function ExecutiveSummary() {
  const { data: stats, isLoading: statsLoading } = useDashboardStats();
  const { data: findingsData, isLoading: findingsLoading } = useFindings();
  const { data: scansData, isLoading: scansLoading } = useScans();

  if (statsLoading || findingsLoading || scansLoading) {
    return <div className="flex justify-center p-8"><Loader2 className="w-8 h-8 animate-spin" /></div>;
  }

  const findings = findingsData?.findings || [];
  const scans = scansData?.scans || [];
  const criticalCount = findings.filter((f: any) => f.severity === 'critical').length;
  const highCount = findings.filter((f: any) => f.severity === 'high').length;
  const activeScans = scans.filter((s: any) => s.status === 'running').length;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Executive Summary</h1>
        <p className="text-gray-400">High-level security posture overview</p>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <div className="flex items-center gap-2 mb-2">
            <Shield className="w-5 h-5 text-cyan-400" />
            <div className="text-gray-400 text-sm">Security Score</div>
          </div>
          <div className="text-3xl font-bold text-cyan-400">
            {Math.max(0, 100 - (criticalCount * 10 + highCount * 5))}%
          </div>
          <div className="flex items-center gap-1 text-sm text-green-400 mt-2">
            <TrendingUp className="w-4 h-4" /> +5% from last month
          </div>
        </div>

        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-5 h-5 text-red-400" />
            <div className="text-gray-400 text-sm">Critical Issues</div>
          </div>
          <div className="text-3xl font-bold text-red-400">{criticalCount}</div>
          <div className="flex items-center gap-1 text-sm text-red-400 mt-2">
            <TrendingDown className="w-4 h-4" /> -2 from last week
          </div>
        </div>

        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <div className="flex items-center gap-2 mb-2">
            <Target className="w-5 h-5 text-orange-400" />
            <div className="text-gray-400 text-sm">High Priority</div>
          </div>
          <div className="text-3xl font-bold text-orange-400">{highCount}</div>
          <div className="flex items-center gap-1 text-sm text-green-400 mt-2">
            <TrendingDown className="w-4 h-4" /> -5 from last week
          </div>
        </div>

        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <div className="flex items-center gap-2 mb-2">
            <Shield className="w-5 h-5 text-green-400" />
            <div className="text-gray-400 text-sm">Active Scans</div>
          </div>
          <div className="text-3xl font-bold text-green-400">{activeScans}</div>
          <div className="text-sm text-gray-400 mt-2">Monitoring in progress</div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <h2 className="text-lg font-bold mb-4">Risk Distribution</h2>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-red-400">Critical</span>
                <span>{criticalCount}</span>
              </div>
              <div className="w-full bg-white/5 rounded-full h-2">
                <div className="bg-red-500 h-2 rounded-full" style={{ width: `${(criticalCount / findings.length) * 100}%` }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-orange-400">High</span>
                <span>{highCount}</span>
              </div>
              <div className="w-full bg-white/5 rounded-full h-2">
                <div className="bg-orange-500 h-2 rounded-full" style={{ width: `${(highCount / findings.length) * 100}%` }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-yellow-400">Medium</span>
                <span>{findings.filter((f: any) => f.severity === 'medium').length}</span>
              </div>
              <div className="w-full bg-white/5 rounded-full h-2">
                <div className="bg-yellow-500 h-2 rounded-full" style={{ width: `${(findings.filter((f: any) => f.severity === 'medium').length / findings.length) * 100}%` }} />
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <h2 className="text-lg font-bold mb-4">Key Recommendations</h2>
          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 bg-red-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-red-400 text-xs font-bold">1</span>
              </div>
              <div className="text-sm">
                <div className="font-semibold mb-1">Address {criticalCount} critical vulnerabilities immediately</div>
                <div className="text-gray-400">Prioritize remote code execution and authentication bypass issues</div>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 bg-orange-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-orange-400 text-xs font-bold">2</span>
              </div>
              <div className="text-sm">
                <div className="font-semibold mb-1">Review {highCount} high-priority findings</div>
                <div className="text-gray-400">Schedule remediation within next sprint cycle</div>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 bg-yellow-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-yellow-400 text-xs font-bold">3</span>
              </div>
              <div className="text-sm">
                <div className="font-semibold mb-1">Implement continuous monitoring</div>
                <div className="text-gray-400">Schedule automated scans for all critical assets</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
