'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';

interface ContactSubmission {
  id: number;
  name: string;
  email: string;
  phone: string;
  subject: string;
  message: string;
  is_read: boolean;
  created_at: string;
}

export default function ContactSubmissionsPage() {
  const [submissions, setSubmissions] = useState<ContactSubmission[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<ContactSubmission | null>(null);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const res = await api.get('/api/admin/content/contact/submissions/');
      setSubmissions(res.data);
    } catch (error) {
      console.error('Error fetching submissions:', error);
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (id: number) => {
    try {
      await api.put(`/api/admin/content/contact/submissions/${id}/`, { is_read: true });
      fetchData();
    } catch (error) {
      console.error('Error updating submission:', error);
    }
  };

  const requestDelete = (id: number) => {
    setDeleteId(id);
  };

  const confirmDelete = async () => {
    if (!deleteId) return;
    try {
      await api.delete(`/api/admin/content/contact/submissions/${deleteId}/`);
      fetchData();
      if (selected?.id === deleteId) {
        setSelected(null);
      }
    } catch (error) {
      console.error('Error deleting submission:', error);
    } finally {
      setDeleteId(null);
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const unreadCount = submissions.filter(s => !s.is_read).length;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white">Contact Messages</h1>
          {unreadCount > 0 && (
            <p className="text-gray-400">
              {unreadCount} unread message{unreadCount !== 1 ? 's' : ''}
            </p>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Messages List */}
        <div className="lg:col-span-1 bg-slate-800/50 backdrop-blur-xl border border-white/10 rounded-xl overflow-hidden">
          <div className="divide-y divide-white/10 max-h-[600px] overflow-y-auto">
            {submissions.length === 0 ? (
              <div className="p-8 text-center">
                <div className="text-4xl mb-4">📬</div>
                <p className="text-gray-500">No contact messages yet.</p>
              </div>
            ) : (
              submissions.map((submission) => (
                <button
                  key={submission.id}
                  onClick={() => {
                    setSelected(submission);
                    if (!submission.is_read) {
                      markAsRead(submission.id);
                    }
                  }}
                  className={`w-full text-left p-4 hover:bg-white/5 transition-colors ${
                    selected?.id === submission.id ? 'bg-purple-500/10' : ''
                  } ${!submission.is_read ? 'bg-purple-500/5' : ''}`}
                >
                  <div className="flex items-start gap-3">
                    {!submission.is_read && (
                      <div className="w-2 h-2 bg-purple-500 rounded-full mt-2 flex-shrink-0" />
                    )}
                    <div className="flex-1 min-w-0">
                      <div className="flex justify-between">
                        <p className={`font-medium truncate ${!submission.is_read ? 'text-white' : 'text-gray-300'}`}>
                          {submission.name}
                        </p>
                        <span className="text-xs text-gray-500 flex-shrink-0 ml-2">
                          {formatDate(submission.created_at).split(',')[0]}
                        </span>
                      </div>
                      <p className="text-sm text-white truncate">{submission.subject}</p>
                      <p className="text-xs text-gray-500 truncate">{submission.message}</p>
                    </div>
                  </div>
                </button>
              ))
            )}
          </div>
        </div>

        {/* Message Detail */}
        <div className="lg:col-span-2 bg-slate-800/50 backdrop-blur-xl border border-white/10 rounded-xl p-6">
          {selected ? (
            <div>
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-xl font-semibold text-white">{selected.subject}</h2>
                  <p className="text-sm text-gray-400">{formatDate(selected.created_at)}</p>
                </div>
                <button
                  onClick={() => requestDelete(selected.id)}
                  className="text-red-400 hover:text-red-300 text-sm"
                >
                  Delete
                </button>
              </div>

              <div className="border-b border-white/10 pb-4 mb-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-500">From</p>
                    <p className="font-medium text-white">{selected.name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">Email</p>
                    <a href={`mailto:${selected.email}`} className="font-medium text-purple-400 hover:text-purple-300">
                      {selected.email}
                    </a>
                  </div>
                  {selected.phone && (
                    <div>
                      <p className="text-sm text-gray-500">Phone</p>
                      <a href={`tel:${selected.phone}`} className="font-medium text-purple-400 hover:text-purple-300">
                        {selected.phone}
                      </a>
                    </div>
                  )}
                </div>
              </div>

              <div>
                <p className="text-sm text-gray-500 mb-2">Message</p>
                <div className="bg-white/5 p-4 rounded-xl border border-white/10">
                  <p className="text-gray-300 whitespace-pre-wrap">{selected.message}</p>
                </div>
              </div>

              <div className="flex gap-4 mt-6">
                <a
                  href={`mailto:${selected.email}?subject=Re: ${selected.subject}`}
                  className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
                >
                  Reply via Email
                </a>
                {selected.phone && (
                  <a
                    href={`tel:${selected.phone}`}
                    className="px-4 py-2 border border-white/10 text-gray-300 rounded-lg hover:bg-white/5 transition-colors"
                  >
                    Call
                  </a>
                )}
              </div>
            </div>
          ) : (
            <div className="h-full flex items-center justify-center text-gray-500">
              <div className="text-center">
                <div className="text-4xl mb-4">✉️</div>
                <p>Select a message to view details</p>
              </div>
            </div>
          )}
        </div>
      </div>
      {deleteId && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-slate-900 border border-white/10 rounded-2xl p-6 max-w-md w-full shadow-2xl transform scale-100 transition-all">
            <h3 className="text-xl font-bold text-white mb-2">Confirm Delete</h3>
            <p className="text-gray-400 mb-6">
              Are you sure you want to delete this message? This action cannot be undone.
            </p>
            <div className="flex gap-4 justify-end">
              <button
                onClick={() => setDeleteId(null)}
                className="px-4 py-2 text-gray-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                disabled={loading}
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
