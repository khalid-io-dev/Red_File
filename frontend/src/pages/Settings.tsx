import { Save } from 'lucide-react';
import Button from '../components/ui/Button';

export default function Settings() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Settings</h1>
        <p className="text-gray-400 mt-1">Configure your environment</p>
      </div>

      <div className="space-y-6">
        <div className="p-6 rounded-xl bg-gray-900/50 border border-cyan-500/20">
          <h2 className="text-xl font-bold text-cyan-400 mb-4">Kali Linux Connection</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Host</label>
              <input
                type="text"
                defaultValue="192.168.56.101"
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Port</label>
              <input
                type="number"
                defaultValue="22"
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Username</label>
              <input
                type="text"
                defaultValue="hollow"
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300"
              />
            </div>
            <Button variant="secondary">Test Connection</Button>
          </div>
        </div>

        <div className="p-6 rounded-xl bg-gray-900/50 border border-cyan-500/20">
          <h2 className="text-xl font-bold text-cyan-400 mb-4">AI Configuration</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Model</label>
              <select className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300">
                <option>qwen2.5-coder:7b</option>
                <option>deepseek-coder:6.7b</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Ollama URL</label>
              <input
                type="text"
                defaultValue="http://localhost:11434"
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300"
              />
            </div>
          </div>
        </div>

        <div className="flex justify-end">
          <Button>
            <Save className="w-5 h-5 mr-2" />
            Save Settings
          </Button>
        </div>
      </div>
    </div>
  );
}
