import { useState } from 'react';
import { Loader2, Key, Play } from 'lucide-react';
import { useCredentials } from '../../hooks/useCredentials';

export default function CredentialAttacks() {
  const [attackType, setAttackType] = useState('brute_force');
  const [target, setTarget] = useState('');
  const [username, setUsername] = useState('');
  const [wordlist, setWordlist] = useState('rockyou.txt');
  const { data: credentialsData } = useCredentials();

  const credentials = credentialsData?.credentials || [];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Credential Attacks</h1>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 space-y-4">
          <h2 className="text-lg font-bold">Attack Configuration</h2>
          <div>
            <label className="block text-sm text-gray-400 mb-2">Attack Type</label>
            <select value={attackType} onChange={(e) => setAttackType(e.target.value)} className="w-full px-4 py-2 bg-white/5 rounded-lg">
              <option value="brute_force">Brute Force</option>
              <option value="dictionary">Dictionary Attack</option>
              <option value="credential_stuffing">Credential Stuffing</option>
              <option value="password_spray">Password Spray</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-2">Target</label>
            <input type="text" value={target} onChange={(e) => setTarget(e.target.value)} placeholder="ssh://192.168.1.1" className="w-full px-4 py-2 bg-white/5 rounded-lg" />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-2">Username</label>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="admin" className="w-full px-4 py-2 bg-white/5 rounded-lg" />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-2">Wordlist</label>
            <select value={wordlist} onChange={(e) => setWordlist(e.target.value)} className="w-full px-4 py-2 bg-white/5 rounded-lg">
              <option value="rockyou.txt">rockyou.txt</option>
              <option value="common.txt">common.txt</option>
              <option value="passwords.txt">passwords.txt</option>
            </select>
          </div>
          <button className="w-full px-6 py-3 bg-cyan-500/20 hover:bg-cyan-500/30 rounded-lg flex items-center justify-center gap-2 font-semibold">
            <Play className="w-5 h-5" /> Launch Attack
          </button>
        </div>

        <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6">
          <h2 className="text-lg font-bold mb-4">Discovered Credentials ({credentials.length})</h2>
          {credentials.length > 0 ? (
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {credentials.map((cred: any) => (
                <div key={cred.id} className="bg-white/5 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-1">
                    <Key className="w-4 h-4 text-cyan-400" />
                    <span className="font-mono text-sm">{cred.username}:{cred.password}</span>
                  </div>
                  <div className="text-xs text-gray-400">{cred.service} - {cred.validated ? '✓ Validated' : 'Unvalidated'}</div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-400 py-12">No credentials discovered yet</div>
          )}
        </div>
      </div>
    </div>
  );
}
