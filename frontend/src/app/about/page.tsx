import { Metadata } from 'next';
import { AboutPageData, SiteSettings } from '@/lib/public-types';
import Header from '@/components/home/header';
import Footer from '@/components/home/footer';
import AnimatedSection from '@/components/ui/animated-section';

async function getAboutData(): Promise<AboutPageData | null> {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const res = await fetch(`${apiUrl}/api/public/about/`, {
      cache: 'no-store', // Disable caching for immediate admin updates
    });
    if (!res.ok) throw new Error('Failed to fetch');
    return res.json();
  } catch (error) {
    console.error('Error fetching about data:', error);
    return null;
  }
}

export const metadata: Metadata = {
  title: 'About Us | School',
  description: 'Learn about our school history, vision, mission, and leadership.',
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

export default async function AboutPage() {
  const data = await getAboutData();

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

  return (
    <main className="overflow-hidden bg-white">
      <Header siteSettings={siteSettings} />

      {/* Hero Section */}
      {(data.hero_title || data.hero_subtitle) && (
        <section className="relative pt-32 pb-24 md:pb-32 bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 text-white overflow-hidden">
          {/* Animated background elements */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '4s' }} />
            <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-indigo-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDuration: '6s' }} />
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-blue-600/10 to-purple-600/10 rounded-full blur-3xl" />
          </div>
          
          {/* Subtle grid pattern overlay */}
          <div className="absolute inset-0 opacity-5" style={{
            backgroundImage: 'radial-gradient(circle at 1px 1px, white 1px, transparent 0)',
            backgroundSize: '40px 40px'
          }} />

          <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <AnimatedSection className="max-w-4xl mx-auto text-center">
              {/* Badge with established year */}
              {data.about_section?.established_year && (
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full text-sm font-medium mb-8 border border-white/10">
                  <span className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" />
                  {data.about_section.established_year}
                </div>
              )}
              
              {data.hero_title && (
                <h1 className="text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-bold mb-6 leading-tight tracking-tight">
                  {data.hero_title}
                </h1>
              )}
              
              {data.hero_subtitle && (
                <p className="text-lg sm:text-xl lg:text-2xl text-blue-100/90 max-w-3xl mx-auto leading-relaxed font-light">
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

      {/* About Overview - Two Column Layout */}
      {data.about_section && (data.about_section.title || data.about_section.content) && (
        <section className="py-16 md:py-24 bg-white">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
              <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
                {/* Content Side */}
                <AnimatedSection direction="left">
                  <div className="space-y-6">
                    {data.about_section.title && (
                      <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 leading-tight">
                        {data.about_section.title}
                      </h2>
                    )}
                    
                    {data.about_section.content && (
                      <div className="prose prose-lg text-gray-600 leading-relaxed">
                        {data.about_section.content.split('\n').map((para, idx) => (
                          <p key={idx} className="mb-4 last:mb-0">{para}</p>
                        ))}
                      </div>
                    )}

                    {/* Stats Row */}
                    {(data.about_section.established_year || data.about_section.students_count || data.about_section.teachers_count) && (
                      <div className="flex flex-wrap gap-8 pt-6 border-t border-gray-100">
                        {data.about_section.established_year && (
                          <div className="group">
                            <div className="text-3xl sm:text-4xl font-bold text-blue-600 group-hover:scale-105 transition-transform">
                              {data.about_section.established_year}
                            </div>
                            <div className="text-sm text-gray-500 font-medium uppercase tracking-wide">Established</div>
                          </div>
                        )}
                        {data.about_section.students_count && (
                          <div className="group">
                            <div className="text-3xl sm:text-4xl font-bold text-blue-600 group-hover:scale-105 transition-transform">
                              {data.about_section.students_count}
                            </div>
                            <div className="text-sm text-gray-500 font-medium uppercase tracking-wide">Students</div>
                          </div>
                        )}
                        {data.about_section.teachers_count && (
                          <div className="group">
                            <div className="text-3xl sm:text-4xl font-bold text-blue-600 group-hover:scale-105 transition-transform">
                              {data.about_section.teachers_count}
                            </div>
                            <div className="text-sm text-gray-500 font-medium uppercase tracking-wide">Teachers</div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </AnimatedSection>

                {/* Image Side */}
                {data.about_section.image && (
                  <AnimatedSection direction="right" delay={0.2}>
                    <div className="relative">
                      <div className="absolute -inset-4 bg-gradient-to-r from-blue-500/20 to-indigo-500/20 rounded-3xl blur-2xl" />
                      <div className="relative aspect-[4/3] rounded-2xl overflow-hidden shadow-2xl">
                        <img 
                          src={data.about_section.image} 
                          alt={data.about_section.title || ''} 
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

      {/* History Section */}
      {data.history_content && (
        <section className="py-16 md:py-24 bg-gradient-to-b from-gray-50 to-white">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className={`max-w-7xl mx-auto ${!data.history_image && 'text-center'}`}>
              <div className={`grid gap-12 items-center ${data.history_image ? 'lg:grid-cols-2' : 'max-w-4xl mx-auto'}`}>
                
                {/* Content Side */}
                <div className={data.history_image ? 'order-2 lg:order-1' : ''}>
                  {data.history_title && (
                    <AnimatedSection className="mb-8">
                      <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900">
                        {data.history_title}
                      </h2>
                    </AnimatedSection>
                  )}
                  
                  <AnimatedSection delay={0.1}>
                    <div className={`relative ${!data.history_image && 'bg-white rounded-3xl shadow-xl p-8 md:p-12 border border-gray-100 text-left'}`}>
                      {!data.history_image && (
                        <div className="absolute top-6 left-6 text-8xl text-blue-100 font-serif leading-none select-none">"</div>
                      )}
                      
                      <div className="relative prose prose-lg max-w-none text-gray-600 leading-relaxed">
                        {data.history_content.split('\n').map((para, idx) => (
                          <p key={idx} className="mb-4 last:mb-0">{para}</p>
                        ))}
                      </div>
                    </div>
                  </AnimatedSection>
                </div>

                {/* Image Side */}
                {data.history_image && (
                  <AnimatedSection delay={0.2} className="order-1 lg:order-2">
                    <div className="relative">
                      <div className="absolute -inset-4 bg-gradient-to-r from-amber-500/20 to-orange-500/20 rounded-3xl blur-2xl" />
                      <div className="relative aspect-[4/3] rounded-2xl overflow-hidden shadow-2xl">
                        <img 
                          src={data.history_image} 
                          alt={data.history_title || 'Our History'} 
                          className="w-full h-full object-cover"
                        />
                      </div>
                      {/* Decorative element */}
                      <div className="absolute -bottom-6 -left-6 w-24 h-24 bg-blue-500 rounded-2xl -z-10 hidden lg:block" />
                    </div>
                  </AnimatedSection>
                )}

              </div>
            </div>
          </div>
        </section>
      )}

      {/* Vision & Mission Cards */}
      {data.vision_mission && (data.vision_mission.vision_content || data.vision_mission.mission_content || data.vision_mission.values_content) && (
        <section className="py-16 md:py-24 bg-white">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                {/* Vision Card */}
                {data.vision_mission.vision_content && (
                  <AnimatedSection delay={0.1} direction="up">
                    <div className="group h-full bg-gradient-to-br from-blue-50 to-indigo-50 rounded-3xl p-8 border border-blue-100 hover:shadow-xl hover:shadow-blue-100/50 transition-all duration-300 hover:-translate-y-1">
                      <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-blue-500/30 group-hover:scale-110 transition-transform">
                        <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                      </div>
                      {data.vision_mission.vision_title && (
                        <h3 className="text-2xl font-bold text-gray-900 mb-4">
                          {data.vision_mission.vision_title}
                        </h3>
                      )}
                      <p className="text-gray-600 leading-relaxed">
                        {data.vision_mission.vision_content}
                      </p>
                    </div>
                  </AnimatedSection>
                )}

                {/* Mission Card */}
                {data.vision_mission.mission_content && (
                  <AnimatedSection delay={0.2} direction="up">
                    <div className="group h-full bg-gradient-to-br from-amber-50 to-orange-50 rounded-3xl p-8 border border-amber-100 hover:shadow-xl hover:shadow-amber-100/50 transition-all duration-300 hover:-translate-y-1">
                      <div className="w-16 h-16 bg-gradient-to-br from-amber-500 to-orange-500 rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-amber-500/30 group-hover:scale-110 transition-transform">
                        <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                      </div>
                      {data.vision_mission.mission_title && (
                        <h3 className="text-2xl font-bold text-gray-900 mb-4">
                          {data.vision_mission.mission_title}
                        </h3>
                      )}
                      <p className="text-gray-600 leading-relaxed">
                        {data.vision_mission.mission_content}
                      </p>
                    </div>
                  </AnimatedSection>
                )}

                {/* Values Card */}
                {data.vision_mission.values_content && (
                  <AnimatedSection delay={0.3} direction="up">
                    <div className="group h-full bg-gradient-to-br from-emerald-50 to-teal-50 rounded-3xl p-8 border border-emerald-100 hover:shadow-xl hover:shadow-emerald-100/50 transition-all duration-300 hover:-translate-y-1 md:col-span-2 lg:col-span-1">
                      <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-emerald-500/30 group-hover:scale-110 transition-transform">
                        <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                        </svg>
                      </div>
                      {data.vision_mission.values_title && (
                        <h3 className="text-2xl font-bold text-gray-900 mb-4">
                          {data.vision_mission.values_title}
                        </h3>
                      )}
                      <p className="text-gray-600 leading-relaxed">
                        {data.vision_mission.values_content}
                      </p>
                    </div>
                  </AnimatedSection>
                )}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Principal's Message */}
      {data.principal && data.principal.message && (
        <section className="py-16 md:py-24 bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 text-white relative overflow-hidden">
          {/* Background decorations */}
          <div className="absolute inset-0">
            <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl" />
            <div className="absolute bottom-0 left-0 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl" />
          </div>

          <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div className="max-w-6xl mx-auto">
              <div className="grid md:grid-cols-3 gap-8 lg:gap-12 items-center">
                {/* Photo */}
                <AnimatedSection direction="left" className="md:col-span-1">
                  <div className="relative max-w-xs mx-auto md:max-w-none">
                    <div className="absolute -inset-4 bg-gradient-to-r from-blue-500/30 to-indigo-500/30 rounded-3xl blur-2xl" />
                    <div className="relative aspect-[3/4] rounded-2xl overflow-hidden shadow-2xl border-4 border-white/10">
                      {data.principal.photo ? (
                        <img 
                          src={data.principal.photo} 
                          alt={data.principal.name || ''} 
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center">
                          <span className="text-7xl font-bold text-white/50">
                            {data.principal.name?.charAt(0) || ''}
                          </span>
                        </div>
                      )}
                    </div>
                    {/* Name card overlay */}
                    {(data.principal.name || data.principal.title) && (
                      <div className="absolute -bottom-4 left-4 right-4 bg-white rounded-xl shadow-xl p-4 text-center">
                        {data.principal.name && (
                          <h3 className="text-lg font-bold text-gray-900">{data.principal.name}</h3>
                        )}
                        {data.principal.title && (
                          <p className="text-sm text-blue-600 font-medium">{data.principal.title}</p>
                        )}
                        {data.principal.qualification && (
                          <p className="text-xs text-gray-500 mt-1">{data.principal.qualification}</p>
                        )}
                      </div>
                    )}
                  </div>
                </AnimatedSection>

                {/* Message */}
                <AnimatedSection direction="right" delay={0.2} className="md:col-span-2 mt-12 md:mt-0">
                  <div className="relative">
                    {/* Large quote mark */}
                    <div className="absolute -top-8 -left-4 text-9xl text-blue-500/20 font-serif leading-none select-none hidden md:block">"</div>
                    
                    <blockquote className="relative text-lg sm:text-xl lg:text-2xl text-blue-100 leading-relaxed italic pl-0 md:pl-8">
                      {data.principal.message}
                    </blockquote>
                    
                    {/* Signature line */}
                    {data.principal.name && (
                      <div className="mt-8 pt-6 border-t border-white/10 pl-0 md:pl-8">
                        <div className="flex items-center gap-4">
                          <div className="w-12 h-1 bg-gradient-to-r from-amber-400 to-orange-400 rounded-full"></div>
                          <span className="text-amber-400 font-semibold">{data.principal.name}</span>
                        </div>
                      </div>
                    )}
                  </div>
                </AnimatedSection>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Timeline */}
      {data.timeline && data.timeline.length > 0 && (
        <section className="py-16 md:py-24 bg-gradient-to-b from-white to-gray-50">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
              <div className="relative">
                {/* Timeline line */}
                <div className="absolute left-8 md:left-1/2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-blue-500 via-indigo-500 to-purple-500 md:-translate-x-px"></div>

                {data.timeline.map((event, idx) => (
                  <AnimatedSection key={idx} delay={idx * 0.1} direction={idx % 2 === 0 ? 'left' : 'right'}>
                    <div className={`relative flex items-center gap-8 mb-12 ${idx % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse'}`}>
                      {/* Year badge - Always visible on mobile, alternating on desktop */}
                      <div className={`hidden md:flex flex-1 ${idx % 2 === 0 ? 'justify-end' : 'justify-start'}`}>
                        <div className="text-4xl lg:text-5xl font-bold text-blue-600/20">{event.year}</div>
                      </div>

                      {/* Center dot */}
                      <div className="absolute left-8 md:left-1/2 w-4 h-4 bg-white border-4 border-blue-500 rounded-full -translate-x-1/2 shadow-lg z-10"></div>

                      {/* Content card */}
                      <div className="flex-1 pl-16 md:pl-0">
                        <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-shadow p-6 border border-gray-100">
                          <div className="md:hidden text-2xl font-bold text-blue-600 mb-2">{event.year}</div>
                          {event.title && (
                            <h3 className="text-xl font-bold text-gray-900 mb-2">{event.title}</h3>
                          )}
                          {event.description && (
                            <p className="text-gray-600">{event.description}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  </AnimatedSection>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Facilities Grid */}
      {data.facilities && data.facilities.length > 0 && (
        <section className="py-16 md:py-24 bg-white">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-7xl mx-auto">
              {(data.infrastructure_title || data.infrastructure_content) && (
                <AnimatedSection className="text-center mb-16">
                  {data.infrastructure_title && (
                    <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900">
                      {data.infrastructure_title}
                    </h2>
                  )}
                  {data.infrastructure_content && (
                    <p className="text-lg text-gray-600 max-w-2xl mx-auto mt-4">
                      {data.infrastructure_content}
                    </p>
                  )}
                </AnimatedSection>
              )}

              <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {data.facilities.map((facility, idx) => (
                  <AnimatedSection key={facility.id} delay={idx * 0.05}>
                    <div className="group bg-gray-50 hover:bg-gradient-to-br hover:from-blue-50 hover:to-indigo-50 rounded-2xl p-6 border border-gray-100 hover:border-blue-200 hover:shadow-lg transition-all duration-300 cursor-default h-full">
                      <div className="flex items-start gap-4">
                        {facility.icon && (
                          <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20 group-hover:scale-110 transition-transform">
                            <span className="text-xl">{facility.icon}</span>
                          </div>
                        )}
                        <div className="flex-1 min-w-0">
                          {facility.name && (
                            <h3 className="text-lg font-bold text-gray-900 mb-1 group-hover:text-blue-600 transition-colors">
                              {facility.name}
                            </h3>
                          )}
                          {facility.description && (
                            <p className="text-sm text-gray-600 line-clamp-2">
                              {facility.description}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  </AnimatedSection>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Management Team */}
      {data.management && data.management.length > 0 && (
        <section className="py-16 md:py-24 bg-gradient-to-b from-gray-50 to-white">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
              {data.management.map((member, idx) => (
                <AnimatedSection key={idx} delay={idx * 0.1}>
                  <div className="group text-center">
                    <div className="relative w-40 h-40 mx-auto mb-6">
                      <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full opacity-0 group-hover:opacity-100 transition-opacity blur-xl scale-110" />
                      <div className="relative w-full h-full rounded-full overflow-hidden shadow-xl ring-4 ring-white group-hover:ring-blue-100 transition-all">
                        {member.photo ? (
                          <img src={member.photo} alt={member.name || ''} className="w-full h-full object-cover" />
                        ) : (
                          <div className="w-full h-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
                            <span className="text-4xl font-bold text-white/80">{member.name?.charAt(0) || ''}</span>
                          </div>
                        )}
                      </div>
                    </div>
                    {member.name && (
                      <h3 className="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
                        {member.name}
                      </h3>
                    )}
                    {member.designation && (
                      <p className="text-amber-600 font-medium">{member.designation}</p>
                    )}
                    {member.bio && (
                      <p className="text-gray-600 text-sm mt-2 max-w-xs mx-auto line-clamp-3">{member.bio}</p>
                    )}
                  </div>
                </AnimatedSection>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Affiliation Badge */}
      {(data.affiliation_title || data.affiliation_content || data.cbse_affiliation_no) && (
        <section className="py-16 md:py-20 bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <AnimatedSection className="max-w-4xl mx-auto text-center">
              {data.affiliation_title && (
                <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold mb-6">
                  {data.affiliation_title}
                </h2>
              )}
              {data.affiliation_content && (
                <p className="text-lg text-blue-100 mb-8 max-w-2xl mx-auto">
                  {data.affiliation_content}
                </p>
              )}
              {data.cbse_affiliation_no && (
                <div className="inline-flex items-center gap-3 bg-white/10 backdrop-blur-sm px-8 py-4 rounded-full border border-white/20">
                  <svg className="w-6 h-6 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="font-bold text-lg">{data.cbse_affiliation_no}</span>
                </div>
              )}
            </AnimatedSection>
          </div>
        </section>
      )}

      <Footer siteSettings={siteSettings} quickLinks={quickLinks} />
    </main>
  );
}
