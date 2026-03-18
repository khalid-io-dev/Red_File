import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useLogin } from '../hooks/useAuth';
import CyberBackground from '../components/CyberBackground';
import Button from '../components/ui/Button';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const { mutate: login, isPending, error } = useLogin();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        login({ email, password });
    };

    return (
        <div className="min-h-screen bg-gray-950 flex items-center justify-center p-4 overflow-hidden relative">
            <CyberBackground />

            <div className="w-full max-w-md card relative z-10 backdrop-blur-xl bg-gray-900/40 border-gray-800 shadow-2xl animate-fade-in">
                <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-cyan-900/20 rounded-full flex items-center justify-center mx-auto mb-4 border border-cyan-500/30 shadow-[0_0_15px_rgba(8,145,178,0.3)]">
                        <svg className="w-8 h-8 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                    </div>
                    <h1 className="text-3xl font-bold text-white mb-2 tracking-tight">System Login</h1>
                    <p className="text-gray-400 text-sm">Enter credentials to access SecureSight</p>
                </div>

                {error && (
                    <div className="bg-red-900/20 border border-red-500/50 text-red-200 p-3 rounded mb-6 text-sm text-center">
                        Invalid email or password
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-1">
                        <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider ml-1">Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="input-field bg-gray-950/50 border-gray-800 focus:border-cyan-500/50 focus:ring-cyan-500/20 rounded-lg"
                            placeholder="name@company.com"
                            required
                        />
                    </div>
                    <div className="space-y-1">
                        <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider ml-1">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="input-field bg-gray-950/50 border-gray-800 focus:border-cyan-500/50 focus:ring-cyan-500/20 rounded-lg"
                            placeholder="••••••••"
                            required
                        />
                    </div>

                    <Button
                        type="submit"
                        isLoading={isPending}
                        className="w-full mt-2"
                    >
                        Authenticate
                    </Button>

                    <div className="text-center mt-6">
                        <p className="text-sm text-gray-500">
                            Don't have an account?{' '}
                            <Link to="/register" className="text-cyan-500 hover:text-cyan-400 font-medium hover:underline transition-all">
                                Create one
                            </Link>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    );
}
