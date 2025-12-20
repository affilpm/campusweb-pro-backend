'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';

interface AboutStats {
  established_year: number;
  students_count: string;
  teachers_count: string;
}

interface AcademicHighlight {
  id?: number;
  title: string;
  value: string;
  icon: string;
  order: number;
  is_active: boolean;
}

export default function StatsPage() {
  const [aboutStats, setAboutStats] = useState<AboutStats>({
    established_year: 1990,
    students_count: '',
    teachers_count: '',
  });
  const [initialAboutStats, setInitialAboutStats] = useState<AboutStats | null>(null);
  
  const [academicHighlights, setAcademicHighlights] = useState<AcademicHighlight[]>([]);
  const [editingHighlight, setEditingHighlight] = useState<AcademicHighlight | null>(null);
  
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [errors, setErrors] = useState<Record<string, string[]>>({});
  
  // Use static year for SSR to prevent hydration mismatch
  const [currentYear, setCurrentYear] = useState(2025);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    setCurrentYear(new Date().getFullYear());
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [aboutRes, academicsRes] = await Promise.all([
        api.get('/api/admin/content/home-about/'),
        api.get('/api/admin/content/academics/')
      ]);
      
      setAboutStats({
        established_year: aboutRes.data.established_year,
        students_count: aboutRes.data.students_count,
        teachers_count: aboutRes.data.teachers_count,
      });
      setInitialAboutStats({
        established_year: aboutRes.data.established_year,
        students_count: aboutRes.data.students_count,
        teachers_count: aboutRes.data.teachers_count,
      });
      
      setAcademicHighlights(academicsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      setMessage({ type: 'error', text: 'Failed to load data' });
    } finally {
      setLoading(false);
    }
  };

  const handleAboutStatsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setAboutStats((prev) => ({ 
      ...prev, 
      [name]: name === 'established_year' ? parseInt(value) || 0 : value 
    }));
    if (errors[name]) {
        setErrors((prev) => ({ ...prev, [name]: [] }));
    }
  };

  const saveAboutStats = async () => {
    setSaving(true);
    setErrors({});
    setMessage(null);
    try {
      await api.put('/api/admin/content/home-about/', aboutStats);
      setMessage({ type: 'success', text: 'Basic stats updated successfully' });
    } catch (error: any) {
      console.error('Error saving about stats:', error);
      if (error.response && error.response.status === 400) {
        setErrors(error.response.data);
         setMessage({ type: 'error', text: 'Please check the form for errors.' });
      } else {
        setMessage({ type: 'error', text: 'Failed to save stats' });
      }
    } finally {
      setSaving(false);
    }
  };

  const handleHighlightChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!editingHighlight) return;
    const { name, value } = e.target;
    setEditingHighlight({ ...editingHighlight, [name]: value });
    if (errors[name]) {
        setErrors((prev) => ({ ...prev, [name]: [] }));
    }
  };

  const saveHighlight = async () => {
    if (!editingHighlight) return;
    setSaving(true);
    setErrors({});
    setMessage(null);
    
    try {
      if (editingHighlight.id) {
        await api.put(`/api/admin/content/academics/${editingHighlight.id}/`, editingHighlight);
      } else {
        await api.post('/api/admin/content/academics/', editingHighlight);
      }
      await fetchData();
      setEditingHighlight(null);
      setMessage({ type: 'success', text: 'Stat saved successfully' });
    } catch (error: any) {
      console.error('Error saving highlight:', error);
      if (error.response && error.response.status === 400) {
        setErrors(error.response.data);
      } else {
         setMessage({ type: 'error', text: 'Failed to save stat' });
      }
    } finally {
      setSaving(false);
    }
  };

  const requestDelete = (id: number) => {
    setDeleteId(id);
  };

  const confirmDelete = async () => {
    if (!deleteId) return;
    try {
      await api.delete(`/api/admin/content/academics/${deleteId}/`);
      await fetchData();
      setMessage({ type: 'success', text: 'Stat deleted successfully' });
    } catch (error) {
      console.error('Error deleting highlight:', error);
      setMessage({ type: 'error', text: 'Failed to delete stat' });
    } finally {
      setDeleteId(null);
    }
  };

  const newHighlight = (): AcademicHighlight => {
      setErrors({});
      return {
        title: '',
        value: '',
        icon: '🏆',
        order: academicHighlights.length,
        is_active: true,
      };
  };

  if (loading) return <div className="text-center p-8 text-gray-400">Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Homepage Stats</h1>
        <p className="text-gray-400">Manage the statistics displayed on the homepage</p>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-xl border ${
          message.type === 'success' ? 'bg-green-500/10 border-green-500/30 text-green-400' : 'bg-red-500/10 border-red-500/30 text-red-400'
        }`}>
          {message.text}
        </div>
      )}

      {/* Basic Stats Section */}
      <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6 mb-8">
        <h2 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
          <span className="text-2xl">📊</span>
          Basic Statistics
        </h2>
        
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Year *</label>
            <select
              name="established_year"
              required
              value={aboutStats.established_year}
              onChange={(e) => {
                  const val = parseInt(e.target.value);
                  handleAboutStatsChange({ target: { name: 'established_year', value: val } } as any);
              }}
              className={`w-full px-4 py-3 bg-white/5 border rounded-xl text-white text-lg font-bold focus:outline-none focus:ring-2 focus:ring-purple-500/50 appearance-none ${
                errors.established_year ? 'border-red-500/50' : 'border-white/10'
              }`}
            >
              <option value="" disabled>Select Year</option>
              {Array.from({ length: 100 }, (_, i) => currentYear - i).map((year) => (
                <option key={year} value={year} className="bg-slate-800 text-white">
                  {year}
                </option>
              ))}
            </select>
            {errors.established_year && (
              <p className="text-xs text-red-400">{errors.established_year[0]}</p>
            )}
          </div>
          
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Students Count *</label>
            <input
              type="text"
              name="students_count"
              required
              value={aboutStats.students_count}
              onChange={handleAboutStatsChange}
              placeholder="e.g., 2500+"
              className={`w-full px-4 py-3 bg-white/5 border rounded-xl text-white text-lg font-bold focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                errors.students_count ? 'border-red-500/50' : 'border-white/10'
              }`}
            />
            {errors.students_count && (
              <p className="text-xs text-red-400">{errors.students_count[0]}</p>
            )}
          </div>
          
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Teachers Count *</label>
            <input
              type="text"
              name="teachers_count"
              required
              value={aboutStats.teachers_count}
              onChange={handleAboutStatsChange}
              placeholder="e.g., 150+"
              className={`w-full px-4 py-3 bg-white/5 border rounded-xl text-white text-lg font-bold focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                errors.teachers_count ? 'border-red-500/50' : 'border-white/10'
              }`}
            />
            {errors.teachers_count && (
              <p className="text-xs text-red-400">{errors.teachers_count[0]}</p>
            )}
          </div>
        </div>
        
        <div className="mt-6 flex justify-end">
          <button
            onClick={saveAboutStats}
            disabled={saving || !initialAboutStats || JSON.stringify(aboutStats) === JSON.stringify(initialAboutStats)}
            className="px-6 py-2.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold rounded-xl shadow-lg disabled:opacity-50 transition-all"
          >
            {saving ? 'Saving...' : 'Save Basic Stats'}
          </button>
        </div>
      </div>

      {/* Academic Highlights / Additional Stats */}
      <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <span className="text-2xl">🏆</span>
            Additional Stats
          </h2>
          <button
            onClick={() => setEditingHighlight(newHighlight())}
            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-xl transition-all flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add Stat
          </button>
        </div>

        {/* Stats List */}
        <div className="space-y-4 mb-6">
          {academicHighlights.length === 0 ? (
            <p className="text-gray-400 text-center py-8">No additional stats yet. Click "Add Stat" to create one.</p>
          ) : (
            academicHighlights.map((highlight) => (
              <div 
                key={highlight.id} 
                className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/10"
              >
                <div className="flex items-center gap-4">
                  <span className="text-3xl">{highlight.icon}</span>
                  <div>
                    <span className="text-2xl font-bold text-amber-400">{highlight.value}</span>
                    <p className="text-sm text-gray-300">{highlight.title}</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => setEditingHighlight(highlight)}
                    className="p-2 text-blue-400 hover:bg-blue-500/20 rounded-lg transition-colors"
                  >
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    onClick={() => highlight.id && requestDelete(highlight.id)}
                    className="p-2 text-red-400 hover:bg-red-500/20 rounded-lg transition-colors"
                  >
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Edit/Add Modal */}
      {editingHighlight && (
          <div 
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
            onClick={() => setEditingHighlight(null)}
          >
            <div 
              className="bg-slate-800 rounded-2xl border border-white/10 max-w-md w-full shadow-2xl"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="p-6 border-b border-white/10">
                <h3 className="text-xl font-bold text-white">
                  {editingHighlight.id ? 'Edit Stat' : 'Add New Stat'}
                </h3>
              </div>
              
              <div className="p-6 space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Value *</label>
                  <input
                    type="text"
                    name="value"
                    required
                    value={editingHighlight.value}
                    onChange={handleHighlightChange}
                    placeholder="e.g., 99%, 500+, 25"
                    className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                      errors.value ? 'border-red-500/50' : 'border-white/10'
                    }`}
                  />
                  {errors.value && (
                    <p className="text-xs text-red-400">{errors.value[0]}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Label *</label>
                  <input
                    type="text"
                    name="title"
                    required
                    value={editingHighlight.title}
                    onChange={handleHighlightChange}
                    placeholder="e.g., Pass Rate, Board Toppers"
                    className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                      errors.title ? 'border-red-500/50' : 'border-white/10'
                    }`}
                  />
                  {errors.title && (
                    <p className="text-xs text-red-400">{errors.title[0]}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Icon (emoji)</label>
                  <input
                    type="text"
                    name="icon"
                    value={editingHighlight.icon}
                    onChange={handleHighlightChange}
                    placeholder="🏆"
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  />
                </div>

                <div className="flex items-center gap-3">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={editingHighlight.is_active}
                      onChange={(e) => setEditingHighlight({ ...editingHighlight, is_active: e.target.checked })}
                      className="w-5 h-5 rounded border-gray-600 bg-gray-700 text-purple-600 focus:ring-purple-500"
                    />
                    <span className="text-sm font-medium text-gray-300">Active</span>
                  </label>
                </div>
              </div>

              <div className="p-6 border-t border-white/10 flex gap-3">
                <button
                  onClick={() => setEditingHighlight(null)}
                  className="flex-1 px-4 py-2.5 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-xl transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={saveHighlight}
                  disabled={saving || !editingHighlight.value || !editingHighlight.title}
                  className="flex-1 px-4 py-2.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold rounded-xl shadow-lg disabled:opacity-50 transition-all"
                >
                  {saving ? 'Saving...' : 'Save'}
                </button>
              </div>
            </div>
          </div>
        )}
      {deleteId && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-slate-900 border border-white/10 rounded-2xl p-6 max-w-md w-full shadow-2xl transform scale-100 transition-all">
            <h3 className="text-xl font-bold text-white mb-2">Confirm Delete</h3>
            <p className="text-gray-400 mb-6">
              Are you sure you want to delete this stat? This action cannot be undone.
            </p>
            <div className="flex gap-4 justify-end">
              <button
                onClick={() => setDeleteId(null)}
                className="px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                disabled={saving}
              >
                Cancel
              </button>
              <button
                onClick={confirmDelete}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg shadow-lg shadow-red-600/20 transition-all"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
