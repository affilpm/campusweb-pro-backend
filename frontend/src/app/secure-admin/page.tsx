'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/auth-context';
import api from '@/lib/api';

interface DashboardStats {
  notices: number;
  events: number;
  gallery: number;
  facilities: number;
}

export default function AdminDashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats>({ notices: 0, events: 0, gallery: 0, facilities: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [notices, events, gallery, facilities] = await Promise.all([
          api.get('/api/admin/content/notices/'),
          api.get('/api/admin/content/events/'),
          api.get('/api/admin/content/gallery/images/'),
          api.get('/api/admin/content/facilities/'),
        ]);
        setStats({
          notices: notices.data.length || 0,
          events: events.data.length || 0,
          gallery: gallery.data.length || 0,
          facilities: facilities.data.length || 0,
        });
      } catch (error) {
        console.error('Error fetching stats:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  const statCards = [
    { name: 'Notices', value: stats.notices, icon: 'bell', color: 'purple' },
    { name: 'Events', value: stats.events, icon: 'calendar', color: 'blue' },
    { name: 'Gallery Images', value: stats.gallery, icon: 'photo', color: 'green' },
    { name: 'Facilities', value: stats.facilities, icon: 'building', color: 'orange' },
  ];

  return (
    <div className="space-y-8">
      {/* Welcome */}
      <div className="bg-gradient-to-r from-purple-600/20 to-indigo-600/20 rounded-2xl border border-purple-500/20 p-6">
        <h1 className="text-2xl font-bold text-white mb-2">
          Welcome back, {user?.first_name || 'Admin'}! 👋
        </h1>
        <p className="text-gray-400">Manage your school website content from here.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat) => (
          <div
            key={stat.name}
            className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 bg-${stat.color}-500/10 rounded-xl`}>
                <svg className={`w-6 h-6 text-${stat.color}-400`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
              </div>
            </div>
            <h3 className="text-3xl font-bold text-white mb-1">
              {loading ? '...' : stat.value}
            </h3>
            <p className="text-sm text-gray-500">{stat.name}</p>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
        <h2 className="text-lg font-semibold text-white mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <a href="/secure-admin/notices" className="flex items-center gap-3 p-4 bg-purple-600/20 hover:bg-purple-600/30 rounded-xl border border-purple-500/20 text-white transition-all">
            <svg className="w-5 h-5 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add New Notice
          </a>
          <a href="/secure-admin/events" className="flex items-center gap-3 p-4 bg-white/5 hover:bg-white/10 rounded-xl border border-white/10 text-white transition-all">
            <svg className="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add New Event
          </a>
          <a href="/secure-admin/gallery" className="flex items-center gap-3 p-4 bg-white/5 hover:bg-white/10 rounded-xl border border-white/10 text-white transition-all">
            <svg className="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Upload Photos
          </a>
        </div>
      </div>

      {/* View Website Link */}
      <div className="text-center">
        <a 
          href="/" 
          target="_blank" 
          className="inline-flex items-center gap-2 text-purple-400 hover:text-purple-300 transition-colors"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
          View Public Website
        </a>
      </div>
    </div>
  );
}
