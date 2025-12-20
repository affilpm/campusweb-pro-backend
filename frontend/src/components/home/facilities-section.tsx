'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { Facility } from '@/lib/public-types';

interface FacilitiesSectionProps {
  facilities: Facility[];
  initialCount?: number;
}

export default function FacilitiesSection({ facilities, initialCount = 6 }: FacilitiesSectionProps) {
  if (!facilities || facilities.length === 0) return null;

  const displayedFacilities = facilities.slice(0, initialCount);

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12">
        
        {/* Header */}
        <motion.div 
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <span className="text-emerald-600 font-bold tracking-wider uppercase text-sm mb-2 block">
            Campus Infrastructure
          </span>
          <h2 className="text-3xl md:text-5xl font-bold text-gray-900 mb-6">
            Our World Class Facilities
          </h2>
          <div className="w-24 h-1.5 bg-gradient-to-r from-emerald-500 to-cyan-500 mx-auto rounded-full"></div>
        </motion.div>

        {/* Grid Container */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {displayedFacilities.map((facility, index) => (
            <motion.div
              key={facility.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
            >
              <Link 
                href={`/facilities/${facility.slug || facility.id}`} 
                className="group relative block h-80 w-full overflow-hidden rounded-[2.5rem] shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2"
              >
                {/* Image Background */}
                <div className="absolute inset-0 bg-gray-200">
                  {facility.image ? (
                    <img
                      src={facility.image}
                      alt={facility.name}
                      className="h-full w-full object-fill transition-transform duration-700 group-hover:scale-105"
                    />
                  ) : (
                    <div className="h-full w-full flex items-center justify-center bg-gradient-to-br from-emerald-500 to-cyan-600">
                      <span className="text-7xl">{facility.icon || '🏫'}</span>
                    </div>
                  )}
                </div>

                {/* Dark Overlay for Text Readability */}
                <div className="absolute inset-0 bg-black/30 group-hover:bg-black/40 transition-colors duration-500" />
                
                {/* Content Container - Centered */}
                <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center z-10">
                   {/* Title */}
                  <h3 className="text-4xl font-bold text-white tracking-wide drop-shadow-lg transform transition-transform duration-500 group-hover:scale-105">
                    {facility.name}
                  </h3>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>

        {/* View All Button */}
        <div className="mt-16 text-center">
            <Link 
              href="/facilities" 
              className="inline-flex items-center gap-2 px-8 py-3 bg-gray-100 hover:bg-gray-200 text-gray-900 font-bold rounded-full transition-all duration-300 hover:shadow-md"
            >
                View All Facilities
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
            </Link>
        </div>
      </div>
    </section>
  );
}
