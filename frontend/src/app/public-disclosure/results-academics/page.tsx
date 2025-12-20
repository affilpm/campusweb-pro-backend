import { Metadata } from 'next';
import { SiteSettings, QuickLink } from '@/lib/public-types';
import Header from '@/components/home/header';
import Footer from '@/components/home/footer';

interface ResultsAcademicsItem {
  id: number;
  title: string;
  file: string;
  order: number;
}

interface PageData {
  site_settings: SiteSettings;
  quick_links: QuickLink[];
  results_academics: ResultsAcademicsItem[];
}

async function getPageData(): Promise<PageData | null> {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    // Fetch site settings from homepage
    const homeRes = await fetch(`${apiUrl}/api/public/home/`, {
      cache: 'no-store',
    });
    
    // Fetch results & academics
    const resultsRes = await fetch(`${apiUrl}/api/public/results-academics/`, {
      cache: 'no-store',
    });
    
    if (!homeRes.ok) throw new Error('Failed to fetch');
    const homeData = await homeRes.json();
    const resultsData = resultsRes.ok ? await resultsRes.json() : [];
    
    return {
      site_settings: homeData.site_settings,
      quick_links: homeData.quick_links || [],
      results_academics: resultsData,
    };
  } catch (error) {
    console.error('Error fetching data:', error);
    return null;
  }
}

export const metadata: Metadata = {
  title: 'Results & Academics | Public Disclosure',
  description: 'Download academic results, reports, and related documents.',
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

export default async function ResultsAcademicsPage() {
  const data = await getPageData();

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  const siteSettings = data.site_settings || defaultSettings;
  const quickLinks = data.quick_links || [];
  const resultsAcademics = data.results_academics || [];

  return (
    <main className="overflow-hidden bg-white">
      <Header siteSettings={siteSettings} />

      {/* Hero Section */}
      <section className="relative pt-32 pb-16 md:pb-20 bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 text-white overflow-hidden">
        {/* Background decorations */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '4s' }} />
          <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-indigo-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '6s' }} />
        </div>

        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            {/* Breadcrumb */}
            <div className="inline-flex items-center gap-2 text-sm text-blue-200 mb-6">
              <a href="/" className="hover:text-white transition-colors">Home</a>
              <span>/</span>
              <a href="/public-disclosure" className="hover:text-white transition-colors">Public Disclosure</a>
              <span>/</span>
              <span className="text-white">Results & Academics</span>
            </div>
            
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-4 leading-tight tracking-tight">
              Results & Academics
            </h1>
            <p className="text-lg sm:text-xl text-blue-100/90 max-w-2xl mx-auto">
              Download academic results, reports, and related documents
            </p>
          </div>
        </div>

        {/* Bottom wave */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-auto">
            <path d="M0 120L60 105C120 90 240 60 360 45C480 30 600 30 720 37.5C840 45 960 60 1080 67.5C1200 75 1320 75 1380 75L1440 75V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0Z" fill="white"/>
          </svg>
        </div>
      </section>

      {/* Results Table Section */}
      <section className="py-16 md:py-24 bg-white">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
            {resultsAcademics.length === 0 ? (
              <div className="text-center py-16 bg-gray-50 rounded-2xl">
                <p className="text-gray-500 text-lg">No documents available at this time.</p>
              </div>
            ) : (
              <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="bg-gradient-to-r from-emerald-500 to-teal-600 text-white">
                        <th className="py-4 px-6 text-left text-sm font-semibold uppercase tracking-wider w-24">
                          Sl.No.
                        </th>
                        <th className="py-4 px-6 text-left text-sm font-semibold uppercase tracking-wider">
                          Documents/Information
                        </th>
                        <th className="py-4 px-6 text-center text-sm font-semibold uppercase tracking-wider w-44">
                          Download Documents
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {resultsAcademics.map((item, index) => (
                        <tr 
                          key={item.id} 
                          className="hover:bg-emerald-50/50 transition-colors"
                        >
                          <td className="py-5 px-6 text-gray-900 font-semibold text-center">
                            {index + 1}
                          </td>
                          <td className="py-5 px-6 text-gray-900 font-medium">
                            {item.title}
                          </td>
                          <td className="py-5 px-6 text-center">
                            <a
                              href={item.file}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-semibold rounded-lg transition-all shadow-md hover:shadow-lg"
                            >
                              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                              </svg>
                              Download
                            </a>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      <Footer siteSettings={siteSettings} quickLinks={quickLinks} />
    </main>
  );
}
