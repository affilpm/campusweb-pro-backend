import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Photo Gallery | School',
  description: 'Explore our school photo gallery - capturing moments of learning, growth, and celebration from campus life and events.',
  keywords: ['school gallery', 'photos', 'campus life', 'events', 'school memories'],
  openGraph: {
    title: 'Photo Gallery | School',
    description: 'Explore our school photo gallery - capturing moments of learning, growth, and celebration.',
    type: 'website',
  },
};

export default function GalleryLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
