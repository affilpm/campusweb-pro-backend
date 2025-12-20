'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';

interface AdmissionSettings {
  id?: number;
  is_open: boolean;
  hero_title: string;
  hero_subtitle: string;
  overview_title: string;
  overview_content: string;
  eligibility_title: string;
  eligibility_content: string;
  documents_required: string;
  contact_info: string;
  application_form_link: string;
}

interface AdmissionStep {
  id?: number;
  step_number: number;
  title: string;
  description: string;
}

export default function AdmissionsManagementPage() {
  const [settings, setSettings] = useState<AdmissionSettings | null>(null);
  const [initialSettings, setInitialSettings] = useState<AdmissionSettings | null>(null);
  const [steps, setSteps] = useState<AdmissionStep[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [editingStep, setEditingStep] = useState<AdmissionStep | null>(null);
  const [initialStepData, setInitialStepData] = useState<AdmissionStep | null>(null);
  const [showStepModal, setShowStepModal] = useState(false);
  const [errors, setErrors] = useState<Record<string, string[]>>({});
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [settingsRes, stepsRes] = await Promise.all([
        api.get('/api/admin/content/admissions/settings/'),
        api.get('/api/admin/content/admissions/steps/')
      ]);
      setSettings(settingsRes.data);
      setInitialSettings(settingsRes.data);
      setSteps(stepsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSettingsChange = (field: keyof AdmissionSettings, value: any) => {
    setSettings(s => s ? { ...s, [field]: value } : null);
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: [] }));
    }
  };

  const handleSaveSettings = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!settings) return;
    
    setSaving(true);
    setErrors({});
    setMessage('');

    try {
      await api.put('/api/admin/content/admissions/settings/', settings);
      setMessage('Settings saved successfully!');
      setTimeout(() => setMessage(''), 3000);
      setInitialSettings(settings);
    } catch (error: any) {
      console.error('Error saving settings:', error);
      if (error.response && error.response.status === 400) {
        setErrors(error.response.data);
        setMessage('Please check the form for errors.');
      } else {
        setMessage('Error saving settings');
      }
    } finally {
      setSaving(false);
    }
  };

  const handleSaveStep = async () => {
    if (!editingStep) return;
    
    try {
      if (editingStep.id) {
        await api.put(`/api/admin/content/admissions/steps/${editingStep.id}/`, editingStep);
      } else {
        await api.post('/api/admin/content/admissions/steps/', editingStep);
      }
      fetchData();
      setShowStepModal(false);
      setEditingStep(null);
    } catch (error) {
      console.error('Error saving step:', error);
    }
  };

  const requestDelete = (id: number) => {
    setDeleteId(id);
  };

  const confirmDelete = async () => {
    if (!deleteId) return;
    
    try {
      await api.delete(`/api/admin/content/admissions/steps/${deleteId}/`);
      fetchData();
    } catch (error) {
       console.error('Error deleting step:', error);
    } finally {
       setDeleteId(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-4xl">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white">Admissions Management</h1>
          <p className="text-gray-400">Manage admission settings and process steps</p>
        </div>
      </div>

      {message && (
        <div className={`p-4 rounded-lg ${message.includes('Error') || message.includes('check') ? 'bg-red-500/20 text-red-400 border border-red-500/20' : 'bg-green-500/20 text-green-400 border border-green-500/20'}`}>
          {message}
        </div>
      )}

      {/* Settings Form */}
      <form onSubmit={handleSaveSettings} className="bg-slate-800/50 backdrop-blur-xl border border-white/10 rounded-xl p-6 space-y-6">
        <h2 className="text-lg font-semibold text-white border-b border-white/10 pb-2">Admission Settings</h2>
        
        {/* Admission Status Toggle */}
        <div className="flex items-center gap-4">
          <label className="text-sm font-medium text-gray-300">Admissions Status</label>
          <button
            type="button"
            onClick={() => setSettings(s => s ? { ...s, is_open: !s.is_open } : null)}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
              settings?.is_open ? 'bg-green-600' : 'bg-gray-600'
            }`}
          >
            <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
              settings?.is_open ? 'translate-x-6' : 'translate-x-1'
            }`} />
          </button>
          <span className={`text-sm font-medium ${settings?.is_open ? 'text-green-400' : 'text-red-400'}`}>
            {settings?.is_open ? 'Open' : 'Closed'}
          </span>
        </div>

        {/* Hero Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Hero Title *</label>
            <input
              type="text"
              value={settings?.hero_title || ''}
              onChange={(e) => handleSettingsChange('hero_title', e.target.value)}
              required
              className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                errors.hero_title ? 'border-red-500/50' : 'border-white/10'
              }`}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Hero Subtitle</label>
            <input
              type="text"
              value={settings?.hero_subtitle || ''}
              onChange={(e) => handleSettingsChange('hero_subtitle', e.target.value)}
              className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
                errors.hero_subtitle ? 'border-red-500/50' : 'border-white/10'
              }`}
            />
          </div>
        </div>

        {/* Overview Section */}
        <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Overview Title</label>
              <input
                type="text"
                value={settings?.overview_title || ''}
                onChange={(e) => handleSettingsChange('overview_title', e.target.value)}
                className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50`}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Overview Content</label>
              <textarea
                value={settings?.overview_content || ''}
                onChange={(e) => handleSettingsChange('overview_content', e.target.value)}
                rows={3}
                className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50`}
              />
            </div>
        </div>

        {/* Eligibility Section */}
        <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Eligibility Title</label>
              <input
                type="text"
                value={settings?.eligibility_title || ''}
                onChange={(e) => handleSettingsChange('eligibility_title', e.target.value)}
                className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50`}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Eligibility Content</label>
              <textarea
                value={settings?.eligibility_content || ''}
                onChange={(e) => handleSettingsChange('eligibility_content', e.target.value)}
                rows={3}
                className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50`}
              />
            </div>
        </div>

        {/* Documents Section */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">Documents Required</label>
          <textarea
            value={settings?.documents_required || ''}
            onChange={(e) => handleSettingsChange('documents_required', e.target.value)}
            rows={4}
            placeholder="Enter each document on a new line"
            className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50`}
          />
        </div>

        {/* Application Form Link */}
        <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Application Form Link</label>
            <input
              type="url"
              value={settings?.application_form_link || ''}
              onChange={(e) => handleSettingsChange('application_form_link', e.target.value)}
              placeholder="https://forms.google.com/..."
              className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50`}
            />
            <p className="text-xs text-gray-500">URL to the external application form (e.g., Google Form)</p>
        </div>

        {/* Contact Info */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-300">Admission Contact Info</label>
          <textarea
            value={settings?.contact_info || ''}
            onChange={(e) => handleSettingsChange('contact_info', e.target.value)}
            rows={3}
            placeholder="Phone numbers, emails, timings..."
            className={`w-full px-4 py-2.5 bg-white/5 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50`}
          />
        </div>

        <div className="flex justify-end pt-4">
          <button
            type="submit"
            disabled={saving}
            className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg transition-colors disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      </form>

      {/* Admission Steps */}
      <div className="bg-slate-800/50 backdrop-blur-xl border border-white/10 rounded-xl p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-lg font-semibold text-white">Admission Steps</h2>
          <button
            onClick={() => {
              const newStep = { step_number: steps.length + 1, title: '', description: '' };
              setEditingStep(newStep);
              setInitialStepData(newStep);
              setShowStepModal(true);
            }}
            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            Add Step
          </button>
        </div>

        <div className="space-y-4">
          {steps.map((step) => (
            <div key={step.id} className="flex items-center gap-4 p-4 bg-white/5 border border-white/10 rounded-xl">
              <div className="w-10 h-10 bg-purple-600 text-white rounded-full flex items-center justify-center font-bold">
                {step.step_number}
              </div>
              <div className="flex-1">
                <h3 className="font-medium text-white">{step.title}</h3>
                <p className="text-sm text-gray-400">{step.description}</p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => {
                    setEditingStep(step);
                    setInitialStepData(step);
                    setShowStepModal(true);
                  }}
                  className="p-2 hover:bg-white/5 rounded-lg text-gray-400 hover:text-white transition-colors"
                >
                  Edit
                </button>
                <button
                  onClick={() => step.id && requestDelete(step.id)}
                  className="p-2 hover:bg-red-500/10 rounded-lg text-gray-400 hover:text-red-400 transition-colors"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}

          {steps.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No admission steps defined yet. Add your first step!
            </div>
          )}
        </div>
      </div>

      {/* Step Modal */}
      {showStepModal && editingStep && (
        <div 
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => setShowStepModal(false)}
        >
          <div 
            className="bg-slate-900 border border-white/10 rounded-2xl w-full max-w-md"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6 border-b border-white/10 flex items-center justify-between">
              <h2 className="text-xl font-bold text-white">
                {editingStep.id ? 'Edit Step' : 'Add Step'}
              </h2>
              <button onClick={() => setShowStepModal(false)} className="text-gray-400 hover:text-white">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="p-6 space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Step Number *</label>
                <input
                  type="number"
                  required
                  value={editingStep.step_number}
                  onChange={(e) => setEditingStep({ ...editingStep, step_number: parseInt(e.target.value) })}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Title *</label>
                <input
                  type="text"
                  required
                  value={editingStep.title}
                  onChange={(e) => setEditingStep({ ...editingStep, title: e.target.value })}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Description *</label>
                <textarea
                  required
                  value={editingStep.description}
                  onChange={(e) => setEditingStep({ ...editingStep, description: e.target.value })}
                  rows={3}
                  className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                />
              </div>
            </div>

            <div className="p-6 border-t border-white/10 flex justify-end gap-3">
              <button
                onClick={() => {
                  setShowStepModal(false);
                  setEditingStep(null);
                }}
                className="px-4 py-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveStep}
                disabled={
                  saving || 
                  JSON.stringify(editingStep) === JSON.stringify(initialStepData) ||
                  !editingStep.title ||
                  !editingStep.description
                }
                className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg transition-colors disabled:opacity-50"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}
      {deleteId && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-slate-900 border border-white/10 rounded-2xl p-6 max-w-md w-full shadow-2xl transform scale-100 transition-all">
            <h3 className="text-xl font-bold text-white mb-2">Confirm Delete</h3>
            <p className="text-gray-400 mb-6">
              Are you sure you want to delete this step? This action cannot be undone.
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
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
