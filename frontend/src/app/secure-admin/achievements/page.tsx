'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';
import ImageUpload from '@/components/admin/image-upload';

interface Achievement {
  id?: number;
  title: string;
  description: string;
  image: string | null;
  year: number | null;
  is_featured: boolean;
  is_active: boolean;
}

export default function AchievementsManagementPage() {
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState<Achievement | null>(null);
  const [initialEditingData, setInitialEditingData] = useState<Achievement | null>(null);

  const [showModal, setShowModal] = useState(false);
  const [newImage, setNewImage] = useState<File | null>(null);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const res = await api.get('/api/admin/content/achievements/');
      setAchievements(res.data);
    } catch (error) {
      console.error('Error fetching achievements:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!editing) return;
    
    try {
      const formData = new FormData();
      formData.append('title', editing.title);
      formData.append('description', editing.description);
      if (editing.year) formData.append('year', editing.year.toString());
      formData.append('is_featured', String(editing.is_featured));
      formData.append('is_active', String(editing.is_active));
      
      if (newImage) {
        formData.append('image', newImage);
      } else if (editing.image === null && initialEditingData?.image) {
        // Handle image deletion if backend supports it by checking explicit null or empty
        // For now assuming backend updates only if provided
        // formData.append('image', ''); 
      }
      
      const config = { headers: { 'Content-Type': 'multipart/form-data' } };

      if (editing.id) {
        await api.put(`/api/admin/content/achievements/${editing.id}/`, formData, config);
      } else {
        await api.post('/api/admin/content/achievements/', formData, config);
      }
      fetchData();
      setShowModal(false);
      setEditing(null);
      setNewImage(null);
      setInitialEditingData(null);
    } catch (error) {
      console.error('Error saving achievement:', error);
    }
  };

  const requestDelete = (id: number) => {
    setDeleteId(id);
  };

  const confirmDelete = async () => {
    if (!deleteId) return;
    
    try {
      await api.delete(`/api/admin/content/achievements/${deleteId}/`);
      fetchData();
    } catch (error) {
      console.error('Error deleting achievement:', error);
    } finally {
      setDeleteId(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-6xl">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white">Achievements & Awards</h1>
          <p className="text-gray-400">Manage school achievements and awards</p>
        </div>
        <button
          onClick={() => {
            const newAchievement = {
              title: '',
              description: '',
              image: null,
              year: new Date().getFullYear(),
              is_featured: false,
              is_active: true
            };
            setEditing(newAchievement);
            setInitialEditingData({ ...newAchievement });
            setShowModal(true);
          }}
          className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add Achievement
        </button>
      </div>

      {/* Achievements Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {achievements.map((achievement) => (
          <div key={achievement.id} className="bg-slate-800/50 backdrop-blur-xl border border-white/10 rounded-xl p-6">
            <div className="flex items-start justify-between mb-3">
              <div>
                <h3 className="font-semibold text-white">{achievement.title}</h3>
                {achievement.year && (
                  <span className="text-sm text-purple-400">{achievement.year}</span>
                )}
              </div>
              {achievement.is_featured && (
                <span className="px-2 py-1 bg-amber-500/20 text-amber-400 text-xs rounded border border-amber-500/20">Featured</span>
              )}
            </div>
            <p className="text-sm text-gray-400 mb-4">{achievement.description}</p>
            <div className="flex justify-end gap-2">
              <button
                onClick={() => {
                  setEditing(achievement);
                  setInitialEditingData({ ...achievement });
                  setShowModal(true);
                }}
                className="p-2 hover:bg-white/5 rounded-lg text-gray-400 hover:text-white transition-colors"
              >
                Edit
              </button>
              <button
                onClick={() => achievement.id && requestDelete(achievement.id)}
                className="p-2 hover:bg-red-500/10 rounded-lg text-gray-400 hover:text-red-400 transition-colors"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {achievements.length === 0 && (
        <div className="text-center py-12 bg-slate-800/20 rounded-xl border border-white/5">
          <div className="text-4xl mb-4">🏆</div>
          <p className="text-gray-500">No achievements yet. Add your first achievement!</p>
        </div>
      )}

      {/* Modal */}
      {showModal && editing && (
        <div 
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => {
            setShowModal(false);
            setEditing(null);
            setNewImage(null);
          }}
        >
          <div 
            className="bg-slate-900 border border-white/10 rounded-2xl w-full max-w-lg flex flex-col max-h-[90vh] shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6 border-b border-white/10 flex items-center justify-between flex-shrink-0">
              <h2 className="text-xl font-bold text-white">
                {editing.id ? 'Edit Achievement' : 'Add Achievement'}
              </h2>
              <button 
                onClick={() => {
                  setShowModal(false);
                  setNewImage(null);
                }} 
                className="text-gray-400 hover:text-white"
              >
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="p-6 space-y-4 overflow-y-auto custom-scrollbar">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Title *</label>
                <input
                  type="text"
                  required
                  value={editing.title}
                  onChange={(e) => setEditing({ ...editing, title: e.target.value })}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Description *</label>
                <textarea
                  required
                  value={editing.description}
                  onChange={(e) => setEditing({ ...editing, description: e.target.value })}
                  rows={3}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Year</label>
                <input
                  type="number"
                  value={editing.year ?? ''}
                  onChange={(e) => setEditing({ ...editing, year: e.target.value ? parseInt(e.target.value) : null })}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  placeholder="Optional"
                />
              </div>
              <div className="space-y-2">
               <label className="text-sm font-medium text-gray-300">Image</label>
               <ImageUpload
                    label=""
                    currentImage={editing.image}
                    onChange={(file) => setNewImage(file)}
                    onRemove={() => {
                      setNewImage(null);
                      setEditing({ ...editing, image: null });
                    }}
                  />
              </div>
              <div className="flex items-center gap-6 pt-2">
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={editing.is_featured}
                    onChange={(e) => setEditing({ ...editing, is_featured: e.target.checked })}
                    className="w-5 h-5 rounded border-gray-600 bg-gray-700 text-purple-600 focus:ring-purple-500"
                  />
                  <span className="text-sm text-gray-300">Featured</span>
                </label>
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={editing.is_active}
                    onChange={(e) => setEditing({ ...editing, is_active: e.target.checked })}
                    className="w-5 h-5 rounded border-gray-600 bg-gray-700 text-purple-600 focus:ring-purple-500"
                  />
                  <span className="text-sm text-gray-300">Active</span>
                </label>
              </div>
            </div>

            <div className="p-6 border-t border-white/10 flex justify-end gap-3 flex-shrink-0">
              <button
                onClick={() => {
                  setShowModal(false);
                  setEditing(null);
                  setNewImage(null);
                }}
                className="px-4 py-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                disabled={
                  loading || 
                  (!newImage && JSON.stringify(editing) === JSON.stringify(initialEditingData)) ||
                  !editing.title ||
                  !editing.description
                }
                className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg transition-colors disabled:opacity-50"
              >
                Save
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
              Are you sure you want to delete this achievement? This action cannot be undone.
            </p>
            <div className="flex gap-4 justify-end">
              <button
                onClick={() => setDeleteId(null)}
                className="px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
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
