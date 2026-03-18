import { Loader2, AlertTriangle, TrendingUp, TrendingDown } from 'lucide-react';
import { useFindings } from '../../hooks/useFindings';
import { useScans } from '../../hooks/useScans';

export default function RiskAssessment() {
  const { data: findingsData, isLoading: findingsLoading } = useFindings();
  const { data: scansData, isLoading: scansLoading } = useScans();

  if (findingsLoading || scansLoading) return <div className="flex justify-center p-8"><Loader2 className="w-8 h-8 animate-spin" /></div>;

  const findings = findingsData?.findings || [];
  const criticalCount = findings.filter((f: any) => f.severity === 'critical').length;
  const highCount = findings.filter((f: any) => f.severity === 'high').length;
  const riskScore = Math.max(0, 100 - (criticalCount * 15 + highCount * 8));

  const riskCategories = [
    { name: 'Infrastructure', score: 75, trend: 'up', findings: 12 },
    { name: 'Application', score: 60, trend: 'down', findings: 18 },
    { name: 'Network', score: 85, trend: 'up', findings: 8 },
    { name: 'Data', score: 70, trend: 'stable', findings: 10 }
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Risk Assessment</h1>

      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <div className="text-gray-400 text-sm mb-2">Overall Risk Score</div>
          <div className={`text-4xl font-bold ${riskScore >= 80 ? 'text-green-400' : riskScore >= 60 ? 'text-yellow-400' : 'text-red-400'}`}>
            {riskScore}
          </div>
          <div className="text-sm text-gray-400 mt-2">Out of 100</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <div className="text-gray-400 text-sm mb-2">Critical Risks</div>
          <div className="text-4xl font-bold text-red-400">{criticalCount}</div>
          <div className="flex items-center gap-1 text-sm text-red-400 mt-2">
            <TrendingDown className="w-4 h-4" /> -2 this week
          </div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <div className="text-gray-400 text-sm mb-2">High Risks</div>
          <div className="text-4xl font-bold text-orange-400">{highCount}</div>
          <div className="flex items-center gap-1 text-sm text-green-400 mt-2">
            <TrendingDown className="w-4 h-4" /> -5 this week
          </div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <div className="text-gray-400 text-sm mb-2">Total Findings</div>
          <div className="text-4xl font-bold">{findings.length}</div>
          <div className="text-sm text-gray-400 mt-2">Across all scans</div>
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
        <h2 className="text-lg font-bold mb-4">Risk by Category</h2>
        <div className="space-y-4">
          {riskCategories.map((category) => (
            <div key={category.name} className="bg-white/5 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-3">
                  <AlertTriangle className={`w-5 h-5 ${category.score >= 80 ? 'text-green-400' : category.score >= 60 ? 'text-yellow-400' : 'text-red-400'}`} />
                  <div>
                    <div className="font-semibold">{category.name}</div>
                    <div className="text-sm text-gray-400">{category.findings} findings</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className={`text-2xl font-bold ${category.score >= 80 ? 'text-green-400' : category.score >= 60 ? 'text-yellow-400' : 'text-red-400'}`}>
                    {category.score}
                  </div>
                  {category.trend === 'up' && <TrendingUp className="w-5 h-5 text-green-400" />}
                  {category.trend === 'down' && <TrendingDown className="w-5 h-5 text-red-400" />}
                </div>
              </div>
              <div className="w-full bg-white/5 rounded-full h-2">
                <div className={`h-2 rounded-full ${category.score >= 80 ? 'bg-green-500' : category.score >= 60 ? 'bg-yellow-500' : 'bg-red-500'}`} style={{ width: `${category.score}%` }} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
