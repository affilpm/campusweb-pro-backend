'use client';

import { motion } from 'framer-motion';
import { PrincipalMessage as PrincipalData } from '@/lib/public-types';

interface PrincipalSectionProps {
  data: PrincipalData;
}

export default function PrincipalSection({ data }: PrincipalSectionProps) {
  return (
    <section className="py-12 sm:py-16 lg:py-20 bg-gray-50">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="grid md:grid-cols-5">
            {/* Image Side */}
            <motion.div 
              className="md:col-span-2 relative min-h-[250px] md:min-h-full"
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
            >
              {data.photo ? (
                <img 
                  src={data.photo} 
                  alt={data.name}
                  className="absolute inset-0 w-full h-full object-fill"
                />
              ) : (
                <div className="absolute inset-0 bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center">
                  <span className="text-6xl md:text-8xl text-white/30 font-bold">{data.name?.charAt(0) || 'P'}</span>
                </div>
              )}
            </motion.div>

            {/* Content Side */}
            <motion.div 
              className="md:col-span-3 p-6 md:p-10 flex flex-col justify-center"
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
            >
              <div className="inline-block px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-xs font-semibold mb-4 w-fit">
                Principal's Message
              </div>
              
              <div className="relative mb-6">
                <span className="absolute -top-4 -left-2 text-6xl text-gray-100 font-serif select-none">"</span>
                <blockquote className="relative text-lg md:text-xl text-gray-700 leading-relaxed font-light italic">
                  {data.message || "Education is the most powerful weapon which you can use to change the world. We are committed to nurturing young minds."}
                </blockquote>
              </div>
              
              <div className="border-t border-gray-100 pt-4 md:pt-6">
                <h3 className="text-lg md:text-xl font-bold text-gray-900 mb-0.5">{data.name || 'Principal Name'}</h3>
                <p className="text-blue-600 font-medium text-sm mb-1">{data.title || 'Principal'}</p>
                {data.qualification && (
                  <p className="text-gray-500 text-xs">{data.qualification}</p>
                )}
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  );
}
