import { ReactNode } from 'react';
import { cn } from '@/lib/utils';
import { Container } from './container';

interface SectionProps {
  children: ReactNode;
  className?: string;
  id?: string;
  background?: 'white' | 'gray' | 'blue' | 'dark';
}

export function Section({ children, className, id, background = 'white' }: SectionProps) {
  const bgStyles = {
    white: 'bg-white',
    gray: 'bg-gray-50',
    blue: 'bg-blue-50',
    dark: 'bg-slate-900 text-white',
  };

  return (
    <section 
      id={id} 
      className={cn(
        'py-16 md:py-24', 
        bgStyles[background], 
        className
      )}
    >
      <Container>
        {children}
      </Container>
    </section>
  );
}
