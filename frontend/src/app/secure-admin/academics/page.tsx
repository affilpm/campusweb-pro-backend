'use client';

import { useEffect, useState, FormEvent } from 'react';
import api from '@/lib/api';
import ImageUpload from '@/components/admin/image-upload';

interface AcademicsPage {
  hero_title: string;
  hero_subtitle: string;
  curriculum_title: string;
  curriculum_content: string;
  curriculum_image: string | null;
  methodology_title: string;
  methodology_content: string;
  calendar_title: string;
  calendar_file: string | null;
}

interface ClassCategory {
  id?: number;
  name: string;
  description: string;
  classes_range: string;
  image: string | null;
  order: number;
  is_active: boolean;
}

interface Subject {
  id?: number;
  name: string;
  description: string;
  icon: string;
  categories: number[]; // Array of category IDs (ManyToMany)
  is_active: boolean;
}

type TabType = 'page' | 'categories' | 'subjects';

export default function AcademicsAdminPage() {
  const [activeTab, setActiveTab] = useState<TabType>('page');
  
  // Page data
  const [pageData, setPageData] = useState<AcademicsPage>({
    hero_title: '',
    hero_subtitle: '',
    curriculum_title: '',
    curriculum_content: '',
    curriculum_image: null,
    methodology_title: '',
    methodology_content: '',
    calendar_title: '',
    calendar_file: null,
  });
  const [initialPageData, setInitialPageData] = useState<AcademicsPage | null>(null);
  const [newCurriculumImage, setNewCurriculumImage] = useState<File | null>(null);
  const [newCalendarFile, setNewCalendarFile] = useState<File | null>(null);

  // Class categories
  const [categories, setCategories] = useState<ClassCategory[]>([]);
  const [editingCategory, setEditingCategory] = useState<ClassCategory | null>(null);
  const [initialCategoryData, setInitialCategoryData] = useState<ClassCategory | null>(null);
  const [newCategoryImage, setNewCategoryImage] = useState<File | null>(null);

  // Subjects
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [editingSubject, setEditingSubject] = useState<Subject | null>(null);
  const [initialSubjectData, setInitialSubjectData] = useState<Subject | null>(null);
  
  // Delete State
  const [deleteParams, setDeleteParams] = useState<{ type: 'categories' | 'subjects'; id: number } | null>(null);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    fetchAllData();
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

  const fetchAllData = async () => {
    try {
      const [pageRes, categoriesRes, subjectsRes] = await Promise.all([
        api.get('/api/admin/content/academics/page/').catch(() => ({ data: null })),
        api.get('/api/admin/content/academics/categories/').catch(() => ({ data: [] })),
        api.get('/api/admin/content/academics/subjects/').catch(() => ({ data: [] })),
      ]);
      
      if (pageRes.data) {
        setPageData(pageRes.data);
        setInitialPageData(pageRes.data);
      }
      if (categoriesRes.data) setCategories(Array.isArray(categoriesRes.data) ? categoriesRes.data : []);
      if (subjectsRes.data) setSubjects(Array.isArray(subjectsRes.data) ? subjectsRes.data : []);
    } catch (error) {
      console.error('Error fetching data:', error);
      setMessage({ type: 'error', text: 'Failed to load data' });
    } finally {
      setLoading(false);
    }
  };

  // Page handlers
  const handlePageChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setPageData((prev) => ({ ...prev, [name]: value }));
  };

  const handlePageSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);

    try {
      const formData = new FormData();
      Object.entries(pageData).forEach(([key, value]) => {
        if (value !== null && key !== 'curriculum_image' && key !== 'calendar_file') {
          formData.append(key, value);
        }
      });
      
      if (newCurriculumImage) {
        formData.append('curriculum_image', newCurriculumImage);
      }
      if (newCalendarFile) {
        formData.append('calendar_file', newCalendarFile);
      }

      const response = await api.put('/api/admin/content/academics/page/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      setPageData(response.data);
      setNewCurriculumImage(null);
      setNewCalendarFile(null);
      setMessage({ type: 'success', text: 'Academics page updated successfully' });
    } catch (error) {
      console.error('Error updating academics page:', error);
      setMessage({ type: 'error', text: 'Failed to update academics page' });
    } finally {
      setSaving(false);
    }
  };

  // Category handlers
  const handleCategorySubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!editingCategory) return;
    
    setSaving(true);
    setMessage(null);

    try {
      const formData = new FormData();
      formData.append('name', editingCategory.name);
      formData.append('description', editingCategory.description);
      formData.append('classes_range', editingCategory.classes_range);
      formData.append('order', String(editingCategory.order));
      formData.append('is_active', String(editingCategory.is_active));
      
      if (newCategoryImage) {
        formData.append('image', newCategoryImage);
      }

      if (editingCategory.id) {
        const response = await api.put(`/api/admin/content/academics/categories/${editingCategory.id}/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        setCategories(prev => prev.map(c => c.id === editingCategory.id ? response.data : c));
      } else {
        const response = await api.post('/api/admin/content/academics/categories/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        setCategories(prev => [...prev, response.data]);
      }
      setEditingCategory(null);
      setNewCategoryImage(null);
      setMessage({ type: 'success', text: 'Category saved successfully' });
    } catch (error) {
      console.error('Error saving category:', error);
      setMessage({ type: 'error', text: 'Failed to save category' });
    } finally {
      setSaving(false);
    }
  };

  // Delete Handler
  const confirmDelete = async () => {
    if (!deleteParams) return;
    
    setSaving(true);
    try {
      if (deleteParams.type === 'categories') {
        await api.delete(`/api/admin/content/academics/categories/${deleteParams.id}/`);
        setCategories(prev => prev.filter(c => c.id !== deleteParams.id));
        setMessage({ type: 'success', text: 'Category deleted' });
      } else {
        await api.delete(`/api/admin/content/academics/subjects/${deleteParams.id}/`);
        setSubjects(prev => prev.filter(s => s.id !== deleteParams.id));
        setMessage({ type: 'success', text: 'Subject deleted' });
      }
    } catch (error) {
      console.error('Error deleting:', error);
      setMessage({ type: 'error', text: 'Failed to delete' });
    } finally {
      setSaving(false);
      setDeleteParams(null);
    }
  };

  // Subject handlers
  const handleSubjectSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!editingSubject) return;
    
    setSaving(true);
    setMessage(null);

    try {
      const payload = {
        name: editingSubject.name,
        description: editingSubject.description,
        icon: editingSubject.icon,
        categories: editingSubject.categories, // Send array of category IDs
        is_active: editingSubject.is_active,
      };

      if (editingSubject.id) {
        const response = await api.put(`/api/admin/content/academics/subjects/${editingSubject.id}/`, payload);
        setSubjects(prev => prev.map(s => s.id === editingSubject.id ? response.data : s));
      } else {
        const response = await api.post('/api/admin/content/academics/subjects/', payload);
        setSubjects(prev => [...prev, response.data]);
      }
      setEditingSubject(null);
      setMessage({ type: 'success', text: 'Subject saved successfully' });
    } catch (error) {
      console.error('Error saving subject:', error);
      setMessage({ type: 'error', text: 'Failed to save subject' });
    } finally {
      setSaving(false);
    }
  };



  if (loading) return <div className="text-center p-8 text-gray-400">Loading...</div>;

  const tabs = [
    { id: 'page' as TabType, label: 'Page Content', icon: '📄' },
    { id: 'categories' as TabType, label: 'Class Categories', icon: '📚' },
    { id: 'subjects' as TabType, label: 'Subjects', icon: '📝' },
  ];

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Academics Page</h1>
          <p className="text-gray-400">Manage curriculum, programs, and academic content</p>
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
                ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg'
                : 'text-gray-400 hover:text-white hover:bg-white/5'
            }`}
          >
            <span>{tab.icon}</span>
            <span className="hidden sm:inline">{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Page Content Tab */}
      {activeTab === 'page' && (
        <form onSubmit={handlePageSubmit} className="space-y-6">
          {/* Hero Section */}
          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Hero Section</h2>
            <div className="grid grid-cols-1 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Hero Title *</label>
                <input
                  type="text"
                  name="hero_title"
                  required
                  value={pageData.hero_title}
                  onChange={handlePageChange}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                  placeholder="Academics"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Hero Subtitle *</label>
                <textarea
                  name="hero_subtitle"
                  required
                  value={pageData.hero_subtitle}
                  onChange={handlePageChange}
                  rows={2}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                  placeholder="Excellence in Education"
                />
              </div>
            </div>
          </div>

          {/* Curriculum Section */}
          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Curriculum Section</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Curriculum Title *</label>
                  <input
                    type="text"
                    name="curriculum_title"
                    required
                    value={pageData.curriculum_title}
                    onChange={handlePageChange}
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                    placeholder="Our Curriculum"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Curriculum Content *</label>
                  <textarea
                    name="curriculum_content"
                    required
                    value={pageData.curriculum_content}
                    onChange={handlePageChange}
                    rows={6}
                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                    placeholder="Describe your curriculum... Use new lines to separate paragraphs."
                  />
                </div>
              </div>
              <div>
                <ImageUpload
                  label="Curriculum Image"
                  currentImage={pageData.curriculum_image}
                  onChange={(file) => setNewCurriculumImage(file)}
                />
              </div>
            </div>
          </div>

          {/* Methodology Section */}
          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Teaching Methodology</h2>
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Methodology Title *</label>
                <input
                  type="text"
                  name="methodology_title"
                  required
                  value={pageData.methodology_title}
                  onChange={handlePageChange}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                  placeholder="Our Teaching Methodology"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Methodology Content *</label>
                <textarea
                  name="methodology_content"
                  required
                  value={pageData.methodology_content}
                  onChange={handlePageChange}
                  rows={5}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                  placeholder="Describe your teaching methodology..."
                />
              </div>
            </div>
          </div>

          {/* Academic Calendar */}
          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Academic Calendar</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Calendar Section Title *</label>
                <input
                  type="text"
                  name="calendar_title"
                  required
                  value={pageData.calendar_title}
                  onChange={handlePageChange}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                  placeholder="Academic Calendar"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Calendar File (PDF)</label>
                <input
                  type="file"
                  accept=".pdf,.doc,.docx"
                  onChange={(e) => setNewCalendarFile(e.target.files?.[0] || null)}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 file:mr-4 file:py-1 file:px-3 file:rounded-lg file:border-0 file:bg-indigo-600 file:text-white file:cursor-pointer"
                />
                {pageData.calendar_file && (
                  <a href={pageData.calendar_file} target="_blank" rel="noopener noreferrer" className="text-sm text-indigo-400 hover:text-indigo-300">
                    View current file ↗
                  </a>
                )}
              </div>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={
                saving || 
                !initialPageData || 
                (JSON.stringify(pageData) === JSON.stringify(initialPageData) && !newCurriculumImage && !newCalendarFile) ||
                !pageData.hero_title ||
                !pageData.hero_subtitle ||
                !pageData.curriculum_title ||
                !pageData.curriculum_content ||
                !pageData.methodology_title ||
                !pageData.methodology_content ||
                !pageData.calendar_title
              }
              className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-semibold rounded-xl shadow-lg disabled:opacity-50 transition-all"
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      )}

      {/* Class Categories Tab */}
      {activeTab === 'categories' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold text-white">Class Categories</h2>
            <button
              onClick={() => {
                const newCat = { name: '', description: '', classes_range: '', image: null, order: categories.length, is_active: true };
                setEditingCategory(newCat);
                setInitialCategoryData(newCat);
              }}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl transition-colors"
            >
              + Add Category
            </button>
          </div>

          {editingCategory && (
            <form onSubmit={handleCategorySubmit} className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
              <h3 className="text-md font-semibold text-white mb-4">
                {editingCategory.id ? 'Edit Category' : 'Add New Category'}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Category Name *</label>
                    <input
                      type="text"
                      required
                      value={editingCategory.name}
                      onChange={(e) => setEditingCategory({ ...editingCategory, name: e.target.value })}
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                      placeholder="e.g., Primary School"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Classes Range *</label>
                    <input
                      type="text"
                      required
                      value={editingCategory.classes_range}
                      onChange={(e) => setEditingCategory({ ...editingCategory, classes_range: e.target.value })}
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                      placeholder="e.g., Classes I - V"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Description *</label>
                    <textarea
                      required
                      value={editingCategory.description}
                      onChange={(e) => setEditingCategory({ ...editingCategory, description: e.target.value })}
                      rows={3}
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                      placeholder="Describe this category..."
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-gray-300">Order *</label>
                      <input
                        type="number"
                        required
                        value={editingCategory.order}
                        onChange={(e) => setEditingCategory({ ...editingCategory, order: parseInt(e.target.value) })}
                        className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-gray-300">Status</label>
                      <select
                        value={editingCategory.is_active ? 'active' : 'inactive'}
                        onChange={(e) => setEditingCategory({ ...editingCategory, is_active: e.target.value === 'active' })}
                        className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                      >
                        <option value="active">Active</option>
                        <option value="inactive">Inactive</option>
                      </select>
                    </div>
                  </div>
                </div>
                <div>
                  <ImageUpload
                    label="Category Image"
                    currentImage={editingCategory.image}
                    onChange={(file) => setNewCategoryImage(file)}
                  />
                </div>
              </div>
              <div className="flex gap-3 mt-6">
                <button
                  type="submit"
                  disabled={
                    saving || 
                    (JSON.stringify(editingCategory) === JSON.stringify(initialCategoryData) && !newCategoryImage) ||
                    !editingCategory.name ||
                    !editingCategory.classes_range ||
                    !editingCategory.description
                  }
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-xl transition-colors disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Category'}
                </button>
                <button
                  type="button"
                  onClick={() => { setEditingCategory(null); setNewCategoryImage(null); }}
                  className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-xl transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {categories.length === 0 ? (
              <div className="col-span-full text-center text-gray-400 py-8 bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10">
                No categories yet. Add your first class category!
              </div>
            ) : (
              categories.sort((a, b) => a.order - b.order).map((category) => (
                <div key={category.id} className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 overflow-hidden hover:border-indigo-500/30 transition-colors">
                  {category.image && (
                    <div className="h-32 overflow-hidden">
                      <img src={category.image} alt={category.name} className="w-full h-full object-fill" />
                    </div>
                  )}
                  <div className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h3 className="text-white font-medium">{category.name}</h3>
                        {category.classes_range && (
                          <span className="text-indigo-400 text-sm">{category.classes_range}</span>
                        )}
                      </div>
                      <span className={`text-xs px-2 py-1 rounded-full ${category.is_active ? 'bg-green-500/20 text-green-400' : 'bg-gray-500/20 text-gray-400'}`}>
                        {category.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                    <p className="text-gray-400 text-sm line-clamp-2 mb-4">{category.description}</p>
                    <div className="flex gap-2 pt-3 border-t border-white/5">
                      <button
                        onClick={() => {
                          setEditingCategory(category);
                          setInitialCategoryData(category);
                        }}
                        className="flex-1 py-2 text-sm text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => category.id && setDeleteParams({ type: 'categories', id: category.id })}
                        className="flex-1 py-2 text-sm text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Subjects Tab */}
      {activeTab === 'subjects' && (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold text-white">Subjects</h2>
            <button
              onClick={() => {
                const newSub = { name: '', description: '', icon: '', categories: [], is_active: true };
                setEditingSubject(newSub);
                setInitialSubjectData(newSub);
              }}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl transition-colors"
            >
              + Add Subject
            </button>
          </div>

          {editingSubject && (
            <form onSubmit={handleSubjectSubmit} className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6">
              <h3 className="text-md font-semibold text-white mb-4">
                {editingSubject.id ? 'Edit Subject' : 'Add New Subject'}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Subject Name *</label>
                    <input
                      type="text"
                      required
                      value={editingSubject.name}
                      onChange={(e) => setEditingSubject({ ...editingSubject, name: e.target.value })}
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                      placeholder="e.g., Mathematics"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Icon (emoji) *</label>
                    <input
                      type="text"
                      required
                      value={editingSubject.icon}
                      onChange={(e) => setEditingSubject({ ...editingSubject, icon: e.target.value })}
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                      placeholder="e.g., 📐"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Class Categories</label>
                    <p className="text-xs text-gray-500 mb-2">Select all categories where this subject is taught</p>
                    <div className="space-y-2 max-h-48 overflow-y-auto bg-white/5 border border-white/10 rounded-xl p-3">
                      {categories.length === 0 ? (
                        <p className="text-gray-500 text-sm">No categories available. Create categories first.</p>
                      ) : (
                        categories.map((cat) => (
                          <label key={cat.id} className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={editingSubject.categories.includes(cat.id!)}
                              onChange={(e) => {
                                if (e.target.checked) {
                                  setEditingSubject({ ...editingSubject, categories: [...editingSubject.categories, cat.id!] });
                                } else {
                                  setEditingSubject({ ...editingSubject, categories: editingSubject.categories.filter(id => id !== cat.id) });
                                }
                              }}
                              className="w-4 h-4 rounded border-white/20 bg-white/5 text-indigo-600 focus:ring-indigo-500"
                            />
                            <span className="text-white">{cat.name}</span>
                            {cat.classes_range && <span className="text-gray-500 text-sm">({cat.classes_range})</span>}
                          </label>
                        ))
                      )}
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Description</label>
                    <textarea
                      value={editingSubject.description}
                      onChange={(e) => setEditingSubject({ ...editingSubject, description: e.target.value })}
                      rows={4}
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                      placeholder="Describe this subject..."
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Status</label>
                    <select
                      value={editingSubject.is_active ? 'active' : 'inactive'}
                      onChange={(e) => setEditingSubject({ ...editingSubject, is_active: e.target.value === 'active' })}
                      className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
                    >
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                    </select>
                  </div>
                </div>
              </div>
              <div className="flex gap-3 mt-6">
                <button
                  type="submit"
                  disabled={
                    saving || 
                    (JSON.stringify(editingSubject) === JSON.stringify(initialSubjectData)) ||
                    !editingSubject.name ||
                    !editingSubject.icon
                  }
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-xl transition-colors disabled:opacity-50"
                >
                  {saving ? 'Saving...' : 'Save Subject'}
                </button>
                <button
                  type="button"
                  onClick={() => setEditingSubject(null)}
                  className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-xl transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}

          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 overflow-hidden">
            {subjects.length === 0 ? (
              <div className="p-8 text-center text-gray-400">
                No subjects yet. Add your first subject!
              </div>
            ) : (
              <div className="divide-y divide-white/5">
                {subjects.map((subject) => {
                  const assignedCategories = categories.filter(c => subject.categories?.includes(c.id!));
                  return (
                    <div key={subject.id} className="p-4 flex items-center justify-between hover:bg-white/5">
                      <div className="flex items-center gap-4">
                        <div className="w-10 h-10 bg-indigo-600/20 rounded-xl flex items-center justify-center text-xl">
                          {subject.icon || '📚'}
                        </div>
                        <div>
                          <div className="text-white font-medium">{subject.name}</div>
                          <div className="text-gray-400 text-sm flex flex-wrap gap-1">
                            {assignedCategories.length > 0 ? (
                              assignedCategories.map(cat => (
                                <span key={cat.id} className="inline-block px-2 py-0.5 bg-indigo-500/20 text-indigo-300 rounded text-xs">
                                  {cat.name}
                                </span>
                              ))
                            ) : (
                              <span className="text-gray-500">No categories assigned</span>
                            )}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <span className={`text-xs px-2 py-1 rounded-full ${subject.is_active ? 'bg-green-500/20 text-green-400' : 'bg-gray-500/20 text-gray-400'}`}>
                          {subject.is_active ? 'Active' : 'Inactive'}
                        </span>
                        <div className="flex gap-2">
                          <button
                            onClick={() => {
                              setEditingSubject(subject);
                              setInitialSubjectData(subject);
                            }}
                            className="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                          >
                            ✏️
                          </button>
                          <button
                            onClick={() => subject.id && setDeleteParams({ type: 'subjects', id: subject.id })}
                            className="p-2 text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                          >
                            🗑️
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      )}
      {/* Delete Confirmation Modal */}
      {deleteParams && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-slate-900 border border-white/10 rounded-2xl p-6 max-w-md w-full shadow-2xl transform scale-100 transition-all">
            <h3 className="text-xl font-bold text-white mb-2">Confirm Delete</h3>
            <p className="text-gray-400 mb-6">
              Are you sure you want to delete this {deleteParams.type === 'categories' ? 'category' : 'subject'}?
              This action cannot be undone.
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
