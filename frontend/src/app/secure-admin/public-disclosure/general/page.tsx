'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import api from '@/lib/api';

interface GeneralInfoItem {
  id?: number;
  title: string;
  value: string;
  order: number;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export default function GeneralPage() {
  const [items, setItems] = useState<GeneralInfoItem[]>([]);
  const [editingItem, setEditingItem] = useState<GeneralInfoItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [errors, setErrors] = useState<Record<string, string[]>>({});
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await api.get('/api/admin/content/general-info/');
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

  const saveItem = async () => {
    if (!editingItem) return;
    setSaving(true);
    setErrors({});
    setMessage(null);

    try {
      if (editingItem.id) {
        await api.put(`/api/admin/content/general-info/${editingItem.id}/`, editingItem);
      } else {
        await api.post('/api/admin/content/general-info/', editingItem);
      }
      await fetchData();
      setEditingItem(null);
      setMessage({ type: 'success', text: 'Item saved successfully' });
    } catch (error: any) {
      console.error('Error saving item:', error);
      if (error.response && error.response.status === 400) {
        setErrors(error.response.data);
        setMessage({ type: 'error', text: 'Please check the form for errors.' });
      } else {
        setMessage({ type: 'error', text: 'Failed to save item' });
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
      await api.delete(`/api/admin/content/general-info/${deleteId}/`);
      await fetchData();
      setMessage({ type: 'success', text: 'Item deleted successfully' });
    } catch (error) {
      console.error('Error deleting item:', error);
      setMessage({ type: 'error', text: 'Failed to delete item' });
    } finally {
      setDeleteId(null);
    }
  };

  const newItem = (): GeneralInfoItem => {
    setErrors({});
    return {
      title: '',
      value: '',
      order: items.length,
      is_active: true,
    };
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
        <h1 className="text-2xl font-bold text-white">General Information</h1>
        <p className="text-gray-400">Manage general information like school timings, affiliation, etc.</p>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-xl border ${
          message.type === 'success' ? 'bg-green-500/10 border-green-500/30 text-green-400' : 'bg-red-500/10 border-red-500/30 text-red-400'
        }`}>
          {message.text}
        </div>
      )}

      {/* Information Table */}
      <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <span className="text-2xl">📋</span>
            Information List
          </h2>
          <button
            onClick={() => setEditingItem(newItem())}
            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-xl transition-all flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add Item
          </button>
        </div>

        {/* Table/List */}
        <div className="overflow-x-auto">
          {items.length === 0 ? (
            <p className="text-gray-400 text-center py-8">No information items yet. Click "Add Item" to create one.</p>
          ) : (
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-400 w-16">Sl.No.</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-400">Title</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-400">Value</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-400 w-20">Status</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-400 w-28">Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item, index) => (
                  <tr key={item.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                    <td className="py-4 px-4 text-gray-300 font-medium">{index + 1}</td>
                    <td className="py-4 px-4 text-white font-medium">{item.title}</td>
                    <td className="py-4 px-4 text-gray-300 max-w-xs truncate">{item.value}</td>
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
                          onClick={() => setEditingItem(item)}
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
          onClick={() => setEditingItem(null)}
        >
          <div
            className="bg-slate-800 rounded-2xl border border-white/10 flex flex-col max-w-lg w-full shadow-2xl relative my-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6 border-b border-white/10">
              <h3 className="text-xl font-bold text-white">
                {editingItem.id ? 'Edit Information' : 'Add New Information'}
              </h3>
            </div>

            <div className="p-6 space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Title *</label>
                <input
                  type="text"
                  name="title"
                  required
                  value={editingItem.title}
                  onChange={handleChange}
                  placeholder="e.g., School Timings"
                  className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                    errors.title ? 'border-red-500/50' : 'border-white/10'
                  }`}
                />
                {errors.title && (
                  <p className="text-xs text-red-400">{errors.title[0]}</p>
                )}
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Value *</label>
                <textarea
                  name="value"
                  required
                  value={editingItem.value}
                  onChange={handleChange}
                  rows={3}
                  placeholder="e.g., 8:00 AM - 3:00 PM"
                  className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                    errors.value ? 'border-red-500/50' : 'border-white/10'
                  }`}
                />
                {errors.value && (
                  <p className="text-xs text-red-400">{errors.value[0]}</p>
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
                  onClick={() => setEditingItem(null)}
                  className="flex-1 px-4 py-2.5 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-xl transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={saveItem}
                  disabled={saving || !editingItem.title || !editingItem.value}
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
              Are you sure you want to delete this item? This action cannot be undone.
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
