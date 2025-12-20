import { Metadata } from 'next';
import Link from 'next/link';
import Header from '@/components/home/header';
import Footer from '@/components/home/footer';
import { Notice, HomepageData } from '@/lib/public-types';

export const metadata: Metadata = {
  title: 'All Notices | School Website',
  description: 'Latest updates, announcements and notices from our school.',
};

async function getData() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  try {
    const [homeRes, noticesRes] = await Promise.all([
      fetch(`${apiUrl}/api/public/home/`, { next: { revalidate: 60 } }),
      fetch(`${apiUrl}/api/public/notices/`, { next: { revalidate: 60 } })
    ]);

    if (!homeRes.ok || !noticesRes.ok) {
      throw new Error('Failed to fetch data');
    }

    const homeData: HomepageData = await homeRes.json();
    const notices: Notice[] = await noticesRes.json();

    return {
      site_settings: homeData.site_settings,
      quick_links: homeData.quick_links,
      notices
    };
  } catch (error) {
    console.error('Error fetching notices page data:', error);
    return null;
  }
}

export default async function NoticesPage() {
  const data = await getData();

  if (!data) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Page</h1>
          <p className="text-gray-600">Please try again later.</p>
        </div>
      </div>
    );
  }

  const { site_settings, notices, quick_links } = data;

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <main className="min-h-screen bg-gray-50 flex flex-col">
      <Header siteSettings={site_settings} />

      {/* Page Header with Dark Background */}
      <div className="pt-32 pb-12 sm:pb-16 bg-gradient-to-br from-blue-900 via-indigo-900 to-blue-800 text-white relative overflow-hidden">
        {/* Abstract shapes */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-amber-500/10 rounded-full blur-2xl translate-y-1/2 -translate-x-1/2" />
        
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4 sm:mb-6">
            School Notice Board
          </h1>
          <p className="text-lg sm:text-xl text-blue-100 max-w-2xl mx-auto leading-relaxed">
            Stay updated with the latest announcements, circulars, and news from the school administration.
          </p>
        </div>
      </div>

      <div className="flex-grow py-12 sm:py-16 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Notices List */}
          <div className="space-y-4">
            {notices.length === 0 ? (
              <div className="text-center py-12 bg-white rounded-2xl shadow-sm border border-gray-100">
                <span className="text-4xl block mb-4">📭</span>
                <p className="text-gray-500 text-lg">No notices published yet.</p>
              </div>
            ) : (
              notices.map((notice) => (
                <div 
                  key={notice.id}
                  className="group block bg-white rounded-xl shadow-sm hover:shadow-md border border-gray-100 p-6 transition-all duration-200"
                >
                  <div className="flex flex-col gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className="text-sm font-medium text-amber-600 bg-amber-50 px-2 py-1 rounded-md">
                          {formatDate(notice.publish_date)}
                        </span>
                        {notice.is_important && (
                          <span className="text-xs font-bold text-red-600 bg-red-50 px-2 py-1 rounded-md uppercase tracking-wide">
                            Important
                          </span>
                        )}
                      </div>
                      <h2 className="text-xl font-semibold text-gray-900 mb-4">
                        {notice.title}
                      </h2>
                      <div className="prose prose-amber max-w-none text-gray-700 whitespace-pre-wrap leading-relaxed">
                        {notice.content}
                      </div>
                      
                      {/* Attachment */}
                      {notice.attachment && (
                        <div className="mt-6 pt-4 border-t border-gray-100">
                          <a 
                            href={notice.attachment} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="inline-flex items-center p-3 rounded-lg border border-gray-200 bg-gray-50 hover:bg-white hover:border-amber-400 hover:shadow-sm transition-all group"
                          >
                            <div className="w-8 h-8 rounded-md bg-amber-100 text-amber-600 flex items-center justify-center mr-3 group-hover:scale-110 transition-transform">
                              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                              </svg>
                            </div>
                            <div>
                              <p className="font-medium text-gray-900 group-hover:text-amber-700 text-sm">Download Attachment</p>
                              <p className="text-xs text-gray-500">Click to view or download</p>
                            </div>
                          </a>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      <Footer siteSettings={site_settings} quickLinks={quick_links} />
    </main>
  );
}
