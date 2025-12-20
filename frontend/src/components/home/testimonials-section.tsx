'use client';

import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { Testimonial } from '@/lib/public-types';

interface TestimonialsSectionProps {
  testimonials: Testimonial[];
}

export default function TestimonialsSection({ testimonials }: TestimonialsSectionProps) {
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    if (!testimonials || testimonials.length <= 1) return;
    const interval = setInterval(() => {
      setActiveIndex((prev) => (prev + 1) % testimonials.length);
    }, 6000);
    return () => clearInterval(interval);
  }, [testimonials]);

  if (!testimonials || testimonials.length === 0) return null;

  return (
    <section className="py-16 sm:py-20 lg:py-28 bg-emerald-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12">
        {/* Header */}
        <motion.div 
          className="text-center mb-10 sm:mb-14 lg:mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <div className="inline-block px-3 sm:px-4 py-1 sm:py-1.5 bg-emerald-100 text-emerald-700 rounded-full text-xs sm:text-sm font-semibold mb-4 sm:mb-6">
            Testimonials
          </div>
          <h2 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold text-gray-900 mb-4 sm:mb-6">
            What Parents Say
          </h2>
          <p className="text-base sm:text-lg lg:text-xl text-gray-600 max-w-2xl mx-auto px-4">
            Hear from our community about their experience with us.
          </p>
        </motion.div>

        {/* Testimonial Card */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-2xl sm:rounded-3xl shadow-xl p-6 sm:p-10 lg:p-16 relative min-h-[280px] sm:min-h-[300px]">
            {/* Quote Mark */}
            <div className="absolute top-4 sm:top-8 left-4 sm:left-8 text-6xl sm:text-8xl lg:text-9xl text-emerald-100 font-serif leading-none select-none">
              "
            </div>
            
            {/* Testimonials */}
            <div className="relative">
              {testimonials.map((testimonial, index) => (
                <motion.div 
                  key={testimonial.id}
                  className="text-center"
                  initial={false}
                  animate={{ 
                    opacity: index === activeIndex ? 1 : 0, 
                    y: index === activeIndex ? 0 : 20,
                    position: index === activeIndex ? 'relative' : 'absolute',
                    pointerEvents: index === activeIndex ? 'auto' : 'none'
                  }}
                  transition={{ duration: 0.5 }}
                  style={{ 
                    top: 0, 
                    left: 0, 
                    right: 0,
                    zIndex: index === activeIndex ? 1 : 0
                  }}
                >
                  <p className="text-base sm:text-lg lg:text-xl xl:text-2xl text-gray-700 leading-relaxed italic mb-6 sm:mb-8 lg:mb-10 max-w-3xl mx-auto px-4">
                    "{testimonial.content}"
                  </p>
                  
                  <div className="flex flex-col items-center gap-3 sm:gap-4">
                    <div className="w-12 h-12 sm:w-14 sm:h-14 lg:w-16 lg:h-16 rounded-full overflow-hidden border-2 sm:border-4 border-white shadow-lg">
                      {testimonial.photo ? (
                        <img 
                          src={testimonial.photo} 
                          alt={testimonial.name}
                          className="w-full h-full object-fill"
                        />
                      ) : (
                        <div className="w-full h-full bg-emerald-100 flex items-center justify-center text-emerald-600 font-bold text-lg sm:text-xl">
                          {testimonial.name.charAt(0)}
                        </div>
                      )}
                    </div>
                    <div>
                      <h4 className="text-lg sm:text-xl font-bold text-gray-900">{testimonial.name}</h4>
                      <p className="text-emerald-600 font-medium text-sm sm:text-base">{testimonial.role}</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Navigation Dots */}
          <div className="flex justify-center gap-2 sm:gap-3 mt-6 sm:mt-8 lg:mt-10">
            {testimonials.map((_, idx) => (
              <button
                key={idx}
                onClick={() => setActiveIndex(idx)}
                className={`h-2 sm:h-3 rounded-full transition-all duration-300 ${
                  idx === activeIndex 
                    ? 'w-6 sm:w-10 bg-emerald-600' 
                    : 'w-2 sm:w-3 bg-emerald-200 hover:bg-emerald-300'
                }`}
                aria-label={`View testimonial ${idx + 1}`}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

