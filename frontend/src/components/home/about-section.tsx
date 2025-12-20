'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { AboutSection as AboutData } from '@/lib/public-types';

interface AboutSectionProps {
  data: AboutData;
}

export default function AboutSection({ data }: AboutSectionProps) {
  return (
    <section className="py-16 sm:py-20 lg:py-28 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12">
        <div className="grid lg:grid-cols-2 gap-10 lg:gap-20 items-center">
          {/* Image Side */}
          <motion.div 
            className="relative order-2 lg:order-1"
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <div className="relative rounded-2xl overflow-hidden shadow-2xl">
              {data.image ? (
                <img 
                  src={data.image} 
                  alt="About our school"
                  className="w-full h-auto object-fill aspect-[4/3]"
                />
              ) : (
                <div className="w-full aspect-[4/3] bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center">
                  <span className="text-6xl sm:text-8xl opacity-50">🏫</span>
                </div>
              )}
            </div>
            
            {/* Floating Stats Card */}
            <div className="absolute -bottom-4 -right-4 sm:-bottom-6 sm:-right-6 bg-white rounded-xl shadow-xl p-4 sm:p-6 border-l-4 border-emerald-500">
              <div className="text-2xl sm:text-4xl font-bold text-gray-900 mb-1">{data.established_year || '1990'}</div>
              <div className="text-gray-500 font-medium text-xs sm:text-sm uppercase tracking-wider">Established</div>
            </div>
          </motion.div>

          {/* Content Side */}
          <motion.div
            className="order-1 lg:order-2"
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="inline-block px-3 sm:px-4 py-1 sm:py-1.5 bg-emerald-100 text-emerald-700 rounded-full text-xs sm:text-sm font-semibold mb-4 sm:mb-6">
              About Us
            </div>
            
            <h2 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold text-gray-900 mb-4 sm:mb-6 lg:mb-8 leading-tight">
              {data.title || 'A Legacy of Excellence in Education'}
            </h2>
            
            <p className="text-base sm:text-lg lg:text-xl text-gray-600 mb-6 sm:mb-8 lg:mb-10 leading-relaxed">
              {data.content || 'We are committed to providing a nurturing environment where every child can discover their potential and achieve excellence in academics, sports, and character development.'}
            </p>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 gap-3 sm:gap-4 lg:gap-6 mb-6 sm:mb-8 lg:mb-10">
              <div className="bg-gray-50 rounded-xl p-4 sm:p-6">
                <div className="text-xl sm:text-2xl lg:text-3xl font-bold text-emerald-600 mb-1 sm:mb-2">{data.students_count || '2500+'}</div>
                <div className="text-gray-600 font-medium text-xs sm:text-sm lg:text-base">Students Enrolled</div>
              </div>
              <div className="bg-gray-50 rounded-xl p-4 sm:p-6">
                <div className="text-xl sm:text-2xl lg:text-3xl font-bold text-cyan-500 mb-1 sm:mb-2">{data.teachers_count || '150+'}</div>
                <div className="text-gray-600 font-medium text-xs sm:text-sm lg:text-base">Expert Teachers</div>
              </div>
            </div>

            <Link 
              href="/about"
              className="inline-flex items-center gap-2 sm:gap-3 text-emerald-600 font-bold text-base sm:text-lg hover:text-emerald-800 transition-colors group"
            >
              Learn More About Us
              <svg className="w-4 h-4 sm:w-5 sm:h-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </Link>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
