import React, { useState } from 'react';
import api from '../services/api';
import Button from '../components/ui/Button';

export default function NewScan() {
    const [target, setTarget] = useState('');
    const [scanType, setScanType] = useState('quick');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

    const validateTarget = (value: string): boolean => {
        const urlPattern = /^(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/;
        const ipPattern = /^(\d{1,3}\.){3}\d{1,3}$/;
        return urlPattern.test(value) || ipPattern.test(value);
    };

    const handleScan = async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (!validateTarget(target)) {
            setMessage({ type: 'error', text: 'Invalid URL or IP address format' });
            return;
        }

        setLoading(true);
        setMessage(null);
        
        try {
            await api.post('/scans/', {
                target_url: target,
                scan_type: scanType
            });
            setMessage({ type: 'success', text: 'Scan initiated successfully. Check the Scans page for results.' });
            setTarget('');
        } catch (error: any) {
            const errorMsg = error.response?.data?.detail || 'Failed to start scan. Please try again.';
            setMessage({ type: 'error', text: errorMsg });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-gray-900/30 p-4 rounded-lg border border-gray-800">
            <form onSubmit={handleScan} className="space-y-4">
                <div className="flex gap-4 items-end flex-wrap">
                    <div className="flex-1 min-w-[250px]">
                        <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 ml-1">Target URL / IP</label>
                        <input
                            type="text"
                            value={target}
                            onChange={(e) => setTarget(e.target.value)}
                            className="input-field bg-gray-950 border-gray-700 focus:border-cyan-500"
                            placeholder="https://example.com or 192.168.1.1"
                            required
                        />
                    </div>
                    <div className="w-48">
                        <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 ml-1">Scan Intensity</label>
                        <select
                            value={scanType}
                            onChange={(e) => setScanType(e.target.value)}
                            className="input-field bg-gray-950 border-gray-700 focus:border-cyan-500 appearance-none cursor-pointer"
                        >
                            <option value="quick">Quick Recon</option>
                            <option value="full">Deep Analysis</option>
                            <option value="passive">Passive Intel</option>
                        </select>
                    </div>
                    <Button
                        type="submit"
                        isLoading={loading}
                        className="mb-[1px]"
                    >
                        {loading ? 'Launching...' : 'Launch Scan'}
                    </Button>
                </div>
                {message && (
                    <div className={`p-3 rounded text-sm flex items-center gap-2 animate-fade-in ${
                        message.type === 'success' 
                            ? 'bg-green-900/20 text-green-400 border border-green-900/50' 
                            : 'bg-red-900/20 text-red-400 border border-red-900/50'
                    }`}>
                        <span className="w-2 h-2 rounded-full bg-current"></span>
                        {message.text}
                    </div>
                )}
            </form>
        </div>
    );
}
