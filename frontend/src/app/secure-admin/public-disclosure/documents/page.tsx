'use client';

import { useEffect, useState, useRef } from 'react';
import Link from 'next/link';
import api from '@/lib/api';

interface DocumentItem {
  id?: number;
  title: string;
  file: string | File | null;
  order: number;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export default function DocumentsPage() {
  const [items, setItems] = useState<DocumentItem[]>([]);
  const [editingItem, setEditingItem] = useState<DocumentItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [errors, setErrors] = useState<Record<string, string[]>>({});
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await api.get('/api/admin/content/documentation/');
      setItems(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      setMessage({ type: 'error', text: 'Failed to load data' });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    if (!editingItem) return;
    const { name, value } = e.target;
    setEditingItem({ ...editingItem, [name]: value });
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: [] }));
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      if (errors.file) {
        setErrors((prev) => ({ ...prev, file: [] }));
      }
    }
  };

  const saveItem = async () => {
    if (!editingItem) return;
    setSaving(true);
    setErrors({});
    setMessage(null);

    try {
      const formData = new FormData();
      formData.append('title', editingItem.title);
      formData.append('order', editingItem.order.toString());
      formData.append('is_active', editingItem.is_active.toString());
      
      if (selectedFile) {
        formData.append('file', selectedFile);
      }

      if (editingItem.id) {
        await api.put(`/api/admin/content/documentation/${editingItem.id}/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      } else {
        if (!selectedFile) {
          setErrors({ file: ['File is required'] });
          setMessage({ type: 'error', text: 'Please select a file to upload.' });
          setSaving(false);
          return;
        }
        await api.post('/api/admin/content/documentation/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }
      await fetchData();
      setEditingItem(null);
      setSelectedFile(null);
      setMessage({ type: 'success', text: 'Document saved successfully' });
    } catch (error: any) {
      console.error('Error saving item:', error);
      if (error.response && error.response.status === 400) {
        setErrors(error.response.data);
        setMessage({ type: 'error', text: 'Please check the form for errors.' });
      } else {
        setMessage({ type: 'error', text: 'Failed to save document' });
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
      await api.delete(`/api/admin/content/documentation/${deleteId}/`);
      await fetchData();
      setMessage({ type: 'success', text: 'Document deleted successfully' });
    } catch (error) {
      console.error('Error deleting item:', error);
      setMessage({ type: 'error', text: 'Failed to delete document' });
    } finally {
      setDeleteId(null);
    }
  };

  const newItem = (): DocumentItem => {
    setErrors({});
    setSelectedFile(null);
    return {
      title: '',
      file: null,
      order: items.length,
      is_active: true,
    };
  };

  const getFileName = (filePath: string | File | null): string => {
    if (!filePath) return '';
    if (typeof filePath === 'string') {
      return filePath.split('/').pop() || '';
    }
    return filePath.name;
  };

  if (loading) return <div className="text-center p-8 text-gray-400">Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto">
      {/* Breadcrumb */}
      <div className="mb-4">
        <Link 
          href="/secure-admin/public-disclosure" 
          className="text-purple-400 hover:text-purple-300 text-sm flex items-center gap-1"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Public Disclosure
        </Link>
      </div>

      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Documents</h1>
        <p className="text-gray-400">Manage documents and files for public disclosure</p>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-xl border ${
          message.type === 'success' ? 'bg-green-500/10 border-green-500/30 text-green-400' : 'bg-red-500/10 border-red-500/30 text-red-400'
        }`}>
          {message.text}
        </div>
      )}

      {/* Documents Table */}
      <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <span className="text-2xl">📄</span>
            Documents List
          </h2>
          <button
            onClick={() => setEditingItem(newItem())}
            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-xl transition-all flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add Document
          </button>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          {items.length === 0 ? (
            <p className="text-gray-400 text-center py-8">No documents yet. Click "Add Document" to upload one.</p>
          ) : (
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-400 w-16">Sl.No.</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-400">Documents/Information</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-400 w-32">Download</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-400 w-20">Status</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-400 w-28">Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item, index) => (
                  <tr key={item.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                    <td className="py-4 px-4 text-gray-300 font-medium">{index + 1}</td>
                    <td className="py-4 px-4 text-white font-medium">{item.title}</td>
                    <td className="py-4 px-4">
                      {item.file && typeof item.file === 'string' && (
                        <a
                          href={item.file}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-2 px-3 py-1.5 bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 rounded-lg transition-colors text-sm"
                        >
                          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                          </svg>
                          Download
                        </a>
                      )}
                    </td>
                    <td className="py-4 px-4">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        item.is_active 
                          ? 'bg-green-500/20 text-green-400' 
                          : 'bg-gray-500/20 text-gray-400'
                      }`}>
                        {item.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <div className="flex justify-end gap-2">
                        <button
                          onClick={() => {
                            setEditingItem(item);
                            setSelectedFile(null);
                          }}
                          className="p-2 text-blue-400 hover:bg-blue-500/20 rounded-lg transition-colors"
                          title="Edit"
                        >
                          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                        <button
                          onClick={() => item.id && requestDelete(item.id)}
                          className="p-2 text-red-400 hover:bg-red-500/20 rounded-lg transition-colors"
                          title="Delete"
                        >
                          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Edit/Add Modal */}
      {editingItem && (
        <div
          className="fixed inset-0 z-50 flex items-start justify-center bg-black/70 backdrop-blur-sm p-4 overflow-y-auto pt-20 pb-10"
          onClick={() => { setEditingItem(null); setSelectedFile(null); }}
        >
          <div
            className="bg-slate-800 rounded-2xl border border-white/10 flex flex-col max-w-lg w-full shadow-2xl relative my-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6 border-b border-white/10">
              <h3 className="text-xl font-bold text-white">
                {editingItem.id ? 'Edit Document' : 'Add New Document'}
              </h3>
            </div>

            <div className="p-6 space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Document Title *</label>
                <input
                  type="text"
                  name="title"
                  required
                  value={editingItem.title}
                  onChange={handleChange}
                  placeholder="e.g., Affiliation Certificate"
                  className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                    errors.title ? 'border-red-500/50' : 'border-white/10'
                  }`}
                />
                {errors.title && (
                  <p className="text-xs text-red-400">{errors.title[0]}</p>
                )}
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">File (PDF, DOC, etc.) *</label>
                <div className="space-y-2">
                  {/* Current file info */}
                  {editingItem.id && editingItem.file && typeof editingItem.file === 'string' && !selectedFile && (
                    <div className="flex items-center gap-2 p-3 bg-white/5 rounded-lg border border-white/10">
                      <svg className="w-5 h-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <span className="text-sm text-gray-300 truncate flex-1">{getFileName(editingItem.file)}</span>
                    </div>
                  )}
                  
                  {/* Selected new file */}
                  {selectedFile && (
                    <div className="flex items-center gap-2 p-3 bg-green-500/10 rounded-lg border border-green-500/30">
                      <svg className="w-5 h-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span className="text-sm text-green-400 truncate flex-1">{selectedFile.name}</span>
                    </div>
                  )}
                  
                  <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.jpg,.jpeg,.png"
                    className="hidden"
                  />
                  <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    className="w-full px-4 py-3 bg-white/5 hover:bg-white/10 border border-dashed border-white/20 rounded-xl text-gray-300 transition-colors flex items-center justify-center gap-2"
                  >
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    {editingItem.id ? 'Replace File' : 'Upload File'}
                  </button>
                </div>
                {errors.file && (
                  <p className="text-xs text-red-400">{errors.file[0]}</p>
                )}
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Order</label>
                  <input
                    type="number"
                    name="order"
                    value={editingItem.order}
                    onChange={(e) => setEditingItem({ ...editingItem, order: parseInt(e.target.value) || 0 })}
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  />
                </div>
                <div className="space-y-2 flex items-end">
                  <label className="flex items-center gap-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={editingItem.is_active}
                      onChange={(e) => setEditingItem({ ...editingItem, is_active: e.target.checked })}
                      className="w-5 h-5 rounded border-gray-600 bg-gray-700 text-purple-600 focus:ring-purple-500"
                    />
                    <span className="text-sm font-medium text-gray-300">Active</span>
                  </label>
                </div>
              </div>
            </div>

            {/* Footer Actions */}
            <div className="p-6 border-t border-white/10 bg-slate-800 rounded-b-2xl">
              <div className="flex gap-3">
                <button
                  onClick={() => { setEditingItem(null); setSelectedFile(null); }}
                  className="flex-1 px-4 py-2.5 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-xl transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={saveItem}
                  disabled={saving || !editingItem.title || (!editingItem.id && !selectedFile)}
                  className="flex-1 px-4 py-2.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold rounded-xl shadow-lg disabled:opacity-50 transition-all"
                >
                  {saving ? 'Saving...' : 'Save'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
      {deleteId && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-slate-900 border border-white/10 rounded-2xl p-6 max-w-md w-full shadow-2xl transform scale-100 transition-all">
            <h3 className="text-xl font-bold text-white mb-2">Confirm Delete</h3>
            <p className="text-gray-400 mb-6">
              Are you sure you want to delete this document? This action cannot be undone.
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
