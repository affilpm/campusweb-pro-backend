'use client';

import Image from 'next/image';
import { Achievement } from '@/lib/public-types';

interface AchievementsSectionProps {
  achievements: Achievement[];
}

export default function AchievementsSection({ achievements }: AchievementsSectionProps) {
  if (!achievements || achievements.length === 0) {
    return null;
  }

  return (
    <section className="py-24 bg-gradient-to-br from-slate-900 to-indigo-950 relative overflow-hidden">
        {/* Decorative background elements */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl translate-x-1/2 -translate-y-1/2" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl -translate-x-1/2 translate-y-1/2" />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-4">
              Awards <span className="text-amber-400">&</span> Achievements
            </h2>
            <p className="text-lg text-indigo-200 max-w-2xl mx-auto">
              Celebrating excellence and the outstanding accomplishments of our students and institution.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {achievements.map((achievement) => (
              <div 
                key={achievement.id}
                className="group bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden hover:bg-white/10 transition-all duration-500 hover:-translate-y-2 hover:shadow-2xl hover:shadow-indigo-500/20"
              >
                {/* Image Container */}
                <div className="relative h-64 overflow-hidden">
                  {achievement.image ? (
                    <Image
                      src={achievement.image}
                      alt={achievement.title}
                      fill
                      className="object-cover transition-transform duration-700 group-hover:scale-110"
                      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                    />
                  ) : (
                    <div className="w-full h-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                      <svg className="w-20 h-20 text-white/50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                      </svg>
                    </div>
                  )}
                  {/* Overlay Gradient */}
                  <div className="absolute inset-x-0 bottom-0 h-2/3 bg-gradient-to-t from-slate-950 via-slate-950/80 to-transparent" />
                  
                  {/* Year Badge */}
                  {achievement.year && (
                    <div className="absolute top-4 right-4 bg-amber-500 text-slate-950 text-xs font-bold px-3 py-1 rounded-full shadow-lg">
                        {achievement.year}
                    </div>
                  )}
                </div>

                {/* Content */}
                <div className="p-6 relative">
                  <h3 className="text-xl font-bold text-white mb-2 line-clamp-2 group-hover:text-amber-400 transition-colors">
                    {achievement.title}
                  </h3>
                  <p className="text-gray-300 text-sm line-clamp-3 leading-relaxed">
                    {achievement.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
    </section>
  );
}
