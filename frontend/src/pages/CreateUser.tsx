import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCreateUser } from '../hooks/useUsers';
import { Loader2 } from 'lucide-react';
import Button from '../components/ui/Button';

export default function CreateUser() {
  const navigate = useNavigate();
  const createUser = useCreateUser();
  const [formData, setFormData] = useState({
    email: '',
    full_name: '',
    password: '',
    role: 'analyst',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createUser.mutateAsync(formData);
    navigate('/user-management');
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white">Create User</h1>
      <form onSubmit={handleSubmit} className="glass-panel p-6 rounded-xl space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Full Name</label>
          <input
            type="text"
            value={formData.full_name}
            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
            className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Password</label>
          <input
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Role</label>
          <select
            value={formData.role}
            onChange={(e) => setFormData({ ...formData, role: e.target.value })}
            className="w-full px-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg text-white focus:border-cyan-500 focus:outline-none"
          >
            <option value="admin">Admin</option>
            <option value="analyst">Analyst</option>
            <option value="viewer">Viewer</option>
          </select>
        </div>
        <div className="flex gap-3">
          <Button type="submit" disabled={createUser.isPending}>
            {createUser.isPending ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
            Create User
          </Button>
          <Button variant="ghost" onClick={() => navigate('/user-management')}>Cancel</Button>
        </div>
      </form>
    </div>
  );
}
