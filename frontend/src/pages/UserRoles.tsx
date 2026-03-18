import { useUsers } from '../hooks/useUsers';
import { Shield, Loader2 } from 'lucide-react';
import Badge from '../components/ui/Badge';

export default function UserRoles() {
  const { data: users = [], isLoading } = useUsers();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  const roleGroups = {
    admin: users.filter(u => u.role === 'admin'),
    analyst: users.filter(u => u.role === 'analyst'),
    viewer: users.filter(u => u.role === 'viewer'),
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white flex items-center gap-3">
        <Shield className="w-6 h-6 text-cyan-400" />
        User Roles
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {Object.entries(roleGroups).map(([role, roleUsers]) => (
          <div key={role} className="glass-panel p-6 rounded-xl">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-white capitalize">{role}</h2>
              <Badge variant="secondary">{roleUsers.length} users</Badge>
            </div>
            <div className="space-y-2">
              {roleUsers.map(user => (
                <div key={user.id} className="p-3 bg-gray-800/50 rounded-lg">
                  <p className="text-gray-300 font-medium">{user.full_name}</p>
                  <p className="text-gray-500 text-sm">{user.email}</p>
                </div>
              ))}
              {roleUsers.length === 0 && (
                <p className="text-gray-500 text-sm text-center py-4">No users</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
