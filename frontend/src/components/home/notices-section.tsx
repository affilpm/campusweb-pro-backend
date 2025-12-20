'use client';

import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Notice } from '@/lib/public-types';

interface NoticesSectionProps {
  notices: Notice[];
}

export default function NoticesSection({ notices }: NoticesSectionProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [selectedNotice, setSelectedNotice] = useState<Notice | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!notices || notices.length <= 1 || isPaused || selectedNotice) return;
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % notices.length);
    }, 4000);
    return () => clearInterval(interval);
  }, [notices, isPaused, selectedNotice]);

  useEffect(() => {
    if (selectedNotice) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
  }, [selectedNotice]);

  if (!notices || notices.length === 0) return null;

  const formatDate = (dateString: string) => {
    // Return static placeholder during SSR to prevent hydration mismatch
    if (!mounted) return '---';
    return new Date(dateString).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const formatFullDate = (dateString: string) => {
    // Return static placeholder during SSR to prevent hydration mismatch
    if (!mounted) return '---';
    return new Date(dateString).toLocaleDateString('en-US', { 
      weekday: 'long',
      year: 'numeric',
      month: 'long', 
      day: 'numeric' 
    });
  };

  return (
    <>
      <section className="py-4 sm:py-6 lg:py-8 bg-amber-50 border-y border-amber-100 relative z-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12">
          <div 
            className="flex flex-col sm:flex-row items-start sm:items-center gap-4 sm:gap-6"
            onMouseEnter={() => setIsPaused(true)}
            onMouseLeave={() => setIsPaused(false)}
          >
            {/* Label */}
            <div className="flex items-center gap-3 sm:gap-4 flex-shrink-0">
              <div className="flex items-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-1.5 sm:py-2 bg-amber-500 text-white rounded-lg font-semibold text-xs sm:text-sm">
                <svg className="w-3 h-3 sm:w-4 sm:h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <span className="hidden xs:inline">Latest</span> Updates
              </div>
              <div className="hidden lg:block w-px h-8 bg-amber-200" />
            </div>

            {/* Notices Ticker */}
            <div className="flex-1 w-full relative h-[50px] sm:h-[60px] overflow-hidden">
              {notices.map((notice, index) => (
                <motion.div
                  key={notice.id}
                  className="absolute inset-0 flex items-center"
                  initial={false}
                  animate={{ 
                    opacity: index === currentIndex ? 1 : 0,
                    y: index === currentIndex ? 0 : 20,
                    pointerEvents: index === currentIndex ? 'auto' : 'none'
                  }}
                  transition={{ duration: 0.4 }}
                >
                  <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-4 w-full pr-4">
                    <span className="text-amber-600 font-medium text-xs sm:text-sm whitespace-nowrap">
                      {formatDate(notice.publish_date)}
                    </span>
                    <button 
                      onClick={() => setSelectedNotice(notice)}
                      className="text-left text-gray-800 font-semibold hover:text-amber-700 transition-colors line-clamp-1 text-sm sm:text-base lg:text-lg focus:outline-none"
                    >
                      {notice.title}
                    </button>
                    {notice.is_important && (
                      <span className="hidden sm:inline-flex flex-shrink-0 px-2 py-0.5 bg-red-100 text-red-600 text-xs font-bold rounded uppercase">
                        Important
                      </span>
                    )}
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Navigation */}
            <div className="flex items-center gap-3 sm:gap-4 self-end sm:self-auto">
              <div className="flex gap-1 sm:gap-1.5">
                {notices.map((_, idx) => (
                  <button
                    key={idx}
                    onClick={() => setCurrentIndex(idx)}
                    className={`h-1.5 sm:h-2 rounded-full transition-all duration-300 ${
                      idx === currentIndex ? 'w-4 sm:w-6 bg-amber-500' : 'w-1.5 sm:w-2 bg-amber-300 hover:bg-amber-400'
                    }`}
                    aria-label={`Go to notice ${idx + 1}`}
                  />
                ))}
              </div>
              <Link 
                href="/notices"
                className="hidden sm:inline-flex items-center gap-1 text-amber-700 font-semibold text-xs sm:text-sm hover:text-amber-800"
              >
                View All
                <svg className="w-3 h-3 sm:w-4 sm:h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Notice Modal */}
      {selectedNotice && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
          <div 
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
            onClick={() => setSelectedNotice(null)}
          />
          <motion.div 
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
          >
            {/* Modal Header */}
            <div className="sticky top-0 bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between z-10">
              <div className="flex items-center gap-3">
                 <span className="text-sm font-medium text-amber-700 bg-amber-100 px-3 py-1 rounded-full">
                  {formatDate(selectedNotice.publish_date)}
                </span>
                {selectedNotice.is_important && (
                  <span className="text-xs font-bold text-red-600 bg-red-100 px-2 py-1 rounded uppercase">
                    Important
                  </span>
                )}
              </div>
              <button 
                onClick={() => setSelectedNotice(null)}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors"
              >
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-6 sm:p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                {selectedNotice.title}
              </h2>
              <p className="text-sm text-gray-500 mb-6">
                Published on {formatFullDate(selectedNotice.publish_date)}
              </p>

              <div className="prose prose-amber max-w-none text-gray-700 whitespace-pre-wrap mb-8">
                {selectedNotice.content}
              </div>

              {selectedNotice.attachment && (
                <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 flex items-center gap-4 group hover:border-amber-300 transition-colors">
                  <div className="w-10 h-10 rounded-lg bg-amber-100 text-amber-600 flex items-center justify-center flex-shrink-0">
                    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">Attachment Available</p>
                    <a 
                      href={selectedNotice.attachment}
                      target="_blank"
                      rel="noopener noreferrer" 
                      className="text-xs text-amber-600 hover:text-amber-700 font-medium"
                    >
                      Download Document &rarr;
                    </a>
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        </div>
      )}
    </>
  );
}
