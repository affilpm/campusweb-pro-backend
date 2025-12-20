import { Metadata } from 'next';
import { AdmissionSettings, SiteSettings } from '@/lib/public-types';
import Header from '@/components/home/header';
import Footer from '@/components/home/footer';
import Link from 'next/link';

async function getAdmissionsData(): Promise<AdmissionSettings | null> {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const res = await fetch(`${apiUrl}/api/public/admissions/`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) throw new Error('Failed to fetch');
    return res.json();
  } catch (error) {
    console.error('Error fetching admissions data:', error);
    return null;
  }
}

export const metadata: Metadata = {
  title: 'Admissions | School',
  description: 'Apply for admission. Learn about our admission process, eligibility, and fee structure.',
};

const defaultSettings: SiteSettings = {
  school_name: 'School',
  school_motto: '',
  school_logo: null,
  favicon: null,
  address: '',
  phone: '',
  email: '',
  facebook_url: '',
  twitter_url: '',
  instagram_url: '',
  youtube_url: '',
  footer_text: ''
};

export default async function AdmissionsPage() {
  const data = await getAdmissionsData();

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
      </div>
    );
  }

  const siteSettings = data.site_settings || defaultSettings;
  const quickLinks = data.quick_links || [];

  return (
    <main className="bg-white">
      <Header siteSettings={siteSettings} />

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 pt-32 pb-24 lg:pt-40 lg:pb-32 overflow-hidden">
        {/* Decorative Elements */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-blue-500/10 rounded-full blur-3xl" />
          <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-indigo-500/10 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-6 sm:px-8 lg:px-12 text-center">
          {/* Status Badge */}
          <div className={`inline-flex items-center gap-2 px-5 py-2 rounded-full text-sm font-semibold mb-8 ${
            data.is_open 
              ? 'bg-green-500/20 text-green-300 border border-green-500/30' 
              : 'bg-red-500/20 text-red-300 border border-red-500/30'
          }`}>
            <span className={`w-2 h-2 rounded-full ${data.is_open ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
            {data.is_open ? 'Admissions Open' : 'Admissions Currently Closed'}
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-8 leading-tight">
            {data.hero_title || 'Admission Process'}
          </h1>
          
          <p className="text-xl lg:text-2xl text-blue-100 max-w-3xl mx-auto mb-12 leading-relaxed">
            {data.hero_subtitle || 'Join our vibrant community of learners. We nurture young minds to achieve their full potential.'}
          </p>

          {data.is_open && data.application_form_link && (
            <a 
              href={data.application_form_link}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-3 px-10 py-5 bg-amber-500 hover:bg-amber-600 text-white font-bold text-lg rounded-lg transition-all duration-300 shadow-xl hover:shadow-2xl hover:-translate-y-1"
            >
              Apply Online
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </a>
          )}
        </div>
      </section>

      {/* Admission Process (Overview) */}
      {(data.overview_title || data.overview_content) && (
        <section className="py-24 lg:py-32 bg-white">
          <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
            <div className="text-center mb-16 lg:mb-20">
              <div className="inline-block px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold mb-6">
                Overview
              </div>
              <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
                {data.overview_title || 'Admission Process'}
              </h2>
              {data.overview_content && (
                <p className="text-xl text-gray-600 max-w-3xl mx-auto whitespace-pre-line">
                  {data.overview_content}
                </p>
              )}
            </div>

            {/* Steps Grid */}
            {data.steps && data.steps.length > 0 && (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 lg:gap-10 mt-12">
                {data.steps.map((step, idx) => (
                  <div 
                    key={idx} 
                    className="relative bg-gray-50 rounded-2xl p-8 lg:p-10 border border-gray-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
                  >
                    <div className="w-14 h-14 bg-blue-600 text-white rounded-xl flex items-center justify-center text-2xl font-bold mb-6 shadow-lg">
                      {step.step_number}
                    </div>
                    
                    <h3 className="text-xl font-bold text-gray-900 mb-4">
                      {step.title}
                    </h3>
                    <p className="text-gray-600 leading-relaxed">
                      {step.description}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>
      )}

      {/* Eligibility & Documents */}
      <section className="py-24 lg:py-32 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
          <div className="grid lg:grid-cols-2 gap-10 lg:gap-16">
            {/* Eligibility */}
            {data.eligibility_content && (
              <div className="bg-white rounded-2xl p-10 lg:p-12 shadow-sm border border-gray-100">
                <div className="flex items-center gap-4 mb-8">
                  <div className="w-14 h-14 bg-blue-100 rounded-xl flex items-center justify-center">
                    <svg className="w-7 h-7 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900">
                    {data.eligibility_title || 'Eligibility Criteria'}
                  </h3>
                </div>
                <div className="prose prose-lg text-gray-600 max-w-none">
                  {data.eligibility_content.split('\n').filter(Boolean).map((line, idx) => (
                    <div key={idx} className="flex gap-3 mb-4">
                      <span className="text-blue-500 font-bold mt-1">•</span>
                      <p className="m-0">{line}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Documents */}
            {data.documents_required && (
              <div className="bg-white rounded-2xl p-10 lg:p-12 shadow-sm border border-gray-100">
                <div className="flex items-center gap-4 mb-8">
                  <div className="w-14 h-14 bg-amber-100 rounded-xl flex items-center justify-center">
                    <svg className="w-7 h-7 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900">
                    Required Documents
                  </h3>
                </div>
                <div className="space-y-4">
                  {data.documents_required.split('\n').filter(Boolean).map((line, idx) => (
                    <div key={idx} className="flex items-start gap-3">
                      <svg className="w-5 h-5 text-green-500 mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <p className="text-gray-600">{line}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Contact CTA */}
      <section className="py-24 lg:py-32 bg-white">
        <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12 text-center">
          <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Have Questions?
          </h2>
          <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto">
            Our admissions team is here to help. Reach out to us for any queries.
          </p>
          


          <div className="flex justify-center">
            <Link
              href="/contact"
              className="inline-flex items-center gap-2 px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors"
            >
              Contact Us
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      <Footer siteSettings={siteSettings} quickLinks={quickLinks} />
    </main>
  );
}
