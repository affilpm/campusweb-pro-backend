'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useRef, useState, useEffect } from 'react';
import Link from 'next/link';
import { Event } from '@/lib/public-types';

interface EventsSectionProps {
  events: Event[];
}

export default function EventsSection({ events }: EventsSectionProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const scroll = (direction: 'left' | 'right') => {
    if (scrollRef.current) {
      const scrollAmount = 320;
      scrollRef.current.scrollBy({ 
        left: direction === 'left' ? -scrollAmount : scrollAmount, 
        behavior: 'smooth' 
      });
    }
  };

  useEffect(() => {
    if (selectedEvent) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
  }, [selectedEvent]);

  if (!events || events.length === 0) return null;

  const formatDate = (dateString: string): { month: string; day: string; full: string } => {
    // Return static placeholder during SSR to prevent hydration mismatch
    if (!mounted) {
      return { month: '---', day: '--', full: '---' };
    }
    const date = new Date(dateString);
    return {
      month: date.toLocaleDateString('en-US', { month: 'short' }),
      day: date.getDate().toString(),
      full: date.toLocaleDateString('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      })
    };
  };

  return (
    <>
      <section className="py-16 sm:py-20 lg:py-28 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12">
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 sm:gap-6 mb-8 sm:mb-12 lg:mb-16">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
            >
              <div className="inline-block px-3 sm:px-4 py-1 sm:py-1.5 bg-blue-100 text-blue-700 rounded-full text-xs sm:text-sm font-semibold mb-3 sm:mb-4">
                Events & Activities
              </div>
              <h2 className="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold text-gray-900 mb-2 sm:mb-4">
                Upcoming Events
              </h2>
              <p className="text-base sm:text-lg lg:text-xl text-gray-600 max-w-2xl">
                Stay updated with our latest events and activities.
              </p>
            </motion.div>
            
            {/* Navigation Arrows */}
            <div className="flex gap-2 sm:gap-3">
              <button 
                onClick={() => scroll('left')}
                className="w-10 h-10 sm:w-12 sm:h-12 rounded-full border-2 border-gray-200 flex items-center justify-center hover:border-blue-500 hover:text-blue-500 transition-colors"
                aria-label="Previous"
              >
                <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button 
                onClick={() => scroll('right')}
                className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-blue-600 text-white flex items-center justify-center hover:bg-blue-700 transition-colors shadow-lg"
                aria-label="Next"
              >
                <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>

          {/* Events Carousel */}
          <div 
            ref={scrollRef}
            className="flex gap-4 sm:gap-6 lg:gap-8 overflow-x-auto pb-6 sm:pb-8 -mx-4 sm:-mx-6 px-4 sm:px-6 scrollbar-hide snap-x"
            style={{ scrollbarWidth: 'none' }}
          >
            {events.map((event, index) => {
              const { month, day } = event.event_date ? formatDate(event.event_date) : { month: 'TBD', day: '--' };
              
              return (
                <motion.article
                  key={event.id}
                  initial={{ opacity: 0, x: 50 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="flex-shrink-0 w-[280px] sm:w-[320px] lg:w-[360px] bg-white rounded-xl sm:rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 group snap-start"
                  onClick={() => setSelectedEvent(event)}
                >
                  {/* Image */}
                  <div className="relative h-40 sm:h-48 lg:h-52 overflow-hidden bg-gray-100 cursor-pointer">
                    {event.image ? (
                      <img 
                        src={event.image} 
                        alt={event.title}
                        className="w-full h-full object-fill group-hover:scale-105 transition-transform duration-500"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center bg-blue-50">
                        <span className="text-4xl sm:text-5xl">📅</span>
                      </div>
                    )}
                    
                    {/* Date Badge */}
                    <div className="absolute top-3 sm:top-4 left-3 sm:left-4 bg-white rounded-lg sm:rounded-xl shadow-lg overflow-hidden text-center min-w-[50px] sm:min-w-[60px]">
                      <div className="bg-blue-600 text-white text-[10px] sm:text-xs font-bold py-1 sm:py-1.5 px-2 sm:px-3 uppercase">
                        {month}
                      </div>
                      <div className="py-1.5 sm:py-2 text-lg sm:text-2xl font-bold text-gray-900">
                        {day}
                      </div>
                    </div>

                    {event.is_featured && (
                      <div className="absolute top-3 sm:top-4 right-3 sm:right-4 px-2 sm:px-3 py-0.5 sm:py-1 bg-amber-500 text-white text-[10px] sm:text-xs font-bold rounded-full shadow">
                        Featured
                      </div>
                    )}
                  </div>
                  
                  {/* Content */}
                  <div className="p-4 sm:p-6 lg:p-8 cursor-pointer">
                    <h3 className="text-base sm:text-lg lg:text-xl font-bold text-gray-900 mb-2 sm:mb-3 line-clamp-2 group-hover:text-blue-600 transition-colors">
                      {event.title}
                    </h3>
                    <p className="text-gray-600 mb-4 sm:mb-6 line-clamp-2 leading-relaxed text-sm sm:text-base">
                      {event.excerpt}
                    </p>
                    <button 
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedEvent(event);
                      }}
                      className="inline-flex items-center gap-1 sm:gap-2 text-blue-600 font-semibold hover:text-blue-800 transition-colors text-sm sm:text-base"
                    >
                      View Details
                      <svg className="w-3 h-3 sm:w-4 sm:h-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                      </svg>
                    </button>
                  </div>
                </motion.article>
              );
            })}
          </div>
        </div>
      </section>

      {/* Event Modal */}
      <AnimatePresence>
      {selectedEvent && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
          <div 
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
            onClick={() => setSelectedEvent(null)}
          />
          <motion.div 
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto flex flex-col"
          >
            {/* Modal Image */}
            <div className="relative h-48 sm:h-64 bg-gray-100 flex-shrink-0">
               {selectedEvent.image ? (
                <img 
                  src={selectedEvent.image} 
                  alt={selectedEvent.title}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center bg-blue-50">
                  <span className="text-6xl">📅</span>
                </div>
              )}
              {/* Close Button */}
              <button 
                onClick={() => setSelectedEvent(null)}
                className="absolute top-4 right-4 p-2 bg-white/90 hover:bg-white text-gray-800 rounded-full shadow-lg transition-colors backdrop-blur-sm"
              >
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-6 sm:p-8 flex-1 overflow-y-auto">
              <div className="flex flex-wrap items-center gap-3 mb-4">
                {selectedEvent.event_date && (
                  <span className="text-sm font-medium text-blue-700 bg-blue-100 px-3 py-1 rounded-full">
                     {formatDate(selectedEvent.event_date).full}
                  </span>
                )}
                {selectedEvent.is_featured && (
                  <span className="text-xs font-bold text-amber-700 bg-amber-100 px-2 py-1 rounded uppercase">
                    Featured
                  </span>
                )}
              </div>
              
              <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-6">
                {selectedEvent.title}
              </h2>

              <div className="prose prose-blue max-w-none text-gray-700 whitespace-pre-wrap">
                {selectedEvent.content || selectedEvent.excerpt}
              </div>
            </div>
          </motion.div>
        </div>
      )}
      </AnimatePresence>
    </>
  );
}
