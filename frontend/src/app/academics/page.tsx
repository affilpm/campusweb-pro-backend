import { Metadata } from 'next';
import { AcademicsPageData, SiteSettings } from '@/lib/public-types';
import Header from '@/components/home/header';
import Footer from '@/components/home/footer';
import AnimatedSection from '@/components/ui/animated-section';

async function getAcademicsData(): Promise<AcademicsPageData | null> {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const res = await fetch(`${apiUrl}/api/public/academics/`, {
      cache: 'no-store', // Disable caching for immediate admin updates
    });
    if (!res.ok) throw new Error('Failed to fetch');
    return res.json();
  } catch (error) {
    console.error('Error fetching academics data:', error);
    return null;
  }
}

export const metadata: Metadata = {
  title: 'Academics | School',
  description: 'Explore our curriculum, teaching methodology, and academic programs.',
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

export default async function AcademicsPage() {
  const data = await getAcademicsData();

  if (!data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-indigo-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-indigo-600 border-t-transparent mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  const siteSettings = data.site_settings || defaultSettings;
  const quickLinks = data.quick_links || [];

  return (
    <main className="overflow-hidden bg-white">
      <Header siteSettings={siteSettings} />

      {/* Hero Section */}
      {(data.hero_title || data.hero_subtitle) && (
        <section className="relative pt-32 pb-24 md:pb-32 bg-gradient-to-br from-indigo-900 via-purple-900 to-blue-900 text-white overflow-hidden">
          {/* Animated background elements */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '4s' }} />
            <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-indigo-400/20 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '6s' }} />
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-purple-600/10 to-blue-600/10 rounded-full blur-3xl" />
          </div>

          {/* Decorative grid pattern */}
          <div className="absolute inset-0 opacity-5" style={{
            backgroundImage: 'radial-gradient(circle at 1px 1px, white 1px, transparent 0)',
            backgroundSize: '40px 40px'
          }} />

          <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <AnimatedSection className="max-w-4xl mx-auto text-center">
              {data.hero_title && (
                <h1 className="text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-bold mb-6 leading-tight tracking-tight">
                  {data.hero_title}
                </h1>
              )}
              
              {data.hero_subtitle && (
                <p className="text-lg sm:text-xl lg:text-2xl text-purple-100/90 max-w-3xl mx-auto leading-relaxed font-light">
                  {data.hero_subtitle}
                </p>
              )}
            </AnimatedSection>
          </div>

          {/* Bottom wave */}
          <div className="absolute bottom-0 left-0 right-0">
            <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-auto">
              <path d="M0 120L60 105C120 90 240 60 360 45C480 30 600 30 720 37.5C840 45 960 60 1080 67.5C1200 75 1320 75 1380 75L1440 75V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0Z" fill="white"/>
            </svg>
          </div>
        </section>
      )}

      {/* Curriculum Section - Two Column Layout */}
      {(data.curriculum_title || data.curriculum_content) && (
        <section className="py-16 md:py-24 bg-white">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
              <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
                {/* Content Side */}
                <AnimatedSection direction="left">
                  <div className="space-y-6">
                    {data.curriculum_title && (
                      <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 leading-tight">
                        {data.curriculum_title}
                      </h2>
                    )}
                    
                    {data.curriculum_content && (
                      <div className="prose prose-lg text-gray-600 leading-relaxed">
                        {data.curriculum_content.split('\n').map((para, idx) => (
                          <p key={idx} className="mb-4 last:mb-0">{para}</p>
                        ))}
                      </div>
                    )}
                  </div>
                </AnimatedSection>

                {/* Image Side */}
                {data.curriculum_image && (
                  <AnimatedSection direction="right" delay={0.2}>
                    <div className="relative">
                      <div className="absolute -inset-4 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-3xl blur-2xl" />
                      <div className="relative aspect-[4/3] rounded-2xl overflow-hidden shadow-2xl">
                        <img 
                          src={data.curriculum_image} 
                          alt={data.curriculum_title || 'Curriculum'} 
                          className="w-full h-full object-cover"
                        />
                      </div>
                      {/* Decorative element */}
                      <div className="absolute -bottom-6 -right-6 w-24 h-24 bg-amber-400 rounded-2xl -z-10 hidden lg:block" />
                    </div>
                  </AnimatedSection>
                )}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Class Categories / Academic Programs */}
      {data.class_categories && data.class_categories.length > 0 && (
        <section className="py-16 md:py-24 bg-gradient-to-b from-gray-50 to-white">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                {data.class_categories.map((category, idx) => (
                  <AnimatedSection key={category.id} delay={idx * 0.1} direction="up">
                    <div className="group h-full bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-100">
                      {/* Category Image */}
                      {category.image && (
                        <div className="relative h-48 overflow-hidden">
                          <img 
                            src={category.image} 
                            alt={category.name}
                            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                          />
                          <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
                          {category.classes_range && (
                            <div className="absolute bottom-4 left-4 px-3 py-1 bg-white/90 backdrop-blur-sm rounded-full text-sm font-semibold text-indigo-600">
                              {category.classes_range}
                            </div>
                          )}
                        </div>
                      )}
                      
                      {/* Content */}
                      <div className="p-6">
                        {category.name && (
                          <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-indigo-600 transition-colors">
                            {category.name}
                          </h3>
                        )}
                        
                        {!category.image && category.classes_range && (
                          <div className="inline-block px-3 py-1 bg-indigo-50 rounded-full text-sm font-semibold text-indigo-600 mb-3">
                            {category.classes_range}
                          </div>
                        )}
                        
                        {category.description && (
                          <p className="text-gray-600 mb-4 line-clamp-3">{category.description}</p>
                        )}
                        
                        {/* Subjects */}
                        {category.subjects && category.subjects.length > 0 && (
                          <div className="pt-4 border-t border-gray-100">
                            <div className="flex flex-wrap gap-2">
                              {category.subjects.slice(0, 4).map((subject) => (
                                <span 
                                  key={subject.id}
                                  className="inline-flex items-center gap-1 px-3 py-1 bg-gradient-to-r from-indigo-50 to-purple-50 text-indigo-700 text-sm rounded-full font-medium"
                                >
                                  {subject.icon && <span className="text-xs">{subject.icon}</span>}
                                  {subject.name}
                                </span>
                              ))}
                              {category.subjects.length > 4 && (
                                <span className="px-3 py-1 bg-gray-100 text-gray-500 text-sm rounded-full">
                                  +{category.subjects.length - 4} more
                                </span>
                              )}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </AnimatedSection>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Teaching Methodology */}
      {data.methodology_content && (
        <section className="py-16 md:py-24 bg-gradient-to-br from-indigo-900 via-purple-900 to-blue-900 text-white relative overflow-hidden">
          {/* Background decorations */}
          <div className="absolute inset-0">
            <div className="absolute top-0 right-0 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl" />
            <div className="absolute bottom-0 left-0 w-80 h-80 bg-indigo-400/10 rounded-full blur-3xl" />
          </div>

          <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div className="max-w-4xl mx-auto">
              <AnimatedSection className="text-center">
                {data.methodology_title && (
                  <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-8">
                    {data.methodology_title}
                  </h2>
                )}
                
                <div className="relative">
                  {/* Large quote mark */}
                  <div className="absolute -top-8 left-1/2 -translate-x-1/2 text-9xl text-purple-400/20 font-serif leading-none select-none hidden md:block">"</div>
                  
                  <div className="text-lg sm:text-xl text-purple-100 leading-relaxed space-y-4 relative z-10">
                    {data.methodology_content.split('\n').map((para, idx) => (
                      <p key={idx}>{para}</p>
                    ))}
                  </div>
                </div>
              </AnimatedSection>
            </div>
          </div>
        </section>
      )}

      {/* Academic Calendar Download */}
      {(data.calendar_title || data.calendar_file) && (
        <section className="py-16 md:py-24 bg-white">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <AnimatedSection className="max-w-3xl mx-auto">
              <div className="relative bg-gradient-to-br from-amber-50 to-orange-50 rounded-3xl p-8 md:p-12 border border-amber-100 overflow-hidden">
                {/* Decorative elements */}
                <div className="absolute top-0 right-0 w-40 h-40 bg-amber-200/30 rounded-full blur-3xl" />
                <div className="absolute bottom-0 left-0 w-32 h-32 bg-orange-200/30 rounded-full blur-2xl" />

                <div className="relative z-10 text-center">
                  {/* Calendar Icon */}
                  <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-amber-500 to-orange-500 rounded-2xl flex items-center justify-center shadow-lg shadow-amber-500/30">
                    <svg className="w-10 h-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>

                  {data.calendar_title && (
                    <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
                      {data.calendar_title}
                    </h2>
                  )}
                  
                  {data.calendar_file && (
                    <a 
                      href={data.calendar_file}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-amber-500 to-orange-500 text-white font-bold rounded-full shadow-lg hover:shadow-xl hover:scale-105 transition-all"
                    >
                      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Download Calendar
                    </a>
                  )}
                </div>
              </div>
            </AnimatedSection>
          </div>
        </section>
      )}

      <Footer siteSettings={siteSettings} quickLinks={quickLinks} />
    </main>
  );
}
