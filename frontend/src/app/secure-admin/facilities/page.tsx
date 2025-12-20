'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import ImageUpload from '@/components/admin/image-upload';
import Link from 'next/link';

interface Facility {
  id: number;
  name: string;
  slug: string;
  short_description: string;
  long_description: string;
  icon: string;
  image: string | null;
  order: number;
  is_active: boolean;
  gallery_count: number;
}

const ICON_OPTIONS = [
  { value: '📚', label: 'Library' },
  { value: '🔬', label: 'Science Lab' },
  { value: '💻', label: 'Computer Lab' },
  { value: '🏃', label: 'Sports' },
  { value: '🎨', label: 'Art Room' },
  { value: '🎵', label: 'Music Room' },
  { value: '🚌', label: 'Transport' },
  { value: '🍽️', label: 'Cafeteria' },
  { value: '🏥', label: 'Medical' },
  { value: '🏫', label: 'Building' },
  { value: '🎭', label: 'Auditorium' },
  { value: '🏊', label: 'Swimming' },
  { value: '🌳', label: 'Garden' },
  { value: '🛡️', label: 'Security' },
];

export default function FacilitiesPage() {
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentFacility, setCurrentFacility] = useState<Partial<Facility>>({});
  const [initialModalData, setInitialModalData] = useState<Partial<Facility> | null>(null);
  const [newImage, setNewImage] = useState<File | null>(null);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    fetchFacilities();
  }, []);

  const fetchFacilities = async () => {
    try {
      const response = await api.get('/api/admin/content/facilities/');
      setFacilities(response.data);
    } catch (error) {
      console.error('Error fetching facilities:', error);
      setMessage({ type: 'error', text: 'Failed to load facilities' });
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (facility: Facility) => {
    setCurrentFacility(facility);
    setInitialModalData(facility);
    setNewImage(null);
    setIsModalOpen(true);
  };

  const requestDelete = (id: number) => {
    setDeleteId(id);
  };

  const confirmDelete = async () => {
    if (!deleteId) return;
    try {
      await api.delete(`/api/admin/content/facilities/${deleteId}/`);
      setFacilities(facilities.filter(f => f.id !== deleteId));
      setMessage({ type: 'success', text: 'Facility deleted' });
    } catch (error) {
      console.error('Error deleting facility:', error);
      setMessage({ type: 'error', text: 'Failed to delete facility' });
    } finally {
      setDeleteId(null);
    }
  };

  const toggleActive = async (facility: Facility) => {
    try {
      await api.patch(`/api/admin/content/facilities/${facility.id}/`, {
        is_active: !facility.is_active
      });
      setFacilities(facilities.map(f => 
        f.id === facility.id ? { ...f, is_active: !f.is_active } : f
      ));
      setMessage({ type: 'success', text: `Facility ${!facility.is_active ? 'activated' : 'deactivated'}` });
    } catch (error) {
      console.error('Error toggling facility:', error);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    
    try {
      const formData = new FormData();
      formData.append('name', currentFacility.name || '');
      formData.append('short_description', currentFacility.short_description || '');
      formData.append('long_description', currentFacility.long_description || '');
      formData.append('icon', currentFacility.icon || '🏫');
      formData.append('order', String(currentFacility.order || 0));
      formData.append('is_active', String(currentFacility.is_active ?? true));
      
      if (newImage) {
        formData.append('cover_image', newImage);
      }

      if (currentFacility.id) {
        await api.put(`/api/admin/content/facilities/${currentFacility.id}/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
      } else {
        await api.post('/api/admin/content/facilities/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
      }
      
      fetchFacilities();
      setIsModalOpen(false);
      setCurrentFacility({});
      setNewImage(null);
      setMessage({ type: 'success', text: 'Facility saved successfully' });
    } catch (error) {
      console.error('Error saving facility:', error);
      setMessage({ type: 'error', text: 'Failed to save facility' });
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="text-center p-8 text-gray-400">Loading...</div>;

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Facilities</h1>
          <p className="text-gray-400">Manage school facilities with galleries</p>
        </div>
        <button
          onClick={() => { 
            const newFac: Partial<Facility> = { order: facilities.length, is_active: true, icon: '🏫' };
            setCurrentFacility(newFac); 
            setInitialModalData(newFac);
            setNewImage(null); 
            setIsModalOpen(true); 
          }}
          className="px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold rounded-xl transition-all flex items-center gap-2 shadow-lg"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add Facility
        </button>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-xl border ${
          message.type === 'success' ? 'bg-green-500/10 border-green-500/30 text-green-400' : 'bg-red-500/10 border-red-500/30 text-red-400'
        }`}>
          {message.text}
        </div>
      )}

      {facilities.length === 0 ? (
        <div className="text-center py-16 bg-slate-800/50 rounded-2xl border border-white/10">
          <span className="text-6xl mb-4 block">🏫</span>
          <h3 className="text-xl font-bold text-white mb-2">No Facilities Yet</h3>
          <p className="text-gray-400 mb-6">Add your first facility to display on the website</p>
          <button
            onClick={() => { 
              const newFac: Partial<Facility> = { order: 0, is_active: true, icon: '🏫' };
              setCurrentFacility(newFac); 
              setInitialModalData(newFac);
              setIsModalOpen(true); 
            }}
            className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-xl transition-colors"
          >
            Add First Facility
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {facilities.sort((a, b) => a.order - b.order).map((facility) => (
            <div 
              key={facility.id} 
              className={`relative bg-slate-800/50 backdrop-blur-xl border rounded-2xl overflow-hidden transition-all ${
                facility.is_active ? 'border-white/10' : 'border-red-500/30 opacity-60'
              }`}
            >
              {/* Status Badge */}
              <div className={`absolute top-3 right-3 px-2 py-1 rounded-full text-xs font-bold z-10 ${
                facility.is_active ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
              }`}>
                {facility.is_active ? 'Active' : 'Inactive'}
              </div>

              {/* Image or Placeholder */}
              <div className="h-40 bg-gradient-to-br from-purple-500/20 to-indigo-500/20 flex items-center justify-center relative">
                {facility.image ? (
                  <img src={facility.image} alt={facility.name} className="w-full h-full object-fill" />
                ) : (
                  <span className="text-6xl opacity-50">{facility.icon}</span>
                )}
                {/* Gallery badge */}
                {facility.gallery_count > 0 && (
                  <div className="absolute bottom-3 left-3 px-2 py-1 bg-black/60 backdrop-blur-sm rounded-lg text-xs text-white flex items-center gap-1">
                    <span>📷</span> {facility.gallery_count} photos
                  </div>
                )}
              </div>

              {/* Content */}
              <div className="p-5">
                <div className="flex items-start gap-3 mb-3">
                  <span className="text-3xl">{facility.icon}</span>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-lg font-bold text-white truncate">{facility.name}</h3>
                    <p className="text-xs text-gray-500">Order: {facility.order} • Slug: {facility.slug || 'auto'}</p>
                  </div>
                </div>
                <p className="text-sm text-gray-400 line-clamp-2 mb-4">{facility.short_description}</p>

                {/* Actions */}
                <div className="flex items-center gap-2 pt-3 border-t border-white/10">
                  <Link 
                    href={`/secure-admin/facilities/${facility.id}/gallery`}
                    className="flex-1 px-3 py-2 bg-indigo-500/20 text-indigo-400 hover:bg-indigo-500/30 rounded-lg text-sm font-medium transition-colors text-center"
                  >
                    📷 Gallery
                  </Link>
                  <button 
                    onClick={() => toggleActive(facility)}
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      facility.is_active 
                        ? 'bg-orange-500/20 text-orange-400 hover:bg-orange-500/30' 
                        : 'bg-green-500/20 text-green-400 hover:bg-green-500/30'
                    }`}
                  >
                    {facility.is_active ? 'Hide' : 'Show'}
                  </button>
                  <button 
                    onClick={() => handleEdit(facility)} 
                    className="p-2 bg-blue-500/20 text-blue-400 hover:bg-blue-500/30 rounded-lg transition-colors"
                  >
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </button>
                  <button 
                    onClick={() => requestDelete(facility.id)} 
                    className="p-2 bg-red-500/20 text-red-400 hover:bg-red-500/30 rounded-lg transition-colors"
                  >
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {isModalOpen && (
        <div 
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => setIsModalOpen(false)}
        >
          <div 
            className="bg-slate-900 border border-white/10 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6 border-b border-white/10 flex items-center justify-between">
              <h2 className="text-xl font-bold text-white">
                {currentFacility.id ? 'Edit Facility' : 'Add Facility'}
              </h2>
              <button onClick={() => setIsModalOpen(false)} className="text-gray-400 hover:text-white">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <form onSubmit={handleSave} className="p-6 space-y-5">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Facility Name *</label>
                <input
                  type="text"
                  required
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  value={currentFacility.name || ''}
                  onChange={e => setCurrentFacility(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="e.g., Library, Computer Lab"
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Description *</label>
                <textarea
                  required
                  rows={2}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  value={currentFacility.short_description || ''}
                  onChange={e => setCurrentFacility(prev => ({ ...prev, short_description: e.target.value }))}
                  placeholder="Brief description shown on facility cards..."
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Long Description (for detail page)</label>
                <textarea
                  rows={4}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  value={currentFacility.long_description || ''}
                  onChange={e => setCurrentFacility(prev => ({ ...prev, long_description: e.target.value }))}
                  placeholder="Detailed description for the facility page..."
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Icon</label>
                <div className="grid grid-cols-7 gap-2">
                  {ICON_OPTIONS.map((icon) => (
                    <button
                      key={icon.value}
                      type="button"
                      onClick={() => setCurrentFacility(prev => ({ ...prev, icon: icon.value }))}
                      className={`p-3 rounded-xl text-2xl transition-all ${
                        currentFacility.icon === icon.value 
                          ? 'bg-purple-500/30 ring-2 ring-purple-500' 
                          : 'bg-white/5 hover:bg-white/10'
                      }`}
                      title={icon.label}
                    >
                      {icon.value}
                    </button>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Display Order</label>
                  <input
                    type="number"
                    min="0"
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    value={currentFacility.order || 0}
                    onChange={e => setCurrentFacility(prev => ({ ...prev, order: parseInt(e.target.value) || 0 }))}
                  />
                </div>
                <div className="space-y-2 flex flex-col justify-end">
                  <label className="flex items-center gap-3 cursor-pointer p-2.5 bg-white/5 rounded-xl">
                    <input
                      type="checkbox"
                      checked={currentFacility.is_active ?? true}
                      onChange={e => setCurrentFacility(prev => ({ ...prev, is_active: e.target.checked }))}
                      className="w-5 h-5 rounded border-gray-600 bg-gray-700 text-purple-600 focus:ring-purple-500"
                    />
                    <span className="text-sm font-medium text-gray-300">Active</span>
                  </label>
                </div>
              </div>

              <div>
                <ImageUpload
                  label="Cover Image"
                  currentImage={currentFacility.image || null}
                  onChange={(file) => setNewImage(file)}
                />
              </div>
              
              <div className="pt-4 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-5 py-2.5 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl transition-colors font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={
                    saving || 
                    (JSON.stringify(currentFacility) === JSON.stringify(initialModalData) && !newImage) ||
                    !currentFacility.name || 
                    !currentFacility.short_description
                  }
                  className="px-6 py-2.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold rounded-xl transition-all disabled:opacity-50 shadow-lg"
                >
                  {saving ? 'Saving...' : 'Save Facility'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
      {deleteId && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-slate-900 border border-white/10 rounded-2xl p-6 max-w-md w-full shadow-2xl transform scale-100 transition-all">
            <h3 className="text-xl font-bold text-white mb-2">Confirm Delete</h3>
            <p className="text-gray-400 mb-6">
              Are you sure you want to delete this facility? This action cannot be undone.
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
