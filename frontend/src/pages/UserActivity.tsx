import { useState } from 'react';
import { Loader2, Filter } from 'lucide-react';
import { useUserActivities } from '../../hooks/useUsers';

export default function UserActivity() {
  const [userId, setUserId] = useState<number | undefined>();
  const [activityType, setActivityType] = useState<string>('');
  const { data, isLoading } = useUserActivities({ user_id: userId, activity_type: activityType });

  if (isLoading) return <div className="flex justify-center p-8"><Loader2 className="w-8 h-8 animate-spin" /></div>;

  const activities = data?.activities || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">User Activity</h1>
        <select value={activityType} onChange={(e) => setActivityType(e.target.value)} className="px-4 py-2 bg-white/5 rounded-lg">
          <option value="">All Activities</option>
          <option value="login">Login</option>
          <option value="logout">Logout</option>
          <option value="scan_created">Scan Created</option>
          <option value="scan_deleted">Scan Deleted</option>
          <option value="finding_created">Finding Created</option>
          <option value="report_generated">Report Generated</option>
        </select>
      </div>

      <div className="bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden">
        {activities.length > 0 ? (
          <div className="divide-y divide-white/10">
            {activities.map((activity: any) => (
              <div key={activity.id} className="p-4 hover:bg-white/5">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-cyan-400 font-semibold">{activity.user?.email || 'Unknown'}</span>
                      <span className="text-gray-400">•</span>
                      <span className="text-gray-300">{activity.activity_type}</span>
                    </div>
                    {activity.details && (
                      <div className="text-sm text-gray-400 mt-1">{JSON.stringify(activity.details)}</div>
                    )}
                  </div>
                  <div className="text-sm text-gray-400">{new Date(activity.timestamp).toLocaleString()}</div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center text-gray-400 py-12">No activities found</div>
        )}
      </div>
    </div>
  );
}
