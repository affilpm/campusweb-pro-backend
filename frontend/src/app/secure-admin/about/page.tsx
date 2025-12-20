'use client';

import { useEffect, useState, FormEvent } from 'react';
import api from '@/lib/api';
import ImageUpload from '@/components/admin/image-upload';

interface AboutSection {
  title: string;
  content: string;
  image: string | null;
  established_year: number;
  students_count: string;
  teachers_count: string;
}

interface VisionMission {
  vision_title: string;
  vision_content: string;
  mission_title: string;
  mission_content: string;
  values_title: string;
  values_content: string;
}

interface AboutPage {
  hero_title: string;
  hero_subtitle: string;
  history_title: string;
  history_content: string;
  history_image: string | null;
  infrastructure_title: string;
  infrastructure_content: string;
}

interface TimelineEvent {
  id?: number;
  year: string;
  title: string;
  description: string;
}

interface ManagementMember {
  id?: number;
  name: string;
  position: string;
  photo: string | null;
  bio: string;
  order: number;
  is_active: boolean;
}

type TabType = 'about' | 'hero' | 'vision' | 'timeline' | 'management';

export default function AboutSectionPage() {
  const [activeTab, setActiveTab] = useState<TabType>('about');
  
  // About Section data
  const [aboutData, setAboutData] = useState<AboutSection>({
    title: '',
    content: '',
    image: null,
    established_year: 1990,
    students_count: '',
    teachers_count: '',
  });
  const [initialAboutData, setInitialAboutData] = useState<AboutSection | null>(null);
  const [newAboutImage, setNewAboutImage] = useState<File | null>(null);

  // About Page data (hero, history, infrastructure)
  const [pageData, setPageData] = useState<AboutPage>({
    hero_title: '',
    hero_subtitle: '',
    history_title: '',
    history_content: '',
    history_image: null,
    infrastructure_title: '',
    infrastructure_content: '',
  });
  const [initialPageData, setInitialPageData] = useState<AboutPage | null>(null);
  const [newHistoryImage, setNewHistoryImage] = useState<File | null>(null);

  // Vision & Mission data
  const [visionData, setVisionData] = useState<VisionMission>({
    vision_title: '',
    vision_content: '',
    mission_title: '',
    mission_content: '',
    values_title: '',
    values_content: '',
  });
  const [initialVisionData, setInitialVisionData] = useState<VisionMission | null>(null);

  // Timeline data
  const [timeline, setTimeline] = useState<TimelineEvent[]>([]);
  const [editingTimeline, setEditingTimeline] = useState<TimelineEvent | null>(null);

  // Management data
  const [management, setManagement] = useState<ManagementMember[]>([]);
  const [editingMember, setEditingMember] = useState<ManagementMember | null>(null);
  const [newMemberPhoto, setNewMemberPhoto] = useState<File | null>(null);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [errors, setErrors] = useState<Record<string, string[]>>({});
  const [deleteParams, setDeleteParams] = useState<{ type: 'timeline' | 'management'; id: number } | null>(null);

  useEffect(() => {
    fetchAllData();
  }, []);

  // Clear errors when changing tabs
  useEffect(() => {
    setErrors({});
    setMessage(null);
  }, [activeTab]);

  // Auto-dismiss message after 3 seconds
  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => {
        setMessage(null);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [message]);

  const fetchAllData = async () => {
    try {
      const [aboutRes, pageRes, visionRes, timelineRes, managementRes] = await Promise.all([
        api.get('/api/admin/content/home-about/'),
        api.get('/api/admin/content/about/page/').catch(() => ({ data: null })),
        api.get('/api/admin/content/vision-mission/').catch(() => ({ data: null })),
        api.get('/api/admin/content/about/timeline/').catch(() => ({ data: [] })),
        api.get('/api/admin/content/about/management/').catch(() => ({ data: [] })),
      ]);
      
      setAboutData(aboutRes.data);
      setInitialAboutData(aboutRes.data);
      
      if (pageRes.data) {
        setPageData(pageRes.data);
        setInitialPageData(pageRes.data);
      }
      if (visionRes.data) {
        setVisionData(visionRes.data);
        setInitialVisionData(visionRes.data);
      }
      if (timelineRes.data) setTimeline(Array.isArray(timelineRes.data) ? timelineRes.data : []);
      if (managementRes.data) setManagement(Array.isArray(managementRes.data) ? managementRes.data : []);
    } catch (error) {
      console.error('Error fetching data:', error);
      setMessage({ type: 'error', text: 'Failed to load data' });
    } finally {
      setLoading(false);
    }
  };

  // About Section handlers
  const handleAboutChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setAboutData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: [] }));
    }
  };

  const handleAboutSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);
    setErrors({});

    try {
      const formData = new FormData();
      formData.append('title', aboutData.title);
      formData.append('content', aboutData.content);
      formData.append('established_year', String(aboutData.established_year));
      formData.append('students_count', aboutData.students_count);
      formData.append('teachers_count', aboutData.teachers_count);
      
      if (newAboutImage) {
        formData.append('image', newAboutImage);
      }

      const response = await api.put('/api/admin/content/home-about/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      setAboutData(response.data);
      setInitialAboutData(response.data);
      setNewAboutImage(null);
      setMessage({ type: 'success', text: 'About section updated successfully' });
    } catch (error: any) {
      console.error('Error updating about section:', error);
      if (error.response && error.response.status === 400) {
        setErrors(error.response.data);
        setMessage({ type: 'error', text: 'Please check the form for errors.' });
      } else {
        setMessage({ type: 'error', text: 'Failed to update about section' });
      }
    } finally {
      setSaving(false);
    }
  };

  // Page Data handlers (hero, history)
  const handlePageChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setPageData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: [] }));
    }
  };

  const handlePageSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);
    setErrors({});

    try {
      const formData = new FormData();
      formData.append('hero_title', pageData.hero_title);
      formData.append('hero_subtitle', pageData.hero_subtitle);
      formData.append('history_title', pageData.history_title);
      formData.append('history_content', pageData.history_content);
      formData.append('infrastructure_title', pageData.infrastructure_title);
      formData.append('infrastructure_content', pageData.infrastructure_content);
      
      if (newHistoryImage) {
        formData.append('history_image', newHistoryImage);
      }

      const response = await api.put('/api/admin/content/about/page/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      setPageData(response.data);
      setInitialPageData(response.data);
      setNewHistoryImage(null);
      setMessage({ type: 'success', text: 'Page content updated successfully' });
    } catch (error: any) {
      console.error('Error updating page content:', error);
      if (error.response && error.response.status === 400) {
        setErrors(error.response.data);
        setMessage({ type: 'error', text: 'Please check the form for errors.' });
      } else {
        setMessage({ type: 'error', text: 'Failed to update page content' });
      }
    } finally {
      setSaving(false);
    }
  };

  // Vision & Mission handlers
  const handleVisionChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setVisionData((prev) => ({ ...prev, [name]: value }));
  };

  const handleVisionSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);

    try {
      const response = await api.put('/api/admin/content/vision-mission/', visionData);
      setVisionData(response.data);
      setInitialVisionData(response.data);
      setMessage({ type: 'success', text: 'Vision & Mission updated successfully' });
    } catch (error) {
      console.error('Error updating vision & mission:', error);
      setMessage({ type: 'error', text: 'Failed to update vision & mission' });
    } finally {
      setSaving(false);
    }
  };

  // Timeline handlers
  const handleTimelineSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!editingTimeline) return;
    
    setSaving(true);
    setMessage(null);

    try {
      const payload = {
        year: editingTimeline.year,
        title: editingTimeline.title,
        description: editingTimeline.description,
      };

      if (editingTimeline.id) {
        const response = await api.put(`/api/admin/content/about/timeline/${editingTimeline.id}/`, payload);
        setTimeline(prev => prev.map(t => t.id === editingTimeline.id ? response.data : t));
      } else {
        const response = await api.post('/api/admin/content/about/timeline/', payload);
        setTimeline(prev => [...prev, response.data]);
      }
      setEditingTimeline(null);
      setMessage({ type: 'success', text: 'Timeline event saved successfully' });
    } catch (error) {
      console.error('Error saving timeline event:', error);
      setMessage({ type: 'error', text: 'Failed to save timeline event' });
    } finally {
      setSaving(false);
    }
  };

  const requestDeleteTimeline = (id: number) => {
    setDeleteParams({ type: 'timeline', id });
  };

  // Management handlers
  const handleManagementSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!editingMember) return;
    
    setSaving(true);
    setMessage(null);

    try {
      const formData = new FormData();
      formData.append('name', editingMember.name);
      formData.append('position', editingMember.position);
      formData.append('bio', editingMember.bio);
      formData.append('order', String(editingMember.order));
      formData.append('is_active', String(editingMember.is_active));
      
      if (newMemberPhoto) {
        formData.append('photo', newMemberPhoto);
      }

      if (editingMember.id) {
        const response = await api.put(`/api/admin/content/about/management/${editingMember.id}/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        setManagement(prev => prev.map(m => m.id === editingMember.id ? response.data : m));
      } else {
        const response = await api.post('/api/admin/content/about/management/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        setManagement(prev => [...prev, response.data]);
      }
      setEditingMember(null);
      setNewMemberPhoto(null);
      setMessage({ type: 'success', text: 'Team member saved successfully' });
    } catch (error) {
      console.error('Error saving team member:', error);
      setMessage({ type: 'error', text: 'Failed to save team member' });
    } finally {
      setSaving(false);
    }
  };

  const requestDeleteManagement = (id: number) => {
    setDeleteParams({ type: 'management', id });
  };

  const confirmDelete = async () => {
    if (!deleteParams) return;
    setSaving(true);
    
    try {
      if (deleteParams.type === 'timeline') {
        await api.delete(`/api/admin/content/about/timeline/${deleteParams.id}/`);
        setTimeline(prev => prev.filter(t => t.id !== deleteParams.id));
        setMessage({ type: 'success', text: 'Timeline event deleted' });
      } else {
        await api.delete(`/api/admin/content/about/management/${deleteParams.id}/`);
        setManagement(prev => prev.filter(m => m.id !== deleteParams.id));
        setMessage({ type: 'success', text: 'Team member deleted' });
      }
    } catch (error) {
       console.error(`Error deleting ${deleteParams.type}:`, error);
       setMessage({ type: 'error', text: `Failed to delete ${deleteParams.type === 'timeline' ? 'event' : 'member'}` });
    } finally {
      setSaving(false);
      setDeleteParams(null);
    }
  };

  if (loading) return <div className="text-center p-8 text-gray-400">Loading...</div>;

  const tabs = [
    { id: 'about' as TabType, label: 'About Overview', icon: '📋' },
    { id: 'hero' as TabType, label: 'Hero & History', icon: '🏠' },
    { id: 'vision' as TabType, label: 'Vision & Mission', icon: '🎯' },
    { id: 'timeline' as TabType, label: 'Timeline', icon: '📅' },
    { id: 'management' as TabType, label: 'Management Team', icon: '👥' },
  ];

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">About Us Page</h1>
          <p className="text-gray-400">Manage all content for the About Us page</p>
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
      <div className="flex flex-wrap gap-2 mb-8 bg-slate-800/30 backdrop-blur-xl rounded-xl p-2 border border-white/5">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-lg font-medium transition-all ${
              activeTab === tab.id
                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg'
                : 'text-gray-400 hover:text-white hover:bg-white/5'
            }`}
          >
            <span>{tab.icon}</span>
            <span className="hidden sm:inline">{tab.label}</span>
          </button>
        ))}
      </div>

      {/* About Overview Tab */}
      {activeTab === 'about' && (
        <form onSubmit={handleAboutSubmit} className="space-y-6">
          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
            <h2 className="text-lg font-semibold text-white mb-4">About Section Overview</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Section Title *</label>
                  <input
                    type="text"
                    name="title"
                    value={aboutData.title}
                    onChange={handleAboutChange}
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
                  <label className="text-sm font-medium text-gray-300">Content *</label>
                  <textarea
                    name="content"
                    value={aboutData.content}
                    onChange={handleAboutChange}
                    rows={6}
                    required
                    className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                      errors.content ? 'border-red-500/50' : 'border-white/10'
                    }`}
                    placeholder="Write a brief overview of the school..."
                  />
                  {errors.content && (
                    <p className="text-xs text-red-400">{errors.content[0]}</p>
                  )}
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Established Year *</label>
                    <input
                      type="number"
                      name="established_year"
                      value={aboutData.established_year}
                      onChange={handleAboutChange}
                      required
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Students Count *</label>
                    <input
                      type="text"
                      name="students_count"
                      value={aboutData.students_count}
                      onChange={handleAboutChange}
                      required
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Teachers Count *</label>
                    <input
                      type="text"
                      name="teachers_count"
                      value={aboutData.teachers_count}
                      onChange={handleAboutChange}
                      required
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    />
                  </div>
                </div>
              </div>

              <div>
                <ImageUpload
                  label="About Image"
                  currentImage={aboutData.image}
                  onChange={(file) => setNewAboutImage(file)}
                  onRemove={() => setNewAboutImage(null)}
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold rounded-xl shadow-lg disabled:opacity-50 transition-all"
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      )}

      {/* Hero & History Tab */}
      {activeTab === 'hero' && (
        <form onSubmit={handlePageSubmit} className="space-y-6">
          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Hero Section</h2>
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Hero Title *</label>
                <input
                  type="text"
                  name="hero_title"
                  value={pageData.hero_title}
                  onChange={handlePageChange}
                  required
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  placeholder="About Our School"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Hero Subtitle</label>
                <textarea
                  name="hero_subtitle"
                  value={pageData.hero_subtitle}
                  onChange={handlePageChange}
                  rows={3}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  placeholder="A brief tagline for the About page..."
                />
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
            <h2 className="text-lg font-semibold text-white mb-4">History Section</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">History Title *</label>
                  <input
                    type="text"
                    name="history_title"
                    value={pageData.history_title}
                    onChange={handlePageChange}
                    required
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    placeholder="Our History"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">History Content *</label>
                  <textarea
                    name="history_content"
                    value={pageData.history_content}
                    onChange={handlePageChange}
                    rows={8}
                    required
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    placeholder="Write the school's history here..."
                  />
                </div>
              </div>
              <div>
                <ImageUpload
                  label="History Image"
                  currentImage={pageData.history_image}
                  onChange={(file) => setNewHistoryImage(file)}
                  onRemove={() => setNewHistoryImage(null)}
                />
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Infrastructure Section</h2>
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Section Title</label>
                <input
                  type="text"
                  name="infrastructure_title"
                  value={pageData.infrastructure_title}
                  onChange={handlePageChange}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  placeholder="Our Infrastructure"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Description</label>
                <textarea
                  name="infrastructure_content"
                  value={pageData.infrastructure_content}
                  onChange={handlePageChange}
                  rows={5}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  placeholder="Describe your school's infrastructure and facilities..."
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold rounded-xl shadow-lg disabled:opacity-50 transition-all"
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      )}

      {/* Vision & Mission Tab */}
      {activeTab === 'vision' && (
        <form onSubmit={handleVisionSubmit} className="space-y-6">
          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Vision</h2>
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Vision Title</label>
                <input
                  type="text"
                  name="vision_title"
                  value={visionData.vision_title}
                  onChange={handleVisionChange}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  placeholder="Our Vision"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Vision Content</label>
                <textarea
                  name="vision_content"
                  value={visionData.vision_content}
                  onChange={handleVisionChange}
                  rows={4}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  placeholder="Describe your school's vision..."
                />
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Mission</h2>
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Mission Title</label>
                <input
                  type="text"
                  name="mission_title"
                  value={visionData.mission_title}
                  onChange={handleVisionChange}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  placeholder="Our Mission"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Mission Content</label>
                <textarea
                  name="mission_content"
                  value={visionData.mission_content}
                  onChange={handleVisionChange}
                  rows={4}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  placeholder="Describe your school's mission..."
                />
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Core Values</h2>
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Values Title</label>
                <input
                  type="text"
                  name="values_title"
                  value={visionData.values_title}
                  onChange={handleVisionChange}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  placeholder="Our Core Values"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Values Content</label>
                <textarea
                  name="values_content"
                  value={visionData.values_content}
                  onChange={handleVisionChange}
                  rows={4}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  placeholder="List your school's core values..."
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-semibold rounded-xl shadow-lg disabled:opacity-50 transition-all"
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      )}

      {/* Timeline Tab */}
      {activeTab === 'timeline' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold text-white">School Timeline</h2>
            <button
              onClick={() => setEditingTimeline({ year: String(new Date().getFullYear()), title: '', description: '' })}
              className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-xl transition-colors"
            >
              + Add Event
            </button>
          </div>

          {editingTimeline && (
            <form onSubmit={handleTimelineSubmit} className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
              <h3 className="text-md font-semibold text-white mb-4">
                {editingTimeline.id ? 'Edit Event' : 'Add New Event'}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Year *</label>
                  <input
                    type="text"
                    value={editingTimeline.year}
                    onChange={(e) => setEditingTimeline({ ...editingTimeline, year: e.target.value })}
                    required
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    placeholder="e.g., 2010"
                  />
                </div>
                <div className="md:col-span-3 space-y-2">
                  <label className="text-sm font-medium text-gray-300">Title *</label>
                  <input
                    type="text"
                    value={editingTimeline.title}
                    onChange={(e) => setEditingTimeline({ ...editingTimeline, title: e.target.value })}
                    required
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    placeholder="Event title"
                  />
                </div>
              </div>
              <div className="space-y-2 mb-4">
                <label className="text-sm font-medium text-gray-300">Description *</label>
                <textarea
                  value={editingTimeline.description}
                  onChange={(e) => setEditingTimeline({ ...editingTimeline, description: e.target.value })}
                  rows={3}
                  required
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  placeholder="Event description"
                />
              </div>
              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={saving}
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-xl transition-colors disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Event'}
                </button>
                <button
                  type="button"
                  onClick={() => setEditingTimeline(null)}
                  className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-xl transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}

          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 overflow-hidden">
            {timeline.length === 0 ? (
              <div className="p-8 text-center text-gray-400">
                No timeline events yet. Add your first milestone!
              </div>
            ) : (
              <div className="divide-y divide-white/5">
                {timeline.sort((a, b) => b.year.localeCompare(a.year)).map((event) => (
                  <div key={event.id} className="p-4 flex items-center justify-between hover:bg-white/5">
                    <div className="flex items-center gap-4">
                      <div className="text-2xl font-bold text-purple-400">{event.year}</div>
                      <div>
                        <div className="text-white font-medium">{event.title}</div>
                        <div className="text-gray-400 text-sm line-clamp-1">{event.description}</div>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => setEditingTimeline(event)}
                        className="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                      >
                        ✏️
                      </button>
                      <button
                        onClick={() => event.id && requestDeleteTimeline(event.id)}
                        className="p-2 text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Management Team Tab */}
      {activeTab === 'management' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold text-white">Leadership Team</h2>
            <button
              onClick={() => setEditingMember({ name: '', position: '', photo: null, bio: '', order: management.length, is_active: true })}
              className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-xl transition-colors"
            >
              + Add Member
            </button>
          </div>

          {editingMember && (
            <form onSubmit={handleManagementSubmit} className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
              <h3 className="text-md font-semibold text-white mb-4">
                {editingMember.id ? 'Edit Member' : 'Add New Member'}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Name *</label>
                    <input
                      type="text"
                      value={editingMember.name}
                      onChange={(e) => setEditingMember({ ...editingMember, name: e.target.value })}
                      required
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                      placeholder="Full name"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Position *</label>
                    <input
                      type="text"
                      value={editingMember.position}
                      onChange={(e) => setEditingMember({ ...editingMember, position: e.target.value })}
                      required
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                      placeholder="e.g., Chairman, Principal"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Biography</label>
                    <textarea
                      value={editingMember.bio}
                      onChange={(e) => setEditingMember({ ...editingMember, bio: e.target.value })}
                      rows={4}
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                      placeholder="Short biography..."
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-gray-300">Display Order</label>
                      <input
                        type="number"
                        value={editingMember.order}
                        onChange={(e) => setEditingMember({ ...editingMember, order: parseInt(e.target.value) || 0 })}
                        className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-gray-300">Status</label>
                      <select
                        value={editingMember.is_active ? 'active' : 'inactive'}
                        onChange={(e) => setEditingMember({ ...editingMember, is_active: e.target.value === 'active' })}
                        className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                      >
                        <option value="active">Active</option>
                        <option value="inactive">Inactive</option>
                      </select>
                    </div>
                  </div>
                </div>
                <div>
                  <ImageUpload
                    label="Photo"
                    currentImage={editingMember.photo}
                    onChange={(file) => setNewMemberPhoto(file)}
                    onRemove={() => setNewMemberPhoto(null)}
                  />
                </div>
              </div>
              <div className="flex gap-3 mt-6">
                <button
                  type="submit"
                  disabled={saving}
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-xl transition-colors disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Member'}
                </button>
                <button
                  type="button"
                  onClick={() => { setEditingMember(null); setNewMemberPhoto(null); }}
                  className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-xl transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {management.length === 0 ? (
              <div className="col-span-full text-center text-gray-400 py-8 bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10">
                No team members yet. Add your leadership team!
              </div>
            ) : (
              management.sort((a, b) => a.order - b.order).map((member) => (
                <div key={member.id} className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-4 hover:border-purple-500/30 transition-colors">
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 rounded-full overflow-hidden bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center flex-shrink-0">
                      {member.photo ? (
                        <img src={member.photo} alt={member.name} className="w-full h-full object-cover" />
                      ) : (
                        <span className="text-2xl font-bold text-white/80">{member.name.charAt(0)}</span>
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-white font-medium truncate">{member.name}</div>
                      <div className="text-purple-400 text-sm truncate">{member.position}</div>
                      <div className={`text-xs mt-1 ${member.is_active ? 'text-green-400' : 'text-gray-500'}`}>
                        {member.is_active ? '● Active' : '○ Inactive'}
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-2 mt-4 pt-4 border-t border-white/5">
                    <button
                      onClick={() => setEditingMember(member)}
                      className="flex-1 py-2 text-sm text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => member.id && requestDeleteManagement(member.id)}
                      className="flex-1 py-2 text-sm text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
      {deleteParams && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-slate-900 border border-white/10 rounded-2xl p-6 max-w-md w-full shadow-2xl transform scale-100 transition-all">
            <h3 className="text-xl font-bold text-white mb-2">Confirm Delete</h3>
            <p className="text-gray-400 mb-6">
              Are you sure you want to delete this {deleteParams.type === 'timeline' ? 'timeline event' : 'team member'}? This action cannot be undone.
            </p>
            <div className="flex gap-4 justify-end">
              <button
                onClick={() => setDeleteParams(null)}
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
