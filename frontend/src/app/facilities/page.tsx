import { Metadata } from 'next';
import Link from 'next/link';
import Header from '@/components/home/header';
import Footer from '@/components/home/footer';
import { SiteSettings, Facility, QuickLink } from '@/lib/public-types';

interface FacilitiesPageData {
  site_settings: SiteSettings;
  facilities: Facility[];
  quick_links: QuickLink[];
}

async function getFacilitiesData(): Promise<FacilitiesPageData | null> {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    // Fetch homepage data for site settings and quick links
    const homeRes = await fetch(`${apiUrl}/api/public/home/`, {
      next: { revalidate: 60 },
    });
    
    if (!homeRes.ok) throw new Error('Failed to fetch data');
    
    const homeData = await homeRes.json();
    
    return {
      site_settings: homeData.site_settings,
      facilities: homeData.facilities,
      quick_links: homeData.quick_links,
    };
  } catch (error) {
    console.error('Error fetching facilities data:', error);
    return null;
  }
}

export const metadata: Metadata = {
  title: 'Our Facilities | School',
  description: 'Explore our world-class campus facilities designed for holistic student development.',
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

export default async function FacilitiesPage() {
  const data = await getFacilitiesData();

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
      </div>
    );
  }

  const { site_settings, facilities, quick_links } = data;

  return (
    <main className="bg-white">
      <Header siteSettings={site_settings || defaultSettings} />

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 pt-32 pb-20 lg:pt-40 lg:pb-28 overflow-hidden">
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-blue-500/10 rounded-full blur-3xl" />
          <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-indigo-500/10 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-white/10 border border-white/20 rounded-full text-white/90 text-sm font-medium mb-6">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            Campus Infrastructure
          </div>
          
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6">
            Our <span className="text-amber-400">Facilities</span>
          </h1>
          
          <p className="text-xl text-blue-100 max-w-3xl mx-auto leading-relaxed">
            State-of-the-art infrastructure designed to nurture academic excellence, 
            creativity, and holistic development.
          </p>
        </div>
      </section>

      {/* Facilities Grid */}
      <section className="py-16 sm:py-20 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12">
          {facilities && facilities.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
              {facilities.map((facility, index) => (
                <Link 
                  href={`/facilities/${facility.slug || facility.id}`}
                  key={facility.id}
                  className="group block bg-white rounded-2xl border border-gray-100 overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-2 cursor-pointer"
                >
                  {/* Image or Icon Header */}
                  <div className="h-48 bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center relative overflow-hidden">
                    {facility.image ? (
                      <img 
                        src={facility.image} 
                        alt={facility.name}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                        loading="lazy"
                      />
                    ) : (
                      <span className="text-7xl opacity-80 group-hover:scale-110 transition-transform duration-300">
                        {facility.icon || '🏫'}
                      </span>
                    )}
                    
                    {/* Overlay on hover */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-6">
                      <div className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full text-white text-sm font-medium border border-white/30 translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
                        View Details →
                      </div>
                    </div>
                  </div>
                  
                  {/* Content */}
                  <div className="p-6">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center group-hover:bg-blue-600 group-hover:text-white transition-colors duration-300">
                        <span className="text-xl">{facility.icon || '🏫'}</span>
                      </div>
                      <h3 className="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
                        {facility.name}
                      </h3>
                    </div>
                    <p className="text-gray-600 leading-relaxed line-clamp-2">
                      {facility.description}
                    </p>
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <span className="text-6xl mb-4 block">🏫</span>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">No Facilities Listed</h3>
              <p className="text-gray-600">Facility information will be available soon.</p>
            </div>
          )}
        </div>
      </section>



      <Footer siteSettings={site_settings || defaultSettings} quickLinks={quick_links || []} />
    </main>
  );
}
