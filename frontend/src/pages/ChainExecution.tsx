import { useParams, useNavigate } from 'react-router-dom';
import { Loader2, ArrowLeft, Play, Square, CheckCircle, XCircle, Clock } from 'lucide-react';
import { useAttackChain, useExecuteAttackChain } from '../../hooks/useAttackChains';

export default function ChainExecution() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: chain, isLoading } = useAttackChain(Number(id));
  const executeChain = useExecuteAttackChain();

  if (isLoading) return <div className="flex justify-center p-8"><Loader2 className="w-8 h-8 animate-spin" /></div>;
  if (!chain) return <div className="p-8 text-center">Attack chain not found</div>;

  const mockExecution = {
    status: 'running',
    current_step: 2,
    total_steps: chain.techniques?.length || 0,
    steps: chain.techniques?.map((t: any, idx: number) => ({
      ...t,
      status: idx < 2 ? 'completed' : idx === 2 ? 'running' : 'pending',
      started_at: idx < 2 ? new Date().toISOString() : null,
      completed_at: idx < 2 ? new Date().toISOString() : null
    })) || []
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/attack-chains')} className="p-2 hover:bg-white/10 rounded-lg">
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="text-2xl font-bold">{chain.name}</h1>
            <p className="text-gray-400">Execution Monitor</p>
          </div>
        </div>
        <button onClick={() => executeChain.mutate(chain.id)} disabled={executeChain.isPending} className="px-4 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center gap-2">
          {executeChain.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
          Execute
        </button>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Status</div>
          <div className="text-xl font-bold capitalize">{mockExecution.status}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Progress</div>
          <div className="text-xl font-bold">{mockExecution.current_step}/{mockExecution.total_steps}</div>
        </div>
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4">
          <div className="text-gray-400 text-sm">Completion</div>
          <div className="text-xl font-bold">{Math.round((mockExecution.current_step / mockExecution.total_steps) * 100)}%</div>
        </div>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
        <h2 className="text-lg font-bold mb-4">Execution Steps</h2>
        <div className="space-y-3">
          {mockExecution.steps.map((step: any, index: number) => (
            <div key={index} className={`bg-white/5 rounded-lg p-4 ${
              step.status === 'running' ? 'border-2 border-cyan-500/50' : ''
            }`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full flex items-center justify-center">
                    {step.status === 'completed' && <CheckCircle className="w-6 h-6 text-green-400" />}
                    {step.status === 'running' && <Loader2 className="w-6 h-6 text-cyan-400 animate-spin" />}
                    {step.status === 'pending' && <Clock className="w-6 h-6 text-gray-400" />}
                    {step.status === 'failed' && <XCircle className="w-6 h-6 text-red-400" />}
                  </div>
                  <div>
                    <div className="font-mono text-sm text-cyan-400">{step.technique_id}</div>
                    <div className="text-sm">{step.name}</div>
                  </div>
                </div>
                <span className={`px-2 py-1 rounded text-xs ${
                  step.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                  step.status === 'running' ? 'bg-cyan-500/20 text-cyan-400' :
                  step.status === 'failed' ? 'bg-red-500/20 text-red-400' :
                  'bg-gray-500/20 text-gray-400'
                }`}>{step.status}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
