'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import ImageUpload from '@/components/admin/image-upload';

interface GalleryCategory {
  id: number;
  name: string;
  slug: string;
}

interface GalleryImage {
  id: number;
  title: string;
  image: string;
  category: number | null;
  caption: string;
  is_featured: boolean;
}

export default function GalleryPage() {
  const [images, setImages] = useState<GalleryImage[]>([]);
  const [categories, setCategories] = useState<GalleryCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentImage, setCurrentImage] = useState<Partial<GalleryImage>>({});
  const [initialModalData, setInitialModalData] = useState<Partial<GalleryImage> | null>(null);
  const [newImage, setNewImage] = useState<File | null>(null);
  const [saving, setSaving] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [imagesRes, categoriesRes] = await Promise.all([
        api.get('/api/admin/content/gallery/images/'),
        api.get('/api/admin/content/gallery/categories/'),
      ]);
      setImages(imagesRes.data);
      setCategories(categoriesRes.data);
    } catch (error) {
      console.error('Error fetching gallery data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (imageItem: GalleryImage) => {
    setCurrentImage(imageItem);
    setInitialModalData(imageItem);
    setNewImage(null);
    setIsModalOpen(true);
  };

  const requestDelete = (id: number) => {
    setDeleteId(id);
  };

  const confirmDelete = async () => {
    if (!deleteId) return;
    try {
      await api.delete(`/api/admin/content/gallery/images/${deleteId}/`);
      setImages(images.filter(img => img.id !== deleteId));
    } catch (error) {
      console.error('Error deleting image:', error);
    } finally {
      setDeleteId(null);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    
    try {
      const formData = new FormData();
      formData.append('title', currentImage.title || '');
      formData.append('caption', currentImage.caption || '');
      formData.append('category', String(currentImage.category || ''));
      formData.append('is_featured', String(currentImage.is_featured || false));
      
      if (newImage) {
        formData.append('image', newImage);
      }

      if (currentImage.id) {
        await api.put(`/api/admin/content/gallery/images/${currentImage.id}/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
      } else {
        await api.post('/api/admin/content/gallery/images/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
      }
      
      fetchData();
      setIsModalOpen(false);
      setCurrentImage({});
      setNewImage(null);
    } catch (error) {
      console.error('Error saving image:', error);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="text-center p-8 text-gray-400">Loading...</div>;

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Gallery</h1>
          <p className="text-gray-400">Manage photo gallery</p>
        </div>
        <button
          onClick={() => { 
              const newImg = {};
              setCurrentImage(newImg); 
              setInitialModalData(newImg);
              setNewImage(null); 
              setIsModalOpen(true); 
          }}
          className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          Add Image
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {images.map((img) => (
          <div key={img.id} className="bg-slate-800/50 backdrop-blur-xl border border-white/10 rounded-xl overflow-hidden group">
            <div className="relative h-48">
              <img src={img.image} alt={img.title} className="w-full h-full object-fill" />
              <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                <button
                  onClick={() => handleEdit(img)}
                  className="p-2 bg-white/20 hover:bg-white/30 rounded-lg text-white backdrop-blur-sm"
                >
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                </button>
                <button
                  onClick={() => requestDelete(img.id)}
                  className="p-2 bg-red-500/80 hover:bg-red-600/80 rounded-lg text-white backdrop-blur-sm"
                >
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
            <div className="p-4">
              <h3 className="font-semibold text-white truncate">{img.title}</h3>
              <p className="text-xs text-gray-500 mt-1">Category: {categories.find(c => c.id === img.category)?.name || 'Uncategorized'}</p>
              {img.is_featured && (
                <span className="inline-block mt-2 px-2 py-0.5 text-xs bg-purple-500/20 text-purple-400 rounded-full border border-purple-500/20">featured</span>
              )}
            </div>
          </div>
        ))}
      </div>
      
      {images.length === 0 && (
          <div className="text-center py-12 text-gray-500 bg-slate-800/20 rounded-xl border border-white/5">
            No images found. Upload one to get started.
          </div>
      )}

      {/* Modal */}
      {isModalOpen && (
        <div 
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => setIsModalOpen(false)}
        >
          <div 
            className="bg-slate-900 border border-white/10 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6 border-b border-white/10 flex items-center justify-between">
              <h2 className="text-xl font-bold text-white">
                {currentImage.id ? 'Edit Image' : 'Add Image'}
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
                  value={currentImage.title || ''}
                  onChange={e => setCurrentImage(prev => ({ ...prev, title: e.target.value }))}
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Category *</label>
                <select
                  required
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  value={currentImage.category || ''}
                  onChange={e => setCurrentImage(prev => ({ ...prev, category: Number(e.target.value) }))}
                >
                  <option value="">Select Category</option>
                  {categories.map(cat => (
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                  ))}
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Caption</label>
                <input
                  type="text"
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  value={currentImage.caption || ''}
                  onChange={e => setCurrentImage(prev => ({ ...prev, caption: e.target.value }))}
                />
              </div>

              <div>
                <ImageUpload
                  label="Upload Image *"
                  currentImage={currentImage.image || null}
                  onChange={(file) => setNewImage(file)}
                />
                {!newImage && !currentImage.image && (
                  <p className="text-xs text-red-400 mt-1">An image is required.</p>
                )}
              </div>
              
              <div className="flex items-center gap-2 pt-2">
                <input
                  type="checkbox"
                  id="is_featured"
                  className="w-5 h-5 rounded border-gray-600 bg-gray-700 text-purple-600 focus:ring-purple-500"
                  checked={currentImage.is_featured || false}
                  onChange={e => setCurrentImage(prev => ({ ...prev, is_featured: e.target.checked }))}
                />
                <label htmlFor="is_featured" className="text-sm font-medium text-gray-300">Featured (Show on Home)</label>
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
                    (JSON.stringify(currentImage) === JSON.stringify(initialModalData) && !newImage) ||
                    !currentImage.title ||
                    (!newImage && !currentImage.image)
                  }
                  className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {saving ? 'Saving...' : 'Save Image'}
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
              Are you sure you want to delete this image? This action cannot be undone.
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
