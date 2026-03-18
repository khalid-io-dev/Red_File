import { useParams } from 'react-router-dom';
import { useFinding, useUpdateFinding } from '../hooks/useFindings';
import { Loader2, CheckCircle, XCircle } from 'lucide-react';
import Button from '../components/ui/Button';

export default function FindingTriage() {
  const { id } = useParams();
  const { data: finding, isLoading } = useFinding(Number(id));
  const updateFinding = useUpdateFinding();

  const handleTriage = async (status: string) => {
    await updateFinding.mutateAsync({ id: Number(id), data: { status } });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  if (!finding) return <p className="text-center text-gray-500 py-8">Finding not found</p>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white">Triage Finding</h1>
      <div className="glass-panel p-6 rounded-xl space-y-6">
        <div>
          <h2 className="text-lg font-bold text-white mb-2">{finding.title}</h2>
          <p className="text-gray-400">{finding.description}</p>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <Button onClick={() => handleTriage('confirmed')} disabled={updateFinding.isPending}>
            <CheckCircle className="w-4 h-4 mr-2" />
            Confirm
          </Button>
          <Button variant="secondary" onClick={() => handleTriage('false_positive')} disabled={updateFinding.isPending}>
            <XCircle className="w-4 h-4 mr-2" />
            False Positive
          </Button>
        </div>
      </div>
    </div>
  );
}
