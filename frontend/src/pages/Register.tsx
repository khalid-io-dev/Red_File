import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useRegister } from '../hooks/useAuth';
import CyberBackground from '../components/CyberBackground';
import Button from '../components/ui/Button';

export default function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const navigate = useNavigate();
    const { mutate: register, isPending, error } = useRegister();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        register({ email, password, full_name: fullName });
    };

    return (
        <div className="min-h-screen bg-gray-950 flex items-center justify-center p-4 overflow-hidden relative">
            <CyberBackground />

            <div className="w-full max-w-md card relative z-10 backdrop-blur-xl bg-gray-900/40 border-gray-800 shadow-2xl animate-fade-in">
                <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-cyan-900/20 rounded-full flex items-center justify-center mx-auto mb-4 border border-cyan-500/30 shadow-[0_0_15px_rgba(8,145,178,0.3)]">
                        <svg className="w-8 h-8 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
                    </div>
                    <h1 className="text-3xl font-bold text-white mb-2 tracking-tight">Create Account</h1>
                    <p className="text-gray-400 text-sm">Join the SecureSight operation</p>
                </div>

                {error && (
                    <div className="bg-red-900/20 border border-red-500/50 text-red-200 p-4 rounded-lg mb-6 text-sm flex items-center gap-3 animate-fade-in">
                        <svg className="w-5 h-5 text-red-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                        Registration failed. Please try again.
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-5">
                    <div className="space-y-1">
                        <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider ml-1">Full Name</label>
                        <input
                            type="text"
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                            className="input-field bg-gray-950/50 border-gray-800 focus:border-cyan-500/50 focus:ring-cyan-500/20 rounded-lg"
                            placeholder="John Doe"
                            required
                        />
                    </div>

                    <div className="space-y-1">
                        <label className="text-xs font-semibold text-gray-400 uppercase tracking-wider ml-1">Email Address</label>
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
                            minLength={8}
                        />
                    </div>

                    <Button
                        type="submit"
                        isLoading={isPending}
                        className="w-full mt-2"
                    >
                        Initialize Account
                    </Button>

                    <div className="text-center mt-6">
                        <p className="text-sm text-gray-500">
                            Already have an account?{' '}
                            <Link to="/login" className="text-cyan-500 hover:text-cyan-400 font-medium hover:underline transition-all">
                                Sign in
                            </Link>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    );
}
