import { useParams, useNavigate } from 'react-router-dom';
import { Loader2, ArrowLeft, CheckCircle, XCircle, Trash2 } from 'lucide-react';
import { useCredential, useDeleteCredential } from '../../hooks/useCredentials';

export default function CredentialDetails() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: credential, isLoading } = useCredential(Number(id));
  const deleteCredential = useDeleteCredential();

  if (isLoading) return <div className="flex justify-center p-8"><Loader2 className="w-8 h-8 animate-spin" /></div>;
  if (!credential) return <div className="p-8 text-center">Credential not found</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/credentials')} className="p-2 hover:bg-white/10 rounded-lg">
            <ArrowLeft className="w-5 h-5" />
          </button>
          <h1 className="text-2xl font-bold">Credential Details</h1>
        </div>
        <button onClick={() => deleteCredential.mutate(credential.id, { onSuccess: () => navigate('/credentials') })} className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 rounded-lg flex items-center gap-2">
          <Trash2 className="w-4 h-4" /> Delete
        </button>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 space-y-4">
          <div>
            <div className="text-gray-400 text-sm">Username</div>
            <div className="text-lg font-mono">{credential.username}</div>
          </div>
          <div>
            <div className="text-gray-400 text-sm">Password</div>
            <div className="text-lg font-mono">{credential.password}</div>
          </div>
          <div>
            <div className="text-gray-400 text-sm">Service</div>
            <div className="text-lg">{credential.service || 'N/A'}</div>
          </div>
          <div>
            <div className="text-gray-400 text-sm">Port</div>
            <div className="text-lg">{credential.port || 'N/A'}</div>
          </div>
        </div>

        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 space-y-4">
          <div>
            <div className="text-gray-400 text-sm">Validated</div>
            <div className="flex items-center gap-2 mt-1">
              {credential.validated ? (
                <><CheckCircle className="w-5 h-5 text-green-500" /> <span>Yes</span></>
              ) : (
                <><XCircle className="w-5 h-5 text-red-500" /> <span>No</span></>
              )}
            </div>
          </div>
          <div>
            <div className="text-gray-400 text-sm">Source</div>
            <div className="text-lg">{credential.source || 'Unknown'}</div>
          </div>
          <div>
            <div className="text-gray-400 text-sm">Discovered</div>
            <div className="text-lg">{new Date(credential.created_at).toLocaleString()}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
