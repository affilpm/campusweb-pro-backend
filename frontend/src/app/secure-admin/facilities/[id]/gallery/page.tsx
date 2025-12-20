'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import api from '@/lib/api';
import Link from 'next/link';

interface FacilityImage {
  id: number;
  image: string;
  caption: string;
  order: number;
  is_active: boolean;
}

interface Facility {
  id: number;
  name: string;
  icon: string;
}

export default function FacilityGalleryPage() {
  const params = useParams();
  const router = useRouter();
  const facilityId = params.id as string;

  const [facility, setFacility] = useState<Facility | null>(null);
  const [images, setImages] = useState<FacilityImage[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    fetchData();
  }, [facilityId]);

  const fetchData = async () => {
    try {
      const [facilityRes, imagesRes] = await Promise.all([
        api.get(`/api/admin/content/facilities/${facilityId}/`),
        api.get(`/api/admin/content/facilities/${facilityId}/images/`)
      ]);
      setFacility(facilityRes.data);
      setImages(imagesRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      setMessage({ type: 'error', text: 'Failed to load gallery' });
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (files: FileList) => {
    setUploading(true);
    try {
      for (let i = 0; i < files.length; i++) {
        const formData = new FormData();
        formData.append('image', files[i]);
        formData.append('order', String(images.length + i));
        formData.append('is_active', 'true');
        
        await api.post(`/api/admin/content/facilities/${facilityId}/images/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }
      await fetchData();
      setMessage({ type: 'success', text: `${files.length} image(s) uploaded successfully` });
    } catch (error) {
      console.error('Error uploading images:', error);
      setMessage({ type: 'error', text: 'Failed to upload images' });
    } finally {
      setUploading(false);
    }
  };

  const requestDelete = (imageId: number) => {
    setDeleteId(imageId);
  };

  const confirmDelete = async () => {
    if (!deleteId) return;
    try {
      await api.delete(`/api/admin/content/facility-images/${deleteId}/`);
      setImages(images.filter(img => img.id !== deleteId));
      setMessage({ type: 'success', text: 'Image deleted' });
    } catch (error) {
      console.error('Error deleting image:', error);
      setMessage({ type: 'error', text: 'Failed to delete image' });
    } finally {
      setDeleteId(null);
    }
  };

  const toggleActive = async (image: FacilityImage) => {
    try {
      await api.patch(`/api/admin/content/facility-images/${image.id}/`, {
        is_active: !image.is_active
      });
      setImages(images.map(img => 
        img.id === image.id ? { ...img, is_active: !img.is_active } : img
      ));
    } catch (error) {
      console.error('Error toggling image:', error);
    }
  };

  const updateCaption = async (image: FacilityImage, caption: string) => {
    try {
      await api.patch(`/api/admin/content/facility-images/${image.id}/`, { caption });
      setImages(images.map(img => 
        img.id === image.id ? { ...img, caption } : img
      ));
    } catch (error) {
      console.error('Error updating caption:', error);
    }
  };

  if (loading) return <div className="text-center p-8 text-gray-400">Loading...</div>;

  if (!facility) {
    return (
      <div className="text-center py-16">
        <span className="text-6xl mb-4 block">🚫</span>
        <h3 className="text-xl font-bold text-white mb-2">Facility Not Found</h3>
        <Link href="/secure-admin/facilities" className="text-purple-400 hover:underline">
          ← Back to Facilities
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <Link 
          href="/secure-admin/facilities" 
          className="inline-flex items-center gap-2 text-gray-400 hover:text-white mb-4 transition-colors"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Facilities
        </Link>
        <div className="flex items-center gap-4">
          <span className="text-4xl">{facility.icon}</span>
          <div>
            <h1 className="text-2xl font-bold text-white">{facility.name} Gallery</h1>
            <p className="text-gray-400">Manage photos for this facility</p>
          </div>
        </div>
      </div>

      {message && (
        <div className={`mb-6 p-4 rounded-xl border ${
          message.type === 'success' ? 'bg-green-500/10 border-green-500/30 text-green-400' : 'bg-red-500/10 border-red-500/30 text-red-400'
        }`}>
          {message.text}
        </div>
      )}

      {/* Upload Area */}
      <div className="mb-8">
        <label className="block">
          <div className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all ${
            uploading ? 'border-purple-500 bg-purple-500/10' : 'border-white/20 hover:border-purple-500/50 hover:bg-white/5'
          }`}>
            {uploading ? (
              <div>
                <div className="inline-block animate-spin rounded-full h-10 w-10 border-4 border-purple-500 border-t-transparent mb-4"></div>
                <p className="text-white">Uploading images...</p>
              </div>
            ) : (
              <>
                <svg className="w-12 h-12 mx-auto mb-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p className="text-white font-semibold mb-2">Click to upload images</p>
                <p className="text-gray-500 text-sm">or drag and drop multiple files</p>
              </>
            )}
          </div>
          <input 
            type="file" 
            multiple 
            accept="image/*"
            className="hidden"
            onChange={(e) => e.target.files && handleUpload(e.target.files)}
            disabled={uploading}
          />
        </label>
      </div>

      {/* Images Grid */}
      {images.length === 0 ? (
        <div className="text-center py-16 bg-slate-800/50 rounded-2xl border border-white/10">
          <span className="text-6xl mb-4 block">📷</span>
          <h3 className="text-xl font-bold text-white mb-2">No Images Yet</h3>
          <p className="text-gray-400">Upload images to create a gallery for this facility</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {images.sort((a, b) => a.order - b.order).map((image) => (
            <div 
              key={image.id} 
              className={`relative group rounded-xl overflow-hidden bg-slate-800/50 border transition-all ${
                image.is_active ? 'border-white/10' : 'border-red-500/30 opacity-60'
              }`}
            >
              {/* Image */}
              <div className="aspect-square">
                <img 
                  src={image.image} 
                  alt={image.caption || 'Gallery image'}
                  className="w-full h-full object-fill"
                />
              </div>

              {/* Overlay Actions */}
              <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-between p-3">
                {/* Top Actions */}
                <div className="flex justify-end gap-2">
                  <button
                    onClick={() => toggleActive(image)}
                    className={`w-8 h-8 rounded-lg flex items-center justify-center transition-colors ${
                      image.is_active ? 'bg-green-500/30 text-green-400' : 'bg-gray-500/30 text-gray-400'
                    }`}
                    title={image.is_active ? 'Hide image' : 'Show image'}
                  >
                    {image.is_active ? '👁️' : '🚫'}
                  </button>
                  <button
                    onClick={() => requestDelete(image.id)}
                    className="w-8 h-8 bg-red-500/30 text-red-400 rounded-lg flex items-center justify-center hover:bg-red-500/50 transition-colors"
                    title="Delete image"
                  >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>

                {/* Bottom Caption */}
                <input
                  type="text"
                  placeholder="Add caption..."
                  value={image.caption}
                  onChange={(e) => updateCaption(image, e.target.value)}
                  className="w-full px-3 py-2 bg-black/50 border border-white/20 rounded-lg text-white text-sm placeholder-gray-500 focus:outline-none focus:border-purple-500"
                />
              </div>

              {/* Status indicator */}
              {!image.is_active && (
                <div className="absolute top-2 left-2 px-2 py-1 bg-red-500/80 text-white text-xs rounded-md font-bold">
                  Hidden
                </div>
              )}
            </div>
          ))}
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
