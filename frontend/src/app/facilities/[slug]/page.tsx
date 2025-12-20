'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import Header from '@/components/home/header';
import Footer from '@/components/home/footer';

interface FacilityImage {
  id: number;
  image: string;
  caption: string;
  order: number;
}

interface FacilityDetail {
  id: number;
  name: string;
  slug: string;
  short_description: string;
  long_description: string;
  icon: string;
  cover_image: string | null;
  gallery: FacilityImage[];
}

export default function FacilityDetailPage() {
  const params = useParams();
  const slug = params.slug as string;

  const [facility, setFacility] = useState<FacilityDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedImage, setSelectedImage] = useState<FacilityImage | null>(null);
  const [siteSettings, setSiteSettings] = useState<any>(null);
  const [quickLinks, setQuickLinks] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        
        // Fetch facility detail
        const facilityRes = await fetch(`${apiUrl}/api/public/facilities/${slug}/`);
        if (!facilityRes.ok) throw new Error('Facility not found');
        const facilityData = await facilityRes.json();
        setFacility(facilityData);

        // Fetch site settings
        const homeRes = await fetch(`${apiUrl}/api/public/home/`);
        if (homeRes.ok) {
          const homeData = await homeRes.json();
          setSiteSettings(homeData.site_settings);
          setQuickLinks(homeData.quick_links || []);
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (slug) {
      fetchData();
    }
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
          <p className="mt-4 text-gray-600">Loading facility...</p>
        </div>
      </div>
    );
  }

  if (error || !facility) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center max-w-md">
          <span className="text-6xl mb-4 block">🏫</span>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Facility Not Found</h1>
          <p className="text-gray-600 mb-6">{error || "The facility you're looking for doesn't exist."}</p>
          <Link
            href="/facilities"
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Facilities
          </Link>
        </div>
      </div>
    );
  }

  const defaultSettings = {
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

  return (
    <main className="bg-white min-h-screen">
      <Header siteSettings={siteSettings || defaultSettings} />

      {/* Hero Section */}
      <section className="relative h-[50vh] min-h-[400px] bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 overflow-hidden">
        {facility.cover_image ? (
          <>
            <img 
              src={facility.cover_image} 
              alt={facility.name}
              className="absolute inset-0 w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-black/20" />
          </>
        ) : (
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-[200px] opacity-20">{facility.icon}</span>
          </div>
        )}

        <div className="relative h-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 flex flex-col justify-end pb-12">
          {/* Breadcrumb */}
          <nav className="mb-6">
            <ol className="flex items-center gap-2 text-white/70 text-sm">
              <li><Link href="/" className="hover:text-white transition-colors">Home</Link></li>
              <li>/</li>
              <li><Link href="/facilities" className="hover:text-white transition-colors">Facilities</Link></li>
              <li>/</li>
              <li className="text-white font-medium">{facility.name}</li>
            </ol>
          </nav>

          {/* Title */}
          <div className="flex items-center gap-4 mb-4">
            <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
              <span className="text-4xl">{facility.icon}</span>
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white">
              {facility.name}
            </h1>
          </div>

          <p className="text-xl text-white/80 max-w-3xl">
            {facility.short_description}
          </p>
        </div>
      </section>

      {/* Content Section */}
      <section className="py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12">
          <div className="grid lg:grid-cols-3 gap-12">
            {/* Main Content */}
            <div className="lg:col-span-2">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">About This Facility</h2>
              <div className="prose prose-lg max-w-none text-gray-600">
                {facility.long_description ? (
                  facility.long_description.split('\n').map((paragraph, idx) => (
                    <p key={idx}>{paragraph}</p>
                  ))
                ) : (
                  <p>{facility.short_description}</p>
                )}
              </div>
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <div className="bg-gray-50 rounded-2xl p-6 sticky top-24">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Facility Info</h3>
                <div className="space-y-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                      <span className="text-xl">{facility.icon}</span>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Facility Type</p>
                      <p className="font-semibold text-gray-900">{facility.name}</p>
                    </div>
                  </div>
                  {facility.gallery.length > 0 && (
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                        <span className="text-xl">📷</span>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Gallery</p>
                        <p className="font-semibold text-gray-900">{facility.gallery.length} Photos</p>
                      </div>
                    </div>
                  )}
                </div>

                <Link
                  href="/facilities"
                  className="mt-6 w-full inline-flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                  All Facilities
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Gallery Section */}
      {facility.gallery.length > 0 && (
        <section className="py-16 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Photo Gallery</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {facility.gallery.map((img, idx) => (
                <motion.div
                  key={img.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: idx * 0.05 }}
                  className="relative group cursor-pointer rounded-xl overflow-hidden shadow-md aspect-square"
                  whileHover={{ scale: 1.02 }}
                  onClick={() => setSelectedImage(img)}
                >
                  <img 
                    src={img.image} 
                    alt={img.caption || `${facility.name} - Image ${idx + 1}`}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                    loading="lazy"
                  />
                  
                  {/* Overlay */}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  
                  {/* Caption on Hover */}
                  <div className="absolute bottom-0 left-0 right-0 p-4 translate-y-full group-hover:translate-y-0 transition-transform duration-300">
                    <p className="text-white font-medium text-sm line-clamp-2">
                      {img.caption || facility.name}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Image Lightbox */}
      <AnimatePresence>
        {selectedImage && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
            onClick={() => setSelectedImage(null)}
          >
            <button 
              className="absolute top-6 right-6 w-12 h-12 bg-white/10 rounded-full flex items-center justify-center text-white hover:bg-white/20 transition-colors"
              onClick={() => setSelectedImage(null)}
            >
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            
            <motion.img
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              src={selectedImage.image}
              alt={selectedImage.caption || facility.name}
              className="max-w-full max-h-[80vh] rounded-lg"
              onClick={(e) => e.stopPropagation()}
            />
            
            {selectedImage.caption && (
              <p className="absolute bottom-6 left-0 right-0 text-center text-white text-lg">
                {selectedImage.caption}
              </p>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      <Footer siteSettings={siteSettings || defaultSettings} quickLinks={quickLinks} />
    </main>
  );
}
