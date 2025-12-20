'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';

interface Notice {
  id: number;
  title: string;
  content: string;
  status: 'draft' | 'published' | 'archived';
  is_important: boolean;
  publish_date: string;
  attachment: string | null;
}

export default function NoticesPage() {
  const [notices, setNotices] = useState<Notice[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentNotice, setCurrentNotice] = useState<Partial<Notice>>({});
  const [initialModalData, setInitialModalData] = useState<Partial<Notice> | null>(null);
  const [saving, setSaving] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileInputKey, setFileInputKey] = useState(0);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    fetchNotices();
  }, []);

  const fetchNotices = async () => {
    try {
      const response = await api.get('/api/admin/content/notices/');
      setNotices(response.data);
    } catch (error) {
      console.error('Error fetching notices:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (notice: Notice) => {
    setCurrentNotice(notice);
    setInitialModalData(notice);
    setSelectedFile(null);
    setFileInputKey(prev => prev + 1);
    setIsModalOpen(true);
  };

  const requestDelete = (id: number) => {
    setDeleteId(id);
  };

  const confirmDelete = async () => {
    if (!deleteId) return;
    setSaving(true);
    
    try {
      await api.delete(`/api/admin/content/notices/${deleteId}/`);
      setNotices(notices.filter(n => n.id !== deleteId));
    } catch (error) {
      console.error('Error deleting notice:', error);
    } finally {
      setSaving(false);
      setDeleteId(null);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    
    try {
      const formData = new FormData();
      formData.append('title', currentNotice.title || '');
      formData.append('content', currentNotice.content || '');
      formData.append('status', currentNotice.status || 'draft');
      formData.append('is_important', String(currentNotice.is_important || false));
      
      const publishDate = currentNotice.publish_date 
        ? new Date(currentNotice.publish_date).toISOString().split('T')[0] 
        : new Date().toISOString().split('T')[0];
      formData.append('publish_date', publishDate);

      if (selectedFile) {
        formData.append('attachment', selectedFile);
      }

      // Explicitly set headers for multipart/form-data
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      };

      if (currentNotice.id) {
        await api.put(`/api/admin/content/notices/${currentNotice.id}/`, formData, config);
      } else {
        await api.post('/api/admin/content/notices/', formData, config);
      }
      
      fetchNotices();
      setIsModalOpen(false);
      setCurrentNotice({});
      setSelectedFile(null);
    } catch (error) {
      console.error('Error saving notice:', error);
      alert('Error saving notice. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="text-center p-8 text-gray-400">Loading...</div>;

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Notices</h1>
          <p className="text-gray-400">Manage school announcements</p>
        </div>
        <button
          onClick={() => { 
            const newNotice = {};
            setCurrentNotice(newNotice);
            setInitialModalData(newNotice);
            setIsModalOpen(true); 
          }}
          className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add Notice
        </button>
      </div>

      {/* List */}
      <div className="grid gap-4">
        {notices.map((notice) => (
          <div key={notice.id} className="bg-slate-800/50 backdrop-blur-xl border border-white/10 rounded-xl p-4 flex items-center justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-1">
                <h3 className="font-semibold text-white">{notice.title}</h3>
                {notice.is_important && (
                  <span className="px-2 py-0.5 text-xs bg-red-500/20 text-red-400 rounded-full border border-red-500/20">Important</span>
                )}
                <span className={`px-2 py-0.5 text-xs rounded-full border ${
                  notice.status === 'published' 
                    ? 'bg-green-500/20 text-green-400 border-green-500/20' 
                    : 'bg-yellow-500/20 text-yellow-400 border-yellow-500/20'
                }`}>
                  {notice.status}
                </span>
              </div>
              <p className="text-sm text-gray-400 line-clamp-1">{notice.content}</p>
              <div className="flex items-center gap-4 mt-2">
                <div className="text-xs text-gray-500">
                  Published: {new Date(notice.publish_date).toLocaleDateString()}
                </div>
                {notice.attachment && (
                  <a 
                    href={notice.attachment} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="flex items-center gap-1 text-xs text-purple-400 hover:text-purple-300 transition-colors"
                  >
                    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                    </svg>
                    View Attachment
                  </a>
                )}
              </div>
            </div>
            
            <div className="flex items-center gap-2 ml-4">
              <button
                onClick={() => handleEdit(notice)}
                className="p-2 hover:bg-white/5 rounded-lg text-gray-400 hover:text-white transition-colors"
                title="Edit"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button
                onClick={() => requestDelete(notice.id)}
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

        {notices.length === 0 && (
          <div className="text-center py-12 text-gray-500 bg-slate-800/20 rounded-xl border border-white/5">
            No notices found. Create one to get started.
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
                {currentNotice.id ? 'Edit Notice' : 'New Notice'}
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
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  value={currentNotice.title || ''}
                  onChange={e => setCurrentNotice(prev => ({ ...prev, title: e.target.value }))}
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Content *</label>
                <textarea
                  required
                  rows={4}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  value={currentNotice.content || ''}
                  onChange={e => setCurrentNotice(prev => ({ ...prev, content: e.target.value }))}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Publish Date</label>
                  <input
                    type="date"
                    required
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    value={currentNotice.publish_date ? new Date(currentNotice.publish_date).toISOString().split('T')[0] : ''}
                    onChange={e => setCurrentNotice(prev => ({ ...prev, publish_date: e.target.value }))}
                  />
                </div>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Status</label>
                  <select
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    value={currentNotice.status || 'draft'}
                    onChange={e => setCurrentNotice(prev => ({ ...prev, status: e.target.value as any }))}
                  >
                    <option value="draft">Draft</option>
                    <option value="published">Published</option>
                    <option value="archived">Archived</option>
                  </select>
                </div>
              </div>

              <div className="flex items-center gap-2 pt-2">
                <input
                  type="checkbox"
                  id="is_important"
                  className="w-5 h-5 rounded border-gray-600 bg-gray-700 text-purple-600 focus:ring-purple-500"
                  checked={currentNotice.is_important || false}
                  onChange={e => setCurrentNotice(prev => ({ ...prev, is_important: e.target.checked }))}
                />
                <label htmlFor="is_important" className="text-sm font-medium text-gray-300">Mark as Important (Sticky)</label>
              </div>

              <div className="space-y-2 pt-2">
                <label className="text-sm font-medium text-gray-300">Attachment (Optional)</label>
                <div className="flex flex-col gap-2">
                  <input
                    key={fileInputKey}
                    type="file"
                    className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-purple-500/50 file:mr-4 file:py-1 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-purple-600 file:text-white hover:file:bg-purple-700"
                    onChange={e => setSelectedFile(e.target.files?.[0] || null)}
                  />
                  {currentNotice.attachment && !selectedFile && (
                    <p className="text-xs text-gray-500 truncate">
                      Current: {currentNotice.attachment.split('/').pop()}
                    </p>
                  )}
                  {selectedFile && (
                    <p className="text-xs text-green-400">
                      New file selected: {selectedFile.name}
                    </p>
                  )}
                </div>
                <p className="text-[10px] text-gray-500">Supported: PDF, Images, Word, etc.</p>
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
                    (JSON.stringify(currentNotice) === JSON.stringify(initialModalData) && !selectedFile) ||
                    !currentNotice.title || 
                    !currentNotice.content || 
                    !currentNotice.publish_date
                  }
                  className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg transition-colors disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Notice'}
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
              Are you sure you want to delete this notice? This action cannot be undone.
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
