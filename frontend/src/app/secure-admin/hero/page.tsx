'use client';

import { useEffect, useState, FormEvent } from 'react';
import api from '@/lib/api';
import ImageUpload from '@/components/admin/image-upload';

interface HeroSection {
  title: string;
  subtitle: string;
  image: string | null;
}

export default function HeroSectionPage() {
  const [data, setData] = useState<HeroSection>({
    title: '',
    subtitle: '',
    image: null,
  });
  const [initialData, setInitialData] = useState<HeroSection | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [newImage, setNewImage] = useState<File | null>(null);
  const [errors, setErrors] = useState<Record<string, string[]>>({});

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await api.get('/api/admin/content/hero/');
      setData(response.data);
      setInitialData(response.data);
    } catch (error) {
      console.error('Error fetching hero data:', error);
      setMessage({ type: 'error', text: 'Failed to load data' });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setData((prev) => ({ ...prev, [name]: value }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: [] }));
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);
    setErrors({});

    try {
      const formData = new FormData();
      formData.append('title', data.title);
      formData.append('subtitle', data.subtitle);
      
      if (newImage) {
        formData.append('image', newImage);
      }

      const response = await api.put('/api/admin/content/hero/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setData(response.data);
      setNewImage(null);
      setMessage({ type: 'success', text: 'Hero section updated successfully' });
    } catch (error: any) {
      console.error('Error updating hero section:', error);
      if (error.response && error.response.status === 400) {
        setErrors(error.response.data);
        setMessage({ type: 'error', text: 'Please check the form for errors.' });
      } else {
        setMessage({ type: 'error', text: 'Failed to update hero section' });
      }
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="text-center p-8 text-gray-400">Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Hero Section</h1>
          <p className="text-gray-400">Manage the main homepage banner</p>
        </div>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-xl border ${
          message.type === 'success' ? 'bg-green-500/10 border-green-500/30 text-green-400' : 'bg-red-500/10 border-red-500/30 text-red-400'
        }`}>
          {message.text}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Main Title *</label>
                <input
                  type="text"
                  name="title"
                  value={data.title}
                  onChange={handleChange}
                  required
                  className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                    errors.title ? 'border-red-500/50' : 'border-white/10'
                  }`}
                />
                {errors.title && (
                  <p className="text-xs text-red-400">{errors.title[0]}</p>
                )}
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Subtitle *</label>
                <textarea
                  name="subtitle"
                  value={data.subtitle}
                  onChange={handleChange}
                  rows={4}
                  required
                  className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                    errors.subtitle ? 'border-red-500/50' : 'border-white/10'
                  }`}
                />
                {errors.subtitle && (
                  <p className="text-xs text-red-400">{errors.subtitle[0]}</p>
                )}
              </div>
            </div>

            <div>
              <ImageUpload
                label="Background Image"
                currentImage={data.image}
                onChange={(file) => setNewImage(file)}
              />
              {errors.image && (
                <p className="text-xs text-red-400 mt-2">{errors.image[0]}</p>
              )}
            </div>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={
              saving || 
              !initialData || 
              (JSON.stringify(data) === JSON.stringify(initialData) && !newImage) ||
              !data.title ||
              !data.subtitle
            }
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold rounded-xl shadow-lg disabled:opacity-50 transition-all"
          >
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </form>
    </div>
  );
}
