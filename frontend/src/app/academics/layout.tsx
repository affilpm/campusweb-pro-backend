import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Academics | School',
  description: 'Explore our comprehensive curriculum, teaching methodology, and academic programs designed to nurture excellence in every student.',
  keywords: ['academics', 'curriculum', 'education', 'school programs', 'teaching methodology', 'class categories'],
  openGraph: {
    title: 'Academics | School',
    description: 'Explore our comprehensive curriculum, teaching methodology, and academic programs.',
    type: 'website',
  },
};

export default function AcademicsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
