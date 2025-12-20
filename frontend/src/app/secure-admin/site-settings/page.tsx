'use client';

import { useEffect, useState, FormEvent, useRef } from 'react';
import { useAuth } from '@/contexts/auth-context';
import api from '@/lib/api';

interface QuickLink {
  id: number;
  title: string;
  url: string;
  order: number;
  is_active: boolean;
  open_in_new_tab: boolean;
}

interface SiteSettings {
  school_name: string;
  school_motto: string;
  school_logo: string | null;
  address: string;
  phone: string;
  email: string;
  facebook_url: string;
  twitter_url: string;
  instagram_url: string;
  youtube_url: string;
  footer_text: string;
}

export default function SiteSettingsPage() {
  const [activeTab, setActiveTab] = useState<'settings' | 'links'>('settings');
  const [settings, setSettings] = useState<SiteSettings>({
    school_name: '',
    school_motto: '',
    school_logo: null,
    address: '',
    phone: '',
    email: '',
    facebook_url: '',
    twitter_url: '',
    instagram_url: '',
    youtube_url: '',
    footer_text: '',
  });
  const [quickLinks, setQuickLinks] = useState<QuickLink[]>([]);
  const [initialSettings, setInitialSettings] = useState<SiteSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [errors, setErrors] = useState<Record<string, string[]>>({});
  const [newLogo, setNewLogo] = useState<File | null>(null);
  const [logoPreview, setLogoPreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Quick Link Form State
  const [isEditingLink, setIsEditingLink] = useState(false);
  const [currentLink, setCurrentLink] = useState<Partial<QuickLink>>({
    title: '',
    url: '',
    order: 0,
    is_active: true,
    open_in_new_tab: false,
  });
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  // Auto-dismiss message after 3 seconds
  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => {
        setMessage(null);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [message]);

  const fetchData = async () => {
    try {
      const [settingsRes, linksRes] = await Promise.all([
        api.get('/api/admin/content/settings/'),
        api.get('/api/admin/content/quick-links/'),
      ]);
      setSettings(settingsRes.data);
      setInitialSettings(settingsRes.data);
      setQuickLinks(linksRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      setMessage({ type: 'error', text: 'Failed to load data' });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setSettings((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: [] }));
    }
  };

  const handleLogoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setNewLogo(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setLogoPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeLogo = () => {
    setNewLogo(null);
    setLogoPreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);
    setErrors({});

    try {
      const formData = new FormData();
      // Append all text fields
      Object.keys(settings).forEach(key => {
         if (key !== 'school_logo' && key !== 'favicon') {
             formData.append(key, (settings as any)[key]);
         }
      });

      if (newLogo) {
        formData.append('school_logo', newLogo);
      }

      // Explicitly unset Content-Type to let the browser handle the boundary
      const response = await api.put('/api/admin/content/settings/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data', 
        },
        transformRequest: (data, headers) => {
          delete headers['Content-Type'];
          return data;
        },
      });
      
      setSettings(response.data);
      setInitialSettings(response.data);
      setNewLogo(null);
      setLogoPreview(null);
      setMessage({ type: 'success', text: 'Settings updated successfully' });
    } catch (error: any) {
      console.error('Error updating settings:', error);
      if (error.response && error.response.status === 400) {
        setErrors(error.response.data);
        setMessage({ type: 'error', text: 'Please check the form for errors.' });
      } else {
        setMessage({ type: 'error', text: 'Failed to update settings. Please try again.' });
      }
    } finally {
      setSaving(false);
    }
  };

  const hasChanges = () => {
    if (!initialSettings) return false;
    if (newLogo) return true;
    return JSON.stringify(settings) !== JSON.stringify(initialSettings);
  };

  // Quick Link Handlers
  const handleLinkSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (currentLink.id) {
        await api.patch(`/api/admin/content/quick-links/${currentLink.id}/`, currentLink);
      } else {
        await api.post('/api/admin/content/quick-links/', currentLink);
      }
      setIsEditingLink(false);
      resetLinkForm();
      fetchData(); // Reload both to be safe, or separate reload logic
      setMessage({ type: 'success', text: 'Quick link saved successfully' });
    } catch (error) {
      console.error('Error saving quick link:', error);
      setMessage({ type: 'error', text: 'Failed to save quick link' });
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
      await api.delete(`/api/admin/content/quick-links/${deleteId}/`);
      fetchData();
      setMessage({ type: 'success', text: 'Quick link deleted' });
    } catch (error) {
      console.error('Error deleting link:', error);
      setMessage({ type: 'error', text: 'Failed to delete link' });
    } finally {
      setDeleteId(null);
    }
  };

  const resetLinkForm = () => {
    setCurrentLink({
      title: '',
      url: '',
      order: 0,
      is_active: true,
      open_in_new_tab: false,
    });
  };


  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Site Settings</h1>
          <p className="text-gray-400">Manage general school information, contact details, and footer links</p>
        </div>
      </div>

      {message && (
        <div className={`fixed bottom-8 right-8 z-50 max-w-sm w-full px-6 py-4 rounded-xl shadow-2xl backdrop-blur-xl border transition-all duration-300 transform translate-y-0 ${
          message.type === 'success' 
            ? 'bg-teal-600/90 border-teal-400 text-white' 
            : 'bg-rose-600/90 border-rose-400 text-white'
        }`}>
          <div className="flex items-start gap-3">
            <span className="text-xl shrink-0 mt-0.5">{message.type === 'success' ? '✅' : '⚠️'}</span>
            <div className="flex-1">
              <h3 className="font-semibold text-lg">{message.type === 'success' ? 'Success' : 'Error'}</h3>
              <p className="text-white/90 text-sm mt-1">{message.text}</p>
            </div>
            <button 
              onClick={() => setMessage(null)} 
              className="group shrink-0 bg-white/10 hover:bg-white/20 rounded-lg p-1 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-4 mb-8 border-b border-white/10">
        <button
          onClick={() => setActiveTab('settings')}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'settings'
              ? 'border-purple-500 text-white'
              : 'border-transparent text-gray-400 hover:text-white'
          }`}
        >
          General Settings
        </button>
        <button
          onClick={() => setActiveTab('links')}
          className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'links'
              ? 'border-purple-500 text-white'
              : 'border-transparent text-gray-400 hover:text-white'
          }`}
        >
          Footer Quick Links
        </button>
      </div>

      {activeTab === 'settings' && (
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* School Logo */}
        <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
          <h2 className="text-lg font-semibold text-white mb-4">School Logo</h2>
          <div className="flex items-start gap-6">
            {/* Logo Preview */}
            <div className="flex-shrink-0">
              <div className="w-32 h-32 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center overflow-hidden">
                {logoPreview || settings.school_logo ? (
                  <img 
                    src={logoPreview || settings.school_logo || ''} 
                    alt="School Logo" 
                    className="w-full h-full object-contain"
                  />
                ) : (
                  <div className="text-center text-gray-500">
                    <svg className="w-12 h-12 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span className="text-xs">No Logo</span>
                  </div>
                )}
              </div>
            </div>

            {/* Upload Controls */}
            <div className="flex-1">
              <p className="text-sm text-gray-400 mb-4">
                Upload your school logo. Recommended size: 200x200 pixels. Supported formats: PNG, JPG, SVG.
              </p>
              <div className="flex gap-3">
                <label className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-xl cursor-pointer transition-colors">
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleLogoChange}
                    className="hidden"
                  />
                  {settings.school_logo || newLogo ? 'Change Logo' : 'Upload Logo'}
                </label>
                {(settings.school_logo || newLogo) && (
                  <button
                    type="button"
                    onClick={removeLogo}
                    className="px-4 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 font-medium rounded-xl transition-colors"
                  >
                    Remove
                  </button>
                )}
              </div>
              {newLogo && (
                <div className="mt-3">
                  <p className="text-sm text-green-400 font-medium break-all">
                    Selected: {newLogo.name}
                  </p>
                  <p className="text-xs text-yellow-500 mt-1 animate-pulse">
                    ⚠️ Click "Save Changes" at the bottom to apply
                  </p>
                </div>
              )}
              {errors.school_logo && (
                <p className="mt-2 text-xs text-red-400">{errors.school_logo[0]}</p>
              )}
            </div>
          </div>
        </div>

        {/* General Info */}
        <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
          <h2 className="text-lg font-semibold text-white mb-4">General Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">School Name *</label>
              <input
                type="text"
                name="school_name"
                value={settings.school_name}
                onChange={handleChange}
                required
                className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                  errors.school_name ? 'border-red-500/50' : 'border-white/10'
                }`}
              />
              {errors.school_name && (
                <p className="text-xs text-red-400">{errors.school_name[0]}</p>
              )}
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Motto *</label>
              <input
                type="text"
                name="school_motto"
                value={settings.school_motto}
                onChange={handleChange}
                required
                className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                  errors.school_motto ? 'border-red-500/50' : 'border-white/10'
                }`}
              />
              {errors.school_motto && (
                <p className="text-xs text-red-400">{errors.school_motto[0]}</p>
              )}
            </div>
          </div>
        </div>

        {/* Contact Info */}
        <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
          <h2 className="text-lg font-semibold text-white mb-4">Contact Details</h2>
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Phone *</label>
                <input
                  type="text"
                  name="phone"
                  value={settings.phone}
                  onChange={handleChange}
                  required
                  className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                    errors.phone ? 'border-red-500/50' : 'border-white/10'
                  }`}
                />
                {errors.phone && (
                  <p className="text-xs text-red-400">{errors.phone[0]}</p>
                )}
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Email *</label>
                <input
                  type="email"
                  name="email"
                  value={settings.email}
                  onChange={handleChange}
                  required
                  className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                    errors.email ? 'border-red-500/50' : 'border-white/10'
                  }`}
                />
                {errors.email && (
                  <p className="text-xs text-red-400">{errors.email[0]}</p>
                )}
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Address *</label>
              <textarea
                name="address"
                value={settings.address}
                onChange={handleChange}
                rows={3}
                required
                className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                  errors.address ? 'border-red-500/50' : 'border-white/10'
                }`}
              />
              {errors.address && (
                <p className="text-xs text-red-400">{errors.address[0]}</p>
              )}
            </div>
          </div>
        </div>

        {/* Social Media */}
        <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
          <h2 className="text-lg font-semibold text-white mb-4">Social Media</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Facebook URL</label>
              <input
                type="url"
                name="facebook_url"
                value={settings.facebook_url}
                onChange={handleChange}
                className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                  errors.facebook_url ? 'border-red-500/50' : 'border-white/10'
                }`}
              />
              {errors.facebook_url && (
                <p className="text-xs text-red-400">{errors.facebook_url[0]}</p>
              )}
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Twitter URL</label>
              <input
                type="url"
                name="twitter_url"
                value={settings.twitter_url}
                onChange={handleChange}
                className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                  errors.twitter_url ? 'border-red-500/50' : 'border-white/10'
                }`}
              />
              {errors.twitter_url && (
                <p className="text-xs text-red-400">{errors.twitter_url[0]}</p>
              )}
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Instagram URL</label>
              <input
                type="url"
                name="instagram_url"
                value={settings.instagram_url}
                onChange={handleChange}
                className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                  errors.instagram_url ? 'border-red-500/50' : 'border-white/10'
                }`}
              />
              {errors.instagram_url && (
                <p className="text-xs text-red-400">{errors.instagram_url[0]}</p>
              )}
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">YouTube URL</label>
              <input
                type="url"
                name="youtube_url"
                value={settings.youtube_url}
                onChange={handleChange}
                className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                  errors.youtube_url ? 'border-red-500/50' : 'border-white/10'
                }`}
              />
              {errors.youtube_url && (
                <p className="text-xs text-red-400">{errors.youtube_url[0]}</p>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
          <h2 className="text-lg font-semibold text-white mb-4">Footer</h2>
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Copyright Text *</label>
            <input
              type="text"
              name="footer_text"
              value={settings.footer_text}
              onChange={handleChange}
              required
              className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                errors.footer_text ? 'border-red-500/50' : 'border-white/10'
              }`}
            />
            {errors.footer_text && (
              <p className="text-xs text-red-400">{errors.footer_text[0]}</p>
            )}
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={
              saving || 
              !hasChanges() ||
              !settings.school_name ||
              !settings.school_motto ||
              !settings.address ||
              !settings.phone ||
              !settings.email
            }
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold rounded-xl shadow-lg disabled:opacity-50 transition-all flex items-center gap-2"
          >
            {saving ? (
              <>
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Saving...
              </>
            ) : (
              'Save Changes'
            )}
          </button>
        </div>
      </form>
      )}

      {activeTab === 'links' && (
        <div className="space-y-6">
          <div className="flex justify-end">
            <button
               onClick={() => {
                 resetLinkForm();
                 setIsEditingLink(true);
               }}
               className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium rounded-lg transition-colors flex items-center gap-2"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Add New Link
            </button>
          </div>

          {/* Quick Links List */}
          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/10 bg-white/5">
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Title</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">URL</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Order</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-300">Status</th>
                  <th className="px-6 py-4 text-right text-sm font-semibold text-gray-300">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/10">
                {quickLinks.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-8 text-center text-gray-400">
                      No quick links found. Add one to get started.
                    </td>
                  </tr>
                ) : (
                  quickLinks.map((link) => (
                    <tr key={link.id} className="hover:bg-white/5 transition-colors">
                      <td className="px-6 py-4 text-white font-medium">{link.title}</td>
                      <td className="px-6 py-4 text-gray-400 text-sm truncate max-w-xs">{link.url}</td>
                      <td className="px-6 py-4 text-gray-400">{link.order}</td>
                      <td className="px-6 py-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          link.is_active 
                            ? 'bg-green-500/10 text-green-400' 
                            : 'bg-red-500/10 text-red-400'
                        }`}>
                          {link.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right space-x-2">
                        <button
                          onClick={() => {
                            setCurrentLink(link);
                            setIsEditingLink(true);
                          }}
                          className="text-gray-400 hover:text-white transition-colors"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => requestDelete(link.id)}
                          className="text-red-400 hover:text-red-300 transition-colors"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Edit/Create Modal */}
      {isEditingLink && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div className="bg-slate-900 border border-white/10 rounded-2xl w-full max-w-md p-6 shadow-xl">
            <h3 className="text-xl font-bold text-white mb-4">
              {currentLink.id ? 'Edit Quick Link' : 'Add Quick Link'}
            </h3>
            <form onSubmit={handleLinkSubmit} className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Title</label>
                <input
                  type="text"
                  required
                  value={currentLink.title}
                  onChange={(e) => setCurrentLink({ ...currentLink, title: e.target.value })}
                  className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">URL</label>
                <input
                  type="text"
                  required
                  value={currentLink.url}
                  onChange={(e) => setCurrentLink({ ...currentLink, url: e.target.value })}
                  className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                />
              </div>
              <div className="space-y-2">
                 <label className="text-sm font-medium text-gray-300">Order</label>
                 <input
                   type="number"
                   required
                   value={currentLink.order}
                   onChange={(e) => setCurrentLink({ ...currentLink, order: parseInt(e.target.value) })}
                   className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                 />
              </div>
              
              <div className="flex items-center gap-4 pt-2">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={currentLink.is_active}
                    onChange={(e) => setCurrentLink({ ...currentLink, is_active: e.target.checked })}
                    className="w-4 h-4 rounded border-gray-600 bg-gray-700 text-purple-600 focus:ring-purple-500"
                  />
                  <span className="text-sm text-gray-300">Active</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                   <input
                    type="checkbox"
                    checked={currentLink.open_in_new_tab}
                    onChange={(e) => setCurrentLink({ ...currentLink, open_in_new_tab: e.target.checked })}
                    className="w-4 h-4 rounded border-gray-600 bg-gray-700 text-purple-600 focus:ring-purple-500"
                  />
                  <span className="text-sm text-gray-300">Open in new tab</span>
                </label>
              </div>

              <div className="flex justify-end gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => setIsEditingLink(false)}
                  className="px-4 py-2 text-gray-400 hover:text-white transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-xl transition-colors disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Link'}
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
              Are you sure you want to delete this link? This action cannot be undone.
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
