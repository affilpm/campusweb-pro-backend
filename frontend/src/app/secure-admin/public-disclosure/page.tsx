'use client';

import Link from 'next/link';

interface SubSection {
  name: string;
  description: string;
  href: string;
  icon: string;
}

const subSections: SubSection[] = [
  {
    name: 'General',
    description: 'General information like school timings, affiliation, etc.',
    href: '/secure-admin/public-disclosure/general',
    icon: '📋',
  },
  {
    name: 'Documents',
    description: 'Upload and manage documents and files for public disclosure.',
    href: '/secure-admin/public-disclosure/documents',
    icon: '📄',
  },
  {
    name: 'Results & Academics',
    description: 'Upload academic results, reports, and related documents.',
    href: '/secure-admin/public-disclosure/results-academics',
    icon: '📊',
  },
  {
    name: 'Infrastructure',
    description: 'Manage infrastructure and facilities information.',
    href: '/secure-admin/public-disclosure/infrastructure',
    icon: '🏗️',
  },
  {
    name: 'Fees',
    description: 'Manage fees and payment structure information.',
    href: '/secure-admin/public-disclosure/fees',
    icon: '💰',
  },
];

export default function PublicDisclosurePage() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Public Disclosure</h1>
        <p className="text-gray-400">Manage public disclosure information for the homepage</p>
      </div>

      {/* Subsections Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {subSections.map((section) => (
          <Link
            key={section.name}
            href={section.href}
            className="bg-slate-800/50 backdrop-blur-xl rounded-2xl border border-white/10 p-6 hover:bg-slate-700/50 hover:border-purple-500/30 transition-all group"
          >
            <div className="flex items-start gap-4">
              <span className="text-3xl">{section.icon}</span>
              <div>
                <h2 className="text-lg font-semibold text-white group-hover:text-purple-400 transition-colors">
                  {section.name}
                </h2>
                <p className="text-sm text-gray-400 mt-1">
                  {section.description}
                </p>
              </div>
              <svg 
                className="w-5 h-5 text-gray-500 group-hover:text-purple-400 ml-auto transition-colors" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
