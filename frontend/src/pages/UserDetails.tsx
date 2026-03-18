import { useParams, useNavigate } from 'react-router-dom';
import { useUser } from '../hooks/useUsers';
import { ArrowLeft, User, Mail, Shield, Calendar, Loader2 } from 'lucide-react';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';

export default function UserDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: user, isLoading } = useUser(Number(id));

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  if (!user) return <p className="text-center text-gray-500 py-8">User not found</p>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="secondary" onClick={() => navigate('/user-management')}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-white">{user.full_name}</h1>
            <p className="text-gray-400 mt-1">User Details</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-panel p-4">
          <div className="flex items-center gap-2 text-gray-400 text-sm mb-2">
            <Mail className="w-4 h-4" />
            Email
          </div>
          <p className="text-gray-300">{user.email}</p>
        </div>
        <div className="glass-panel p-4">
          <div className="flex items-center gap-2 text-gray-400 text-sm mb-2">
            <Shield className="w-4 h-4" />
            Role
          </div>
          <Badge variant="secondary">{user.role}</Badge>
        </div>
        <div className="glass-panel p-4">
          <div className="flex items-center gap-2 text-gray-400 text-sm mb-2">
            <Calendar className="w-4 h-4" />
            Status
          </div>
          <Badge variant={user.is_active ? 'success' : 'secondary'}>
            {user.is_active ? 'Active' : 'Inactive'}
          </Badge>
        </div>
      </div>

      <div className="glass-panel p-6">
        <h2 className="text-xl font-bold text-white mb-4">Account Information</h2>
        <div className="space-y-3">
          <div>
            <p className="text-sm text-gray-400">User ID</p>
            <p className="text-gray-300 font-mono">{user.id}</p>
          </div>
          <div>
            <p className="text-sm text-gray-400">Created At</p>
            <p className="text-gray-300">{new Date(user.created_at).toLocaleString()}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
