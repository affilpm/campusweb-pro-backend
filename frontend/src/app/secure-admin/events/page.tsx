'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import ImageUpload from '@/components/admin/image-upload';

interface Event {
  id: number;
  title: string;
  excerpt: string;
  content: string;
  status: 'draft' | 'published' | 'archived';
  is_featured: boolean;
  event_date: string;
  image: string | null;
}

export default function EventsPage() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentEvent, setCurrentEvent] = useState<Partial<Event>>({});
  const [initialEventData, setInitialEventData] = useState<Partial<Event> | null>(null);
  const [newImage, setNewImage] = useState<File | null>(null);
  const [saving, setSaving] = useState(false);
  const [errors, setErrors] = useState<Record<string, string[]>>({});
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await api.get('/api/admin/content/events/');
      setEvents(response.data);
    } catch (error) {
      console.error('Error fetching events:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (event: Event) => {
    setCurrentEvent(event);
    setInitialEventData({ ...event });
    setNewImage(null);
    setErrors({});
    setIsModalOpen(true);
  };

  const requestDelete = (id: number) => {
    setDeleteId(id);
  };

  const confirmDelete = async () => {
    if (!deleteId) return;
    setSaving(true);
    
    try {
      await api.delete(`/api/admin/content/events/${deleteId}/`);
      setEvents(events.filter(n => n.id !== deleteId));
    } catch (error) {
      console.error('Error deleting event:', error);
    } finally {
      setSaving(false);
      setDeleteId(null);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setErrors({});
    
    try {
      const formData = new FormData();
      formData.append('title', currentEvent.title || '');
      formData.append('excerpt', currentEvent.excerpt || '');
      formData.append('content', currentEvent.content || '');
      formData.append('status', currentEvent.status || 'draft');
      formData.append('is_featured', String(currentEvent.is_featured || false));
      
      if (currentEvent.event_date) {
        formData.append('event_date', new Date(currentEvent.event_date).toISOString().split('T')[0]);
      }
      
      if (newImage) {
        formData.append('image', newImage);
      }

      if (currentEvent.id) {
        await api.put(`/api/admin/content/events/${currentEvent.id}/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
      } else {
        await api.post('/api/admin/content/events/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
      }
      
      fetchEvents();
      setIsModalOpen(false);
      setCurrentEvent({});
      setInitialEventData(null);
      setNewImage(null);
    } catch (error: any) {
      console.error('Error saving event:', error);
      if (error.response && error.response.status === 400) {
        setErrors(error.response.data);
      }
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="text-center p-8 text-gray-400">Loading...</div>;

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Events & News</h1>
          <p className="text-gray-400">Manage school events and latest news</p>
        </div>
        <button
          onClick={() => { 
            const newEvent = { title: '', excerpt: '', content: '', status: 'draft' as const, is_featured: false };
            setCurrentEvent(newEvent); 
            setInitialEventData(newEvent);
            setNewImage(null); 
            setErrors({}); 
            setIsModalOpen(true); 
          }}
          className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add Event
        </button>
      </div>

      {/* List */}
      <div className="grid gap-4">
        {events.map((event) => (
          <div key={event.id} className="bg-slate-800/50 backdrop-blur-xl border border-white/10 rounded-xl p-4 flex gap-4">
            <div className="w-24 h-24 bg-white/5 rounded-lg overflow-hidden flex-shrink-0">
                {event.image ? (
                    <img src={event.image} alt={event.title} className="w-full h-full object-fill" />
                ) : (
                    <div className="w-full h-full flex items-center justify-center text-gray-600">
                        <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                    </div>
                )}
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3 mb-1">
                <h3 className="font-semibold text-white truncate">{event.title}</h3>
                {event.is_featured && (
                  <span className="px-2 py-0.5 text-xs bg-purple-500/20 text-purple-400 rounded-full border border-purple-500/20">Featured</span>
                )}
                <span className={`px-2 py-0.5 text-xs rounded-full border ${
                  event.status === 'published' 
                    ? 'bg-green-500/20 text-green-400 border-green-500/20' 
                    : 'bg-yellow-500/20 text-yellow-400 border-yellow-500/20'
                }`}>
                  {event.status}
                </span>
              </div>
              <p className="text-sm text-gray-400 line-clamp-2 mb-2">{event.excerpt}</p>
              <div className="text-xs text-gray-500">
                Event Date: {event.event_date ? new Date(event.event_date).toLocaleDateString() : 'N/A'}
              </div>
            </div>
            
            <div className="flex flex-col gap-2 ml-4">
              <button
                onClick={() => handleEdit(event)}
                className="p-2 hover:bg-white/5 rounded-lg text-gray-400 hover:text-white transition-colors"
                title="Edit"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button
                onClick={() => requestDelete(event.id)}
                className="p-2 hover:bg-red-500/10 rounded-lg text-gray-400 hover:text-red-400 transition-colors"
                title="Delete"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        ))}

        {events.length === 0 && (
          <div className="text-center py-12 text-gray-500 bg-slate-800/20 rounded-xl border border-white/5">
            No events found. Create one to get started.
          </div>
        )}
      </div>

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
                {currentEvent.id ? 'Edit Event' : 'New Event'}
              </h2>
              <button onClick={() => setIsModalOpen(false)} className="text-gray-400 hover:text-white">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <form onSubmit={handleSave} className="p-6 space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Title *</label>
                <input
                  type="text"
                  required
                  className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                    errors.title ? 'border-red-500/50' : 'border-white/10'
                  }`}
                  value={currentEvent.title || ''}
                  onChange={e => {
                    setCurrentEvent(prev => ({ ...prev, title: e.target.value }));
                    if (errors.title) setErrors(prev => ({ ...prev, title: [] }));
                  }}
                />
                {errors.title && <p className="text-xs text-red-400">{errors.title[0]}</p>}
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Summary (Excerpt) *</label>
                <textarea
                  required
                  rows={2}
                  className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                    errors.excerpt ? 'border-red-500/50' : 'border-white/10'
                  }`}
                  value={currentEvent.excerpt || ''}
                  onChange={e => {
                    setCurrentEvent(prev => ({ ...prev, excerpt: e.target.value }))
                    if (errors.excerpt) setErrors(prev => ({ ...prev, excerpt: [] }));
                  }}
                />
                {errors.excerpt && <p className="text-xs text-red-400">{errors.excerpt[0]}</p>}
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Full Content *</label>
                <textarea
                  required
                  rows={4}
                  className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                    errors.content ? 'border-red-500/50' : 'border-white/10'
                  }`}
                  value={currentEvent.content || ''}
                  onChange={e => {
                    setCurrentEvent(prev => ({ ...prev, content: e.target.value }));
                    if (errors.content) setErrors(prev => ({ ...prev, content: [] }));
                  }}
                />
                {errors.content && <p className="text-xs text-red-400">{errors.content[0]}</p>}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Event Date</label>
                  <input
                    type="date"
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    value={currentEvent.event_date ? new Date(currentEvent.event_date).toISOString().split('T')[0] : ''}
                    onChange={e => setCurrentEvent(prev => ({ ...prev, event_date: e.target.value }))}
                  />
                </div>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Status</label>
                  <select
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    value={currentEvent.status || 'draft'}
                    onChange={e => setCurrentEvent(prev => ({ ...prev, status: e.target.value as any }))}
                  >
                    <option value="draft">Draft</option>
                    <option value="published">Published</option>
                    <option value="archived">Archived</option>
                  </select>
                </div>
              </div>

              <div>
                <ImageUpload
                  label="Event Image"
                  currentImage={currentEvent.image || null}
                  onChange={(file) => setNewImage(file)}
                />
              </div>

              <div className="flex items-center gap-2 pt-2">
                <input
                  type="checkbox"
                  id="is_featured"
                  className="w-5 h-5 rounded border-gray-600 bg-gray-700 text-purple-600 focus:ring-purple-500"
                  checked={currentEvent.is_featured || false}
                  onChange={e => setCurrentEvent(prev => ({ ...prev, is_featured: e.target.checked }))}
                />
                <label htmlFor="is_featured" className="text-sm font-medium text-gray-300">Feature on Homepage</label>
              </div>

              <div className="pt-6 flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={
                    saving || 
                    (JSON.stringify(currentEvent) === JSON.stringify(initialEventData) && !newImage) ||
                    !currentEvent.title ||
                    !currentEvent.excerpt ||
                    !currentEvent.content
                  }
                  className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg transition-colors disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Event'}
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
              Are you sure you want to delete this event? This action cannot be undone.
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
                disabled={saving}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg shadow-lg shadow-red-600/20 transition-all"
              >
                {saving ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
