import { Metadata } from 'next';
import { HomepageData } from '@/lib/public-types';

// Components
import Header from '../components/home/header';
import HeroSection from '../components/home/hero-section';
import StatsSection from '../components/home/stats-section';
import AboutSection from '../components/home/about-section';
import PrincipalSection from '../components/home/principal-section';
import FacilitiesSection from '../components/home/facilities-section';
import AchievementsSection from '../components/home/achievements-section';
import NoticesSection from '../components/home/notices-section';
import EventsSection from '../components/home/events-section';
import GallerySection from '../components/home/gallery-section';
import CTASection from '../components/home/cta-section';
import TestimonialsSection from '../components/home/testimonials-section';
import PublicDisclosureSection from '../components/home/public-disclosure-section';
import Footer from '../components/home/footer';

// Fetch homepage data from Django API with ISR
async function getHomepageData(): Promise<HomepageData | null> {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const res = await fetch(`${apiUrl}/api/public/home/`, {
      next: { revalidate: 60 }, // ISR: revalidate every 60 seconds
    });
    
    if (!res.ok) {
      throw new Error('Failed to fetch homepage data');
    }
    
    return res.json();
  } catch (error) {
    console.error('Error fetching homepage data:', error);
    return null;
  }
}

// Dynamic metadata based on site settings
export async function generateMetadata(): Promise<Metadata> {
  const data = await getHomepageData();
  
  return {
    title: data?.site_settings?.school_name || 'School Website',
    description: data?.site_settings?.school_motto || 'Quality education for tomorrow\'s leaders',
    keywords: ['school', 'education', 'CBSE', 'academics', 'admissions'],
    openGraph: {
      title: data?.site_settings?.school_name,
      description: data?.site_settings?.school_motto,
      type: 'website',
    },
  };
}

export default async function HomePage() {
  const data = await getHomepageData();
  
  // Loading/Error State
  if (!data) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 to-indigo-900 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-4 border-white border-t-transparent mb-6"></div>
          <h1 className="text-2xl font-bold text-white mb-2">Loading...</h1>
          <p className="text-blue-200">Please wait while we load the content</p>
        </div>
      </div>
    );
  }

  const { 
    site_settings, 
    hero, 
    about, 
    principal, 
    notices, 
    events, 
    gallery, 
    facilities, 
    academics, 
    achievements,
    testimonials, 
    quick_links,
    general_info
  } = data;

  return (
    <main className="overflow-hidden">
      {/* Sticky Header */}
      <Header siteSettings={site_settings} />

      {/* Hero Section - Full screen with animations */}
      <HeroSection 
        data={hero} 
        schoolName={site_settings.school_name} 
      />

      {/* Notices Banner - Animated ticker */}
      <NoticesSection notices={notices} />

      {/* Stats Section - Animated counters */}
      <StatsSection 
        stats={[
          { id: 'est', value: about.established_year?.toString() || '1990', label: 'Established' },
          { id: 'students', value: about.students_count || '2000+', label: 'Students' },
          { id: 'teachers', value: about.teachers_count || '100+', label: 'Teachers' },
          ...(academics || []).map(a => ({ id: `acad-${a.id}`, value: a.value, label: a.title }))
        ]}
      />

      {/* About Section - Interactive split layout */}
      <AboutSection data={about} />

      {/* Principal's Message - Premium card design */}
      <PrincipalSection data={principal} />

      {/* Facilities Section - Dynamic grid with hover effects */}
      <FacilitiesSection facilities={facilities} />

      {/* Achievements Section - Awards and Recognition */}
      <AchievementsSection achievements={achievements} />

      {/* Events Section - Horizontal slider */}
      <EventsSection events={events} />

      {/* Gallery Section - Masonry with lightbox */}
      <GallerySection images={gallery} />

      {/* CTA Section - Parallax background */}
      <CTASection />

      {/* Testimonials Section - Interactive carousel */}
      <TestimonialsSection testimonials={testimonials} />

      {/* Public Disclosure Section - Information table */}
      <PublicDisclosureSection items={general_info} />

      {/* Footer - Modern multi-column */}
      <Footer 
        siteSettings={site_settings} 
        quickLinks={quick_links} 
      />
    </main>
  );
}
